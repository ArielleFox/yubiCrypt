use clap::{Arg, Command};

pub fn build_cli() -> Command {
    Command::new("yubi_crypt")
    .about("Encrypt/Decrypt with YubiKey + AGE")
    .arg(
        Arg::new("list")
        .long("list")
        .help("Show current identity")
        .global(true)
        .num_args(0),
    )
    .subcommand_required(false)
    .subcommand(Command::new("encrypt").about("Encrypt a file").arg(Arg::new("file").required(true)))
    .subcommand(Command::new("decrypt").about("Decrypt a file").arg(Arg::new("file").required(true)))
    .subcommand(Command::new("import").about("Import identities from YubiKey"))
    .subcommand(Command::new("pcsc").about("Test PC/SC smartcard access"))
    .subcommand(Command::new("slots").about("List YubiKey slots"))
}
