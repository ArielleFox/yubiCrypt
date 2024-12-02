#!/usr/bin/env python3

import os
from pathlib import Path
import sys

def check_yubikey_files() -> bool:
    """
    Check for .txt files in ~/.yubiCrypt/keys/
    Returns: True if .txt files are found, False otherwise
    """
    try:
        # Get the keys directory path
        keys_dir = Path.home() / '.yubiCrypt' / 'keys'

        # Check if the directory exists
        if not keys_dir.exists():
            print(f"📁 Creating directory: {keys_dir}")
            keys_dir.mkdir(parents=True, mode=0o700)
            return False

        # List all .txt files in the directory
        txt_files = list(keys_dir.glob('*.txt'))

        # Check if any .txt files were found
        if txt_files:
            print("🔑 Keys detected:")
            print("═" * 40)
            for file in sorted(txt_files):
                # Get file stats
                stats = file.stat()
                size = stats.st_size

                # Format size nicely
                if size < 1024:
                    size_str = f"{size} bytes"
                else:
                    size_str = f"{size/1024:.1f} KB"

                # Print file info with size
                print(f"📄 {file.name} ({size_str})")

            print("═" * 40)
            print(f"Total keys found: {len(txt_files)}")
            return True
        else:
            print("\n⚠️  No keys detected in ~/.yubiCrypt/keys/")
            return False

    except PermissionError:
        print(f"❌ Error: No permission to access {keys_dir}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"❌ Error checking keys: {e}", file=sys.stderr)
        return False

def main():
    """Main function to run the key check"""
    print("🔍 Checking for YubiKey files...")

    # Get the keys directory path
    keys_dir = Path.home() / '.yubiCrypt' / 'keys'
    print(f"📁 Directory: {keys_dir}")

    # Run the check
    if check_yubikey_files():
        # Additional information if keys are found
        try:
            total_size = sum((f.stat().st_size for f in keys_dir.glob('*.txt')))
            if total_size < 1024:
                size_str = f"{total_size} bytes"
            else:
                size_str = f"{total_size/1024:.1f} KB"
            print(f"📊 Total size: {size_str}")
        except Exception as e:
            print(f"⚠️  Could not calculate total size: {e}", file=sys.stderr)
    else:
        print("💡 To add keys:")
        print("1. Create a new key file in ~/.yubiCrypt/keys/")
        print("2. Ensure it has a .txt extension")
        print("3. Set proper file permissions (600)")

if __name__ == "__main__":
    main()

# Created/Modified files during execution:
# - ~/.yubiCrypt/keys/ (directory, if it doesn't exist)
