use std::fs::File;
use std::io::{Read, Write};
use std::process::{Command, Stdio};
use crate::error::AppError;

pub fn encrypt_file(input_path: &str) -> Result<(), AppError> {
    let mut input_file = File::open(input_path)?;
    let mut contents = Vec::new();
    input_file.read_to_end(&mut contents)?;

    let mut child = Command::new("age")
    .arg("-r")
    .arg("AGE_RECIPIENT_PLACEHOLDER") // Replace with actual recipient
    .stdin(Stdio::piped())
    .stdout(Stdio::piped())
    .stderr(Stdio::piped())
    .spawn()?;

    if let Some(mut stdin) = child.stdin.take() {
        stdin.write_all(&contents)?;
    }

    let output = child.wait_with_output()?;

    if !output.status.success() {
        return Err(AppError::Other("Encryption failed".into()));
    }

    let encrypted_path = format!("{}.age", input_path);
    let mut out_file = File::create(&encrypted_path)?;
    out_file.write_all(&output.stdout)?;

    println!("✅ Encrypted: {}", encrypted_path);
    Ok(())
}
