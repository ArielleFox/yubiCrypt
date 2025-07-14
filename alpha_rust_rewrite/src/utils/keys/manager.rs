use std::fs;
use anyhow::{Result, anyhow};

pub fn print_current_identity() -> Result<()> {
    let identity_path = dirs::home_dir()
    .map(|p| p.join(".yubiCrypt/keys/first.txt"))
    .ok_or_else(|| anyhow!("Could not resolve home directory"))?;

    if !identity_path.exists() {
        println!("❌ No identity file found at: {}", identity_path.display());
        return Ok(());
    }

    let contents = fs::read_to_string(&identity_path)?;
    println!("# Current Identity: {}", identity_path.display());
    println!("{contents}");
    Ok(())
}
