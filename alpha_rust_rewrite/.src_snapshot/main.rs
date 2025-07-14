mod cli;
mod encryption;
mod keys;
mod identities;
mod utils;
mod installer;
mod error;

use identities::get::import_identities;

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
            import_identities()?;
        }
        _ => {
            println!("Use --help to see available commands.");
        }
    }

    Ok(())
}
