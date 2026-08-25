//! # ai_agent_loop — a durable AI-agent tool-call loop (mocked LLM)
//!
//! The classic agent loop — call the LLM, execute the tool it asks for,
//! append the observation, repeat until it produces a final answer — written
//! as a sqrl workflow.
//!
//! THE POINT: **every LLM call and every tool call is its own durably
//! journaled step.** If the process crashes (power cut, OOM, deploy) at any
//! point in the loop, the restarted process replays the journal and resumes
//! at the exact turn it died on:
//!
//!   * completed LLM calls are NOT re-issued — no re-paying for tokens, no
//!     nondeterministic second opinion changing the agent's trajectory;
//!   * completed tool calls are NOT re-executed — no duplicated side
//!     effects;
//!   * the transcript is rebuilt deterministically from journaled step
//!     results, because it only accumulates in orchestration code.
//!
//! The LLM here is a mock that scripts a 3-turn run (search → calculate →
//! final answer). A real integration would make its API call *inside* the
//! step closure — everything else stays the same.
//!
//! Run with: `cargo run -p ai_agent_loop`

use serde::{Deserialize, Serialize};
use sqrl::{Ctx, Sqrl, WalStorage};

/// Maximum turns before the agent gives up.
const MAX_TURNS: u32 = 6;

/// What the (mock) LLM returns each turn. Must be `Serialize +
/// Deserialize`: step results are journaled and fed back in on replay.
#[derive(Debug, Clone, Serialize, Deserialize)]
enum LlmResponse {
    /// "Call this tool with these arguments."
    ToolCall { tool: String, args: String },
    /// "I'm done; here is the answer."
    FinalAnswer(String),
}

/// The workflow's output: final answer, turns used, and the full transcript.
#[derive(Debug, Serialize, Deserialize)]
struct AgentRun {
    answer: String,
    turns: u32,
    transcript: Vec<String>,
}

// ---------------------------------------------------------------------------
// Mocks — swap these for a real LLM API + real tools
// ---------------------------------------------------------------------------

/// Mock LLM: decides purely from the turn number. A real one would receive
/// the task + transcript as its prompt (which is why they are passed in).
fn mock_llm(_task: &str, transcript: &[String], turn: u32) -> LlmResponse {
    match turn {
        0 => LlmResponse::ToolCall {
            tool: "search".to_string(),
            args: "sqrl durable execution".to_string(),
        },
        1 => LlmResponse::ToolCall {
            tool: "calculate".to_string(),
            args: "3 * 1447".to_string(),
        },
        _ => LlmResponse::FinalAnswer(format!(
            "3 * 1447 = 4341, and sqrl journals every step — this agent read {} transcript \
             entries and would survive a crash at any point.",
            transcript.len()
        )),
    }
}

/// Mock tool executor.
fn run_tool(tool: &str, args: &str) -> Result<String, String> {
    match tool {
        "search" => Ok(format!(
            "top result for `{args}`: \"sqrl — embedded durable execution for Rust\""
        )),
        "calculate" => Ok("4341".to_string()),
        other => Err(format!("unknown tool `{other}`")),
    }
}

// ---------------------------------------------------------------------------
// The workflow
// ---------------------------------------------------------------------------

#[sqrl::workflow(name = "agent-loop", version = 1)]
async fn agent_loop(ctx: &Ctx, task: String) -> sqrl::Result<AgentRun> {
    // The transcript lives in orchestration code and is therefore
    // deterministic: on replay it is reconstructed from journaled step
    // results, never from re-running the LLM or the tools.
    let mut transcript = vec![format!("user: {task}")];

    for turn in 0..MAX_TURNS {
        // One durable step per LLM call. Once this step's result is
        // journaled, a crash-and-restart replays the recorded response
        // instead of calling the LLM again.
        let task_c = task.clone();
        let transcript_c = transcript.clone();
        let response: LlmResponse = ctx
            .step(&format!("llm-call-{turn}"), move || {
                let task = task_c.clone();
                let transcript = transcript_c.clone();
                async move {
                    println!(
                        "  [llm-call-{turn}] calling LLM ({} messages)",
                        transcript.len()
                    );
                    Ok::<_, String>(mock_llm(&task, &transcript, turn))
                }
            })
            .await?;

        match response {
            LlmResponse::ToolCall { tool, args } => {
                transcript.push(format!("assistant: call {tool}({args})"));
                // Each tool call is its own durable step too: a crash after
                // the tool ran (but before the next LLM call) resumes here
                // with the journaled observation — the side effect is not
                // repeated.
                let tool_c = tool.clone();
                let args_c = args.clone();
                let observation: String = ctx
                    .step(&format!("tool-{tool}-{turn}"), move || {
                        let tool = tool_c.clone();
                        let args = args_c.clone();
                        async move {
                            println!("  [tool-{tool}-{turn}] executing {tool}({args})");
                            run_tool(&tool, &args)
                        }
                    })
                    .await?;
                transcript.push(format!("tool[{tool}]: {observation}"));
            }
            LlmResponse::FinalAnswer(answer) => {
                transcript.push(format!("assistant: {answer}"));
                return Ok(AgentRun {
                    answer,
                    turns: turn + 1,
                    transcript,
                });
            }
        }
    }
    Err(sqrl::Error::app(format!(
        "agent did not produce a final answer within {MAX_TURNS} turns"
    )))
}

// ---------------------------------------------------------------------------
// main
// ---------------------------------------------------------------------------

fn main() -> Result<(), Box<dyn std::error::Error>> {
    // WalStorage in a temp dir for realism (a real agent service would use a
    // stable path so in-flight agents survive restarts); removed at the end.
    let dir = std::env::temp_dir().join(format!("sqrl-agent-{}", std::process::id()));
    println!("=== sqrl ai_agent_loop: durable agent with mocked LLM ===");
    println!("data dir: {}", dir.display());

    let sqrl = Sqrl::builder()
        .storage(WalStorage::open(&dir)?)
        .register(agent_loop)
        .build()?;

    let task = "what is 3 * 1447, and what is sqrl?".to_string();
    println!("task: {task}\n");
    let handle = sqrl.start_blocking("agent-loop", &task)?;
    let run: AgentRun = handle.result_blocking()?;

    println!("\n--- transcript ({} turns) ---", run.turns);
    for line in &run.transcript {
        println!("  {line}");
    }
    println!("--- final answer ---");
    println!("  {}", run.answer);

    sqrl.shutdown();
    std::fs::remove_dir_all(&dir)?;
    println!("=== done (data dir removed) ===");
    Ok(())
}
