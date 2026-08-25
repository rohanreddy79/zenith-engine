//! Real-process `kill -9` acceptance tests: SIGKILL a subprocess mid-workflow
//! on a real filesystem WAL, restart it, and assert recovery semantics.

#![allow(clippy::disallowed_methods)] // real-time test driver: wall sleeps are the point

use std::path::Path;
use std::process::{Child, Command, Stdio};
use std::time::{Duration, Instant};

fn spawn_child(dir: &Path, scenario: &str) -> Child {
    Command::new(env!("CARGO_BIN_EXE_crash_child"))
        .arg(dir)
        .arg(scenario)
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()
        .expect("spawn crash_child")
}

fn wait_with_timeout(mut child: Child, timeout: Duration) -> (bool, String) {
    let start = Instant::now();
    loop {
        match child.try_wait().expect("try_wait") {
            Some(status) => {
                let out = child.wait_with_output().expect("collect output");
                let stdout = String::from_utf8_lossy(&out.stdout).to_string();
                assert!(
                    status.success(),
                    "child failed: {status:?}\nstdout: {stdout}\nstderr: {}",
                    String::from_utf8_lossy(&out.stderr)
                );
                return (true, stdout);
            }
            None if start.elapsed() > timeout => {
                let _ = child.kill();
                panic!("child did not finish within {timeout:?}");
            }
            None => std::thread::sleep(Duration::from_millis(50)),
        }
    }
}

fn effect_lines(dir: &Path) -> Vec<String> {
    std::fs::read_to_string(dir.join("effects.log"))
        .unwrap_or_default()
        .lines()
        .map(str::to_string)
        .collect()
}

#[test]
fn kill_dash_nine_mid_saga_resumes_from_last_completed_step() {
    let dir = tempfile::tempdir().unwrap();
    // Run 1: SIGKILL ~500ms in (mid step 3 of 5; each step takes 150ms).
    let mut child = spawn_child(dir.path(), "saga");
    std::thread::sleep(Duration::from_millis(500));
    child.kill().expect("SIGKILL");
    let status = child.wait().expect("reap");
    assert!(!status.success(), "child must have died from SIGKILL");
    let before = effect_lines(dir.path());
    assert!(
        !before.is_empty() && before.len() < 5,
        "kill must land mid-workflow; effects so far: {before:?}"
    );

    // Run 2: restart; the workflow must resume and complete.
    let child = spawn_child(dir.path(), "saga");
    let (_, stdout) = wait_with_timeout(child, Duration::from_secs(30));
    assert!(
        stdout.contains("RESULT:15"),
        "saga result 1+2+3+4+5: {stdout}"
    );

    let after = effect_lines(dir.path());
    // Every step ran at least once…
    for step_no in 0..5 {
        assert!(
            after.iter().any(|l| l == &format!("step-{step_no}")),
            "step-{step_no} must have executed: {after:?}"
        );
    }
    // …and completed steps did NOT re-execute: at most the in-flight step
    // repeats, so at most 6 total executions.
    assert!(
        after.len() <= 6,
        "no duplicated completed steps (at-least-once allows only the \
         in-flight one to repeat): {after:?}"
    );
}

#[test]
fn kill_dash_nine_mid_sleep_timer_survives_restart() {
    let dir = tempfile::tempdir().unwrap();
    let t0 = Instant::now();
    // Run 1: the workflow sleeps 2s; kill at ~1s.
    let mut child = spawn_child(dir.path(), "sleeper");
    std::thread::sleep(Duration::from_millis(1_000));
    child.kill().expect("SIGKILL");
    let status = child.wait().expect("reap");
    assert!(!status.success(), "child must have died from SIGKILL");
    assert!(
        effect_lines(dir.path()).is_empty(),
        "killed mid-sleep: nothing after the timer may have run"
    );

    // Run 2: timer must re-arm from the journal and fire on the original
    // schedule.
    let child = spawn_child(dir.path(), "sleeper");
    let (_, stdout) = wait_with_timeout(child, Duration::from_secs(30));
    let line = stdout
        .lines()
        .find(|l| l.starts_with("RESULT:"))
        .expect("result line");
    let v: serde_json::Value = serde_json::from_str(&line["RESULT:".len()..]).unwrap();
    let (started, woke) = (v[0].as_u64().unwrap(), v[1].as_u64().unwrap());
    assert!(
        woke.saturating_sub(started) >= 2_000,
        "durable sleep must span >= 2s of logical time: started={started} woke={woke}"
    );
    let total = t0.elapsed();
    assert!(
        total >= Duration::from_secs(2),
        "wall clock must reflect the full sleep: {total:?}"
    );
    assert_eq!(effect_lines(dir.path()), vec!["woke".to_string()]);
}
