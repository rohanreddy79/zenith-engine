//! Payload serialization.
//!
//! All user-visible payloads (workflow inputs/outputs, step results, signal
//! payloads) and all engine records are encoded as **self-describing
//! MessagePack** (`rmp-serde` in named mode: struct fields and enum variants
//! are encoded by name, not index). Combined with the per-record
//! `format_version` byte in the WAL envelope this gives forward-compatible,
//! inspectable on-disk data. See ADR 0004 and `docs/on-disk-format.md`.

use crate::error::Error;
use serde::{de::DeserializeOwned, Serialize};

/// Version of the *logical record encoding* (the MessagePack schema of
/// journal events and snapshots). Stored in every WAL record envelope.
/// Bump on any change to event/snapshot serialization; readers must reject
/// versions they do not understand. See `docs/on-disk-format.md`.
pub const SQRL_FORMAT_VERSION: u8 = 1;

/// Default maximum serialized payload size (1 MiB). Larger payloads are
/// rejected with [`Error::PayloadTooLarge`]; store blobs externally and
/// journal a reference instead.
pub const DEFAULT_MAX_PAYLOAD: usize = 1024 * 1024;

/// Serialize a value as self-describing MessagePack.
pub fn to_vec<T: Serialize + ?Sized>(value: &T, context: &str) -> Result<Vec<u8>, Error> {
    rmp_serde::encode::to_vec_named(value).map_err(|e| Error::Codec {
        context: context.to_string(),
        message: e.to_string(),
    })
}

/// Serialize with a size limit.
pub fn to_vec_limited<T: Serialize + ?Sized>(
    value: &T,
    limit: usize,
    context: &str,
) -> Result<Vec<u8>, Error> {
    let bytes = to_vec(value, context)?;
    if bytes.len() > limit {
        return Err(Error::PayloadTooLarge {
            size: bytes.len(),
            limit,
            context: context.to_string(),
        });
    }
    Ok(bytes)
}

/// Deserialize a value from self-describing MessagePack.
pub fn from_slice<T: DeserializeOwned>(bytes: &[u8], context: &str) -> Result<T, Error> {
    rmp_serde::decode::from_slice(bytes).map_err(|e| Error::Codec {
        context: context.to_string(),
        message: e.to_string(),
    })
}

#[cfg(test)]
mod tests {
    use super::*;
    use serde::Deserialize;

    #[derive(Debug, PartialEq, Serialize, Deserialize)]
    struct V1 {
        a: u32,
        b: String,
    }

    // Same data with fields reordered and one added: named encoding must
    // tolerate reordering, and default-able additions.
    #[derive(Debug, PartialEq, Serialize, Deserialize)]
    struct V2 {
        b: String,
        #[serde(default)]
        c: Option<u64>,
        a: u32,
    }

    #[test]
    fn round_trip() {
        let v = V1 {
            a: 7,
            b: "x".into(),
        };
        let bytes = to_vec(&v, "test").unwrap();
        let back: V1 = from_slice(&bytes, "test").unwrap();
        assert_eq!(v, back);
    }

    #[test]
    fn named_encoding_survives_field_reorder_and_addition() {
        let v = V1 {
            a: 7,
            b: "x".into(),
        };
        let bytes = to_vec(&v, "test").unwrap();
        let evolved: V2 = from_slice(&bytes, "test").unwrap();
        assert_eq!(
            evolved,
            V2 {
                b: "x".into(),
                c: None,
                a: 7
            }
        );
    }

    #[test]
    fn size_limit_enforced() {
        let big = vec![0u8; 100];
        let err = to_vec_limited(&big, 10, "step result").unwrap_err();
        match err {
            Error::PayloadTooLarge { limit: 10, .. } => {}
            other => panic!("expected PayloadTooLarge, got {other:?}"),
        }
    }
}
