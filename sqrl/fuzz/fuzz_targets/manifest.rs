//! Fuzz the manifest/meta parser via a SimDisk file: arbitrary contents must
//! either parse or degrade cleanly (None), never panic, never error the
//! recovery path.
#![no_main]
use libfuzzer_sys::fuzz_target;
use sqrl_core::vfs::Vfs;
use sqrl_sim::SimDisk;

fuzz_target!(|data: &[u8]| {
    let disk = SimDisk::new(1);
    {
        let mut f = disk.open("shard-0/MANIFEST", true).unwrap();
        f.write_at(0, data).unwrap();
        f.sync().unwrap();
    }
    disk.sync_dir("shard-0").unwrap();
    // Corrupt/garbled manifests must degrade to None (directory-scan
    // fallback), never Err, never panic.
    let m = sqrl_store::manifest::read_manifest(&disk, "shard-0").expect("never hard-errors");
    let _ = m;
    let meta = sqrl_store::manifest::read_meta(&disk, "shard-0");
    let _ = meta; // meta may Err(Corrupt) — that is a defined outcome — but must not panic
});
