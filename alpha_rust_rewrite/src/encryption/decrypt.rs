use std::fs::File;
use std::io::{Read, Write};
use std::process::{Command, Stdio};
use crate::error::AppError;

pub fn decrypt_file(input_path: &str) -> Result<(), AppError> {
    let mut input_file = File::open(input_path)?;
    let mut contents = Vec::new();
    input_file.read_to_end(&mut contents)?;

    let mut child = Command::new("age")
    .arg("-d")
    .stdin(Stdio::piped())
    .stdout(Stdio::piped())
    .stderr(Stdio::piped())
    .spawn()?;

    if let Some(mut stdin) = child.stdin.take() {
        stdin.write_all(&contents)?;
    }

    let output = child.wait_with_output()?;

    if !output.status.success() {
        return Err(AppError::Other("Decryption failed".into()));
    }

    let decrypted_path = input_path.trim_end_matches(".age");
    let mut out_file = File::create(&decrypted_path)?;
    out_file.write_all(&output.stdout)?;

    println!("🔓 Decrypted: {}", decrypted_path);
    Ok(())
}
