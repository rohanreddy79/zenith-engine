//! Fuzz the replay/recovery engine: a WAL directory whose segment holds
//! arbitrary fuzzer bytes must open (with truncation), list, and replay
//! without panicking; workflows either recover or land in a defined state.
#![no_main]
use libfuzzer_sys::fuzz_target;
use sqrl_core::vfs::Vfs;
use sqrl_core::{Ctx, EngineConfig, Registry};
use sqrl_sim::{SimClock, SimDisk, SimScheduler};
use sqrl_store::{WalOptions, WalStorage};
use std::sync::Arc;

fuzz_target!(|data: &[u8]| {
    let disk = SimDisk::new(1);
    // Seed the store with a real prefix so the fuzzer's tail lands mid-log.
    {
        let storage = WalStorage::open_with(
            Arc::new(disk.clone()),
            WalOptions { num_shards: 1, segment_size: 1 << 20 },
        )
        .unwrap();
        let mut reg = Registry::new();
        reg.register("wf", 1, |ctx: Ctx, n: u64| async move {
            let v: u64 = ctx
                .step("s", move || async move { Ok::<u64, String>(n) })
                .await?;
            let w: u64 = ctx.await_signal("go").await?;
            Ok(v + w)
        });
        let clock = SimClock::new(sqrl_core::LogicalTime::from_millis(1000));
        let mut sched =
            SimScheduler::with_clock(1, &storage, Arc::new(reg), EngineConfig::default(), clock)
                .unwrap();
        let _ = sched.start("wf-1", "wf", &5u64);
        sched.run_until_idle();
    }
    // Append fuzz bytes to the tail of the segment.
    {
        let names = disk.view_image();
        if let Some(seg) = names.keys().find(|k| k.contains("wal-")) {
            let mut f = disk.open(seg, false).unwrap();
            let len = f.len().unwrap();
            let cut = if data.is_empty() { len } else { len.saturating_sub((data[0] as u64) % len.max(1)) };
            f.truncate(cut).unwrap();
            f.write_at(cut, data).unwrap();
            f.sync().unwrap();
        }
    }
    // Recovery over the mangled store must not panic.
    let storage = match WalStorage::open_with(
        Arc::new(disk.clone()),
        WalOptions { num_shards: 1, segment_size: 1 << 20 },
    ) {
        Ok(s) => s,
        Err(_) => return, // defined failure is fine
    };
    let mut reg = Registry::new();
    reg.register("wf", 1, |ctx: Ctx, n: u64| async move {
        let v: u64 = ctx
            .step("s", move || async move { Ok::<u64, String>(n) })
            .await?;
        let w: u64 = ctx.await_signal("go").await?;
        Ok(v + w)
    });
    let clock = SimClock::new(sqrl_core::LogicalTime::from_millis(500_000));
    if let Ok(mut sched) =
        SimScheduler::with_clock(2, &storage, Arc::new(reg), EngineConfig::default(), clock)
    {
        sched.run_until_idle();
        let _ = sched.signal("wf-1", "go", &1u64);
        sched.run_until_idle();
        let _ = sched.states();
    }
});
