use anyhow::{Result, Context};
use std::fs::{self, File};
use std::io::Write;
use std::path::PathBuf;
use crate::identities::extract::extract_age_identities;

pub fn import_identities() -> Result<()> {
    let identities = extract_age_identities()?;

    let dir = dirs::home_dir()
    .context("Failed to resolve home directory")?
    .join(".yubiCrypt/keys");

    fs::create_dir_all(&dir).context("Failed to create keys directory")?;

    for (i, identity) in identities.iter().enumerate() {
        let file_path = dir.join(format!("identity_{}.txt", i + 1));
        let mut file = File::create(&file_path)?;
        writeln!(file, "Recipient: {}", identity)?;
        println!("✅ Imported identity to: {}", file_path.display());
    }

    Ok(())
}
