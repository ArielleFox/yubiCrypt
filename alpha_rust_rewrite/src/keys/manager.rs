use std::fs;
use crate::error::AppError;

pub fn print_current_identity() -> Result<(), AppError> {
    let home_dir = dirs::home_dir().ok_or_else(|| AppError::Other("Could not determine home directory".into()))?;
    let identity_path = home_dir.join(".config/yubi_crypt/identity.txt");

    if identity_path.exists() {
        let identity = fs::read_to_string(&identity_path)?;
        println!("🔐 Current Identity:\n{}", identity);
    } else {
        println!("⚠️ No identity found. Try running 'yubi_crypt import'");
    }

    Ok(())
}
