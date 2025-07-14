// Stub for future support of YubiKey slots/enumeration
pub fn list_slots() -> Vec<String> {
    vec![
        String::from("slot 9a - Authentication"),
        String::from("slot 9c - Digital Signature"),
    ]
}
