use anyhow::{Result, Context};
use std::process::{Command, Stdio};
use std::io::{BufRead, BufReader};

pub fn extract_age_identities() -> Result<Vec<String>> {
    let output = Command::new("age-plugin-yubikey")
    .arg("identities")
    .stdout(Stdio::piped())
    .spawn()
    .context("Failed to start age-plugin-yubikey")?;

    let reader = BufReader::new(output.stdout.unwrap());
    let mut identities = Vec::new();

    for line in reader.lines().flatten() {
        if line.starts_with("age1") {
            identities.push(line);
        }
    }

    Ok(identities)
}
