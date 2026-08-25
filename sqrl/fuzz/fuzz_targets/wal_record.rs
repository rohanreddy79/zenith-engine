//! Fuzz the WAL record decoder: arbitrary bytes must never panic, never
//! over-read, and scanning must terminate. Valid records must round-trip.
#![no_main]
use libfuzzer_sys::fuzz_target;

fuzz_target!(|data: &[u8]| {
    // Decoding arbitrary bytes: must return, never panic.
    let _ = sqrl_store::codec::decode_one(data, 0);
    let (records, _end) = sqrl_store::codec::scan(data);
    // Anything that decoded must re-encode and decode back identically.
    for (_, rec) in records {
        let bytes = sqrl_store::codec::encode(&rec).expect("re-encode");
        let (back, consumed) = sqrl_store::codec::decode_one(&bytes, 0)
            .expect("decode of own encoding")
            .expect("non-empty");
        assert_eq!(back, rec, "round-trip mismatch");
        assert_eq!(consumed, bytes.len());
    }
});
