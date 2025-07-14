use std::fs;
use std::path::Path;

pub fn file_exists(path: &Path) -> bool {
    path.exists()
}

pub fn remove_if_exists(path: &Path) {
    if path.exists() {
        let _ = fs::remove_file(path);
    }
}
