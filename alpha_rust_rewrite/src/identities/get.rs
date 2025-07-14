use std::process::Command;
use std::fs::{self, OpenOptions};
use std::io::{Write, BufWriter};
use std::path::PathBuf;

use crate::error::AppError;

pub fn import_identities() -> Result<(), AppError> {
    println!("📥 Importing identities from YubiKey...");

    let output = Command::new("age-plugin-yubikey").output()?;

    if !output.status.success() {
        return Err(AppError::Other(format!(
            "age-plugin-yubikey failed: {}",
            String::from_utf8_lossy(&output.stderr)
        )));
    }

    let stdout = String::from_utf8_lossy(&output.stdout);

    // Prepare config directory
    let config_dir = dirs::config_dir()
    .unwrap_or_else(|| PathBuf::from("."))
    .join("yubi_crypt");

    fs::create_dir_all(&config_dir)?;

    let identities_path = config_dir.join("identities.txt");
    let file = OpenOptions::new()
    .create(true)
    .append(true)
    .open(&identities_path)?;

    let mut writer = BufWriter::new(file);
    let mut found = false;

    for line in stdout.lines() {
        if line.contains("AGE-PLUGIN-YUBIKEY-") {
            writeln!(writer, "{}", line)?;
            println!("🔐 Found and saved identity: {}", line);
            found = true;
        }
    }

    if !found {
        println!("⚠️ No YubiKey identities found.");
    } else {
        println!("✅ Identities saved to {}", identities_path.display());
    }

    Ok(())
}
