use pcsc::{Context, Scope};
use std::ffi::CStr;

pub fn test_pcsc() -> Result<(), Box<dyn std::error::Error>> {
    let ctx = Context::establish(Scope::User)?;
    let mut readers_buf = [0; 2048];
    let readers = ctx.list_readers(&mut readers_buf)?;

    let reader_list: Vec<_> = readers.collect();

    if reader_list.is_empty() {
        println!("❌ No smartcard readers found.");
    } else {
        println!("📟 Smartcard readers found:");
        for reader in reader_list {
            let name = unsafe { CStr::from_ptr(reader.as_ptr()) };
            println!(" - {:?}", name);
        }
    }

    Ok(())
}
