use anyhow::{Result, Context};
use std::{
    fs::{create_dir_all, OpenOptions},
    io::{BufRead, BufReader, Write},
    path::PathBuf,
    process::{Command, Stdio},
};

pub fn extract_age_identities() -> Result<Vec<String>> {
    let process = Command::new("age-plugin-yubikey")
    .arg("identities")
    .stdout(Stdio::piped())
    .spawn()
    .context("❌ Failed to start age-plugin-yubikey. Is it installed and in $PATH?")?;

    let stdout = process
    .stdout
    .context("❌ Failed to capture output from age-plugin-yubikey")?;
    let reader = BufReader::new(stdout);

    let mut identities = Vec::new();

    for line in reader.lines().flatten() {
        println!("🔍 Line: {}", line); // Optional: helpful for debugging

        if line.starts_with("age1") {
            println!("✅ Found identity: {}", line);
            identities.push(line);
        }
    }

    // Optional: Save found identities to a config file
    if !identities.is_empty() {
        let mut path = dirs::home_dir().unwrap_or_else(|| PathBuf::from("."));
        path.push(".config/yubi_crypt");

        create_dir_all(&path)
        .context("❌ Could not create config directory at ~/.config/yubi_crypt")?;

        path.push("identities.txt");

        let mut file = OpenOptions::new()
        .create(true)
        .append(true)
        .open(&path)
        .context("❌ Failed to open identities.txt for writing")?;

        for identity in &identities {
            writeln!(file, "{}", identity)?;
        }

        println!("💾 Saved {} identities to {}", identities.len(), path.display());
    }

    Ok(identities)
}
