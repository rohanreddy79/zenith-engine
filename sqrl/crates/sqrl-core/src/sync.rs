//! Minimal runtime-agnostic promise: the engine completes it, any executor
//! (Tokio, the simulator, a plain thread) can await or block on it.
//!
//! Deliberately hand-rolled instead of pulling in an async runtime: the
//! orchestration path must not depend on Tokio, and the simulator needs
//! wakers that behave deterministically.

use std::future::Future;
use std::pin::Pin;
use std::sync::{Arc, Condvar, Mutex};
use std::task::{Context, Poll, Waker};

struct Shared<T> {
    slot: Mutex<(Option<T>, Vec<Waker>)>,
    cv: Condvar,
}

/// Create a linked completer/waiter pair.
pub fn promise<T: Clone + Send>() -> (Completer<T>, Waiter<T>) {
    let shared = Arc::new(Shared {
        slot: Mutex::new((None, Vec::new())),
        cv: Condvar::new(),
    });
    (
        Completer {
            shared: Arc::clone(&shared),
        },
        Waiter { shared },
    )
}

/// The producing side; completing is idempotent (first value wins).
pub struct Completer<T: Clone + Send> {
    shared: Arc<Shared<T>>,
}

impl<T: Clone + Send> Completer<T> {
    /// Complete with `value` if not already completed. Returns whether this
    /// call won.
    pub fn complete(&self, value: T) -> bool {
        let mut guard = match self.shared.slot.lock() {
            Ok(g) => g,
            Err(poisoned) => poisoned.into_inner(),
        };
        if guard.0.is_some() {
            return false;
        }
        guard.0 = Some(value);
        let wakers = std::mem::take(&mut guard.1);
        drop(guard);
        self.shared.cv.notify_all();
        for w in wakers {
            w.wake();
        }
        true
    }
}

impl<T: Clone + Send> Clone for Completer<T> {
    fn clone(&self) -> Self {
        Completer {
            shared: Arc::clone(&self.shared),
        }
    }
}

/// The consuming side: a `Future` (runtime-agnostic) that also supports
/// blocking waits for synchronous callers.
pub struct Waiter<T: Clone + Send> {
    shared: Arc<Shared<T>>,
}

impl<T: Clone + Send> Clone for Waiter<T> {
    fn clone(&self) -> Self {
        Waiter {
            shared: Arc::clone(&self.shared),
        }
    }
}

impl<T: Clone + Send> Waiter<T> {
    /// The value, if already completed.
    pub fn peek(&self) -> Option<T> {
        match self.shared.slot.lock() {
            Ok(g) => g.0.clone(),
            Err(poisoned) => poisoned.into_inner().0.clone(),
        }
    }

    /// Block the current thread until completed. Never use from async code.
    pub fn wait_blocking(&self) -> T {
        let mut guard = match self.shared.slot.lock() {
            Ok(g) => g,
            Err(poisoned) => poisoned.into_inner(),
        };
        loop {
            if let Some(v) = &guard.0 {
                return v.clone();
            }
            guard = match self.shared.cv.wait(guard) {
                Ok(g) => g,
                Err(poisoned) => poisoned.into_inner(),
            };
        }
    }
}

impl<T: Clone + Send> Future for Waiter<T> {
    type Output = T;

    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<T> {
        let mut guard = match self.shared.slot.lock() {
            Ok(g) => g,
            Err(poisoned) => poisoned.into_inner(),
        };
        if let Some(v) = &guard.0 {
            return Poll::Ready(v.clone());
        }
        guard.1.push(cx.waker().clone());
        Poll::Pending
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn complete_then_wait() {
        let (c, w) = promise::<u32>();
        assert!(c.complete(7));
        assert!(!c.complete(9), "second completion must lose");
        assert_eq!(w.wait_blocking(), 7);
        assert_eq!(w.peek(), Some(7));
    }

    #[test]
    fn cross_thread() {
        let (c, w) = promise::<String>();
        let t = std::thread::spawn(move || w.wait_blocking());
        std::thread::spawn(move || c.complete("hi".to_string()));
        assert_eq!(t.join().unwrap(), "hi");
    }
}
