mod cli;
mod encryption;
mod keys;
mod identities;
mod utils;
mod installer;
mod error;

use std::fs::{create_dir_all, OpenOptions};
use std::io::Write;
use std::path::Path;

use identities::get::import_identities;
use identities::extract::extract_age_identities;
use keys::slots::list_slots;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let matches = cli::build_cli().get_matches();

    if matches.get_flag("list") {
        keys::manager::print_current_identity()?;
        return Ok(());
    }

    match matches.subcommand() {
        Some(("encrypt", sub_m)) => {
            let file = sub_m.get_one::<String>("file").unwrap();
            encryption::encrypt::encrypt_file(file)?;
        }
        Some(("decrypt", sub_m)) => {
            let file = sub_m.get_one::<String>("file").unwrap();
            encryption::decrypt::decrypt_file(file)?;
        }
        Some(("import", _)) => {
            let ids = extract_age_identities()?;

            let config_path = dirs::config_dir()
            .unwrap_or_else(|| Path::new(".").to_path_buf())
            .join("yubi_crypt/identities.txt");

            if let Some(parent) = config_path.parent() {
                create_dir_all(parent)?;
            }

            let mut file = OpenOptions::new()
            .create(true)
            .append(true)
            .open(&config_path)?;

            for id in ids {
                println!("📥 Identity: {}", id);
                writeln!(file, "{}", id)?;
            }
        }
        Some(("slots", _)) => {
            let slots = list_slots();
            for slot in slots {
                println!("🔐 Slot: {}", slot);
            }
        }
        Some(("pcsc", _)) => {
            installer::pcsclite::test_pcsc()?;
        }
        _ => {
            println!("Use --help to see available commands.");
        }
    }

    Ok(())
}
