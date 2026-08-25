//! Workflow registration: stable name + version → type-erased factory.

use crate::codec;
use crate::ctx::Ctx;
use crate::error::Error;
use serde::{de::DeserializeOwned, Serialize};
use std::collections::BTreeMap;
use std::future::Future;
use std::pin::Pin;
use std::sync::Arc;

/// A type-erased workflow future. Deliberately **not** `Send`: orchestration
/// runs on exactly one logical thread of control per workflow.
pub type WorkflowFut = Pin<Box<dyn Future<Output = Result<Vec<u8>, Error>> + 'static>>;

/// A type-erased workflow factory: `(ctx, serialized input) → future`.
pub type WorkflowFactory = Arc<dyn Fn(Ctx, Vec<u8>) -> WorkflowFut + Send + Sync + 'static>;

/// A registered workflow definition.
#[derive(Clone)]
pub struct WorkflowDef {
    /// Stable registered name.
    pub name: String,
    /// Version (journaled at start; see `docs/versioning-and-patching.md`).
    pub version: u32,
    /// Factory producing the orchestration future.
    pub factory: WorkflowFactory,
}

/// The set of registered workflows an engine serves.
#[derive(Clone, Default)]
pub struct Registry {
    defs: BTreeMap<String, WorkflowDef>,
}

impl Registry {
    /// Empty registry.
    pub fn new() -> Self {
        Registry::default()
    }

    /// Register a typed workflow function.
    ///
    /// ```
    /// use sqrl_core::{Ctx, Error, Registry};
    /// let mut reg = Registry::new();
    /// reg.register("double", 1, |_ctx: Ctx, x: u64| async move { Ok::<_, Error>(x * 2) });
    /// assert!(reg.get("double").is_some());
    /// ```
    pub fn register<I, O, F, Fut>(&mut self, name: &str, version: u32, f: F) -> &mut Self
    where
        I: DeserializeOwned + 'static,
        O: Serialize + 'static,
        F: Fn(Ctx, I) -> Fut + Send + Sync + 'static,
        Fut: Future<Output = Result<O, Error>> + 'static,
    {
        let f = Arc::new(f);
        let factory: WorkflowFactory = Arc::new(move |ctx: Ctx, input: Vec<u8>| {
            let f = Arc::clone(&f);
            Box::pin(async move {
                let max_payload = ctx.cell.borrow().max_payload;
                let input: I = codec::from_slice(&input, "workflow input")?;
                let out = f(ctx, input).await?;
                codec::to_vec_limited(&out, max_payload, "workflow output")
            }) as WorkflowFut
        });
        self.register_def(WorkflowDef {
            name: name.to_string(),
            version,
            factory,
        })
    }

    /// Register a pre-built (possibly macro-generated) definition.
    pub fn register_def(&mut self, def: WorkflowDef) -> &mut Self {
        self.defs.insert(def.name.clone(), def);
        self
    }

    /// Look up a definition by name.
    pub fn get(&self, name: &str) -> Option<&WorkflowDef> {
        self.defs.get(name)
    }

    /// Registered names, sorted.
    pub fn names(&self) -> Vec<&str> {
        self.defs.keys().map(|s| s.as_str()).collect()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn register_and_lookup() {
        let mut reg = Registry::new();
        reg.register("wf", 3, |_ctx: Ctx, x: u32| async move {
            Ok::<u32, Error>(x + 1)
        });
        let def = reg.get("wf").expect("registered");
        assert_eq!(def.version, 3);
        assert_eq!(reg.names(), vec!["wf"]);
        assert!(reg.get("nope").is_none());
    }
}
