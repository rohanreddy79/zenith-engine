//! Real-filesystem `StdVfs` coverage: the file/namespace operations and the
//! error paths a healthy run never touches.

use sqrl_core::vfs::{Vfs, VfsError};
use sqrl_store::StdVfs;

#[test]
fn file_ops_roundtrip() {
    let dir = tempfile::tempdir().unwrap();
    let vfs = StdVfs::new(dir.path()).unwrap();
    vfs.create_dir_all("sub").unwrap();
    let mut f = vfs.open("sub/a.bin", true).unwrap();
    f.write_at(0, b"hello world").unwrap();
    f.write_at(6, b"there").unwrap();
    f.sync().unwrap();
    assert_eq!(f.len().unwrap(), 11);
    let mut buf = [0u8; 32];
    let n = f.read_at(0, &mut buf).unwrap();
    assert_eq!(&buf[..n], b"hello there");
    // Short read at the tail, empty read past the end.
    let n = f.read_at(9, &mut buf).unwrap();
    assert_eq!(&buf[..n], b"re");
    assert_eq!(f.read_at(100, &mut buf).unwrap(), 0);
    f.truncate(5).unwrap();
    f.sync().unwrap();
    assert_eq!(f.len().unwrap(), 5);
    vfs.sync_dir("sub").unwrap();
    assert!(vfs.exists("sub/a.bin").unwrap());
    assert_eq!(vfs.list("sub").unwrap(), vec!["a.bin".to_string()]);
}

#[test]
fn namespace_ops_and_errors() {
    let dir = tempfile::tempdir().unwrap();
    let vfs = StdVfs::new(dir.path()).unwrap();
    // Open without create on a missing file: NotFound.
    assert!(matches!(
        vfs.open("missing.bin", false),
        Err(VfsError::NotFound(_))
    ));
    assert!(!vfs.exists("missing.bin").unwrap());
    // Rename with overwrite.
    let mut f = vfs.open("x.tmp", true).unwrap();
    f.write_at(0, b"new").unwrap();
    f.sync().unwrap();
    drop(f);
    let mut old = vfs.open("x", true).unwrap();
    old.write_at(0, b"old-old").unwrap();
    old.sync().unwrap();
    drop(old);
    vfs.rename("x.tmp", "x").unwrap();
    vfs.sync_dir("").unwrap();
    let mut f = vfs.open("x", false).unwrap();
    assert_eq!(f.len().unwrap(), 3);
    drop(f);
    vfs.delete("x").unwrap();
    assert!(!vfs.exists("x").unwrap());
    // Deleting a missing file errors (callers treat it as best-effort).
    assert!(vfs.delete("x").is_err());
    // Path escape attempts are rejected, not resolved.
    assert!(vfs.open("../escape", true).is_err());
}
