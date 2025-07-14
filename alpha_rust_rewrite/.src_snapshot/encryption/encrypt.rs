use std::fs::{self, File};
use std::io::{BufRead, BufReader};
use std::process::{Command, Stdio};
use std::thread;
use std::time::Duration;

use anyhow::{bail, Context, Result};

pub fn encrypt_file(input_file: &str) -> Result<()> {
    let identity_path = dirs::home_dir()
    .context("Could not resolve home directory")?
    .join(".yubiCrypt/keys/first.txt");

    if !identity_path.exists() {
        bail!("Missing identity file: {}", identity_path.display());
    }

    let recipient_key = extract_recipient_from_file(&identity_path)
    .context("Failed to extract recipient key from identity")?;

    let output_file = format!("{}.age", input_file);

    println!("🔒 Starting encryption...");
    println!("📁 Input:  {input_file}");
    println!("📎 Output: {output_file}");
    println!("🔑 Using recipient: {recipient_key}");

    let mut child = Command::new("age")
    .args(&["-r", &recipient_key, "-o", &output_file, input_file])
    .stdout(Stdio::piped())
    .stderr(Stdio::piped())
    .spawn()
    .context("Failed to start `age` command")?;

    thread::spawn(|| {
        thread::sleep(Duration::from_secs(2));
        println!("⌛ If nothing happens, please touch your YubiKey...");
    });

    if let Some(stderr) = &mut child.stderr {
        let reader = BufReader::new(stderr.try_clone()?);
        thread::spawn(move || {
            for line in reader.lines().flatten() {
                if line.to_lowercase().contains("touch") {
                    println!("👆 Please touch your YubiKey...");
                } else {
                    eprintln!("⚠️ age: {}", line);
                }
            }
        });
    }

    let status = child.wait().context("Failed to wait for `age` process")?;

    if status.success() {
        println!("✅ Successfully encrypted: {output_file}");
        fs::remove_file(input_file).context("Failed to delete original file after encryption")?;
    } else {
        bail!("❌ Encryption failed with exit code: {}", status);
    }

    Ok(())
}

fn extract_recipient_from_file(path: &std::path::Path) -> Result<String> {
    let file = File::open(path).context("Failed to open identity file")?;
    let reader = BufReader::new(file);

    for line in reader.lines().flatten() {
        if line.trim_start().starts_with("Recipient:") {
            return Ok(line["Recipient:".len()..].trim().to_string());
        }
    }

    bail!("No Recipient line found in identity file: {}", path.display());
}
