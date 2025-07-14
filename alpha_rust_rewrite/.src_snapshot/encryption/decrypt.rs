use std::fs;
use std::io::{BufRead, BufReader};
use std::process::{Command, Stdio};
use std::thread;
use std::time::Duration;

use anyhow::{bail, Context, Result};

pub fn decrypt_file(input_file: &str) -> Result<()> {
    let identity_path = dirs::home_dir()
    .context("Could not locate home directory")?
    .join(".yubiCrypt/keys/first.txt");

    if !identity_path.exists() {
        bail!("Missing identity file: {}", identity_path.display());
    }

    if !input_file.ends_with(".age") {
        bail!("Input file does not have .age extension: {input_file}");
    }

    let output_file = input_file.strip_suffix(".age").unwrap_or(input_file);

    println!("🔐 Starting decryption...");
    println!("📎 Input: {input_file}");
    println!("📁 Output: {output_file}");

    let mut child = Command::new("age")
    .args(&["-d", "-i"])
    .arg(&identity_path)
    .arg("-o")
    .arg(output_file)
    .arg(input_file)
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

    let status = child.wait().context("Failed to wait on `age` process")?;

    if status.success() {
        println!("✅ Successfully decrypted: {output_file}");
        fs::remove_file(input_file).context("Failed to remove encrypted file")?;
    } else {
        bail!("❌ Decryption failed with exit code: {}", status);
    }

    Ok(())
}
