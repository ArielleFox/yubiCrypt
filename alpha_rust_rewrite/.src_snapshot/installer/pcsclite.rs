// installer/pcsclite.rs
// Check if pcsc-lite is installed (Linux/macOS)
pub fn check_pcsc_installed() -> bool {
    which::which("pcsc_scan").is_ok()
}
