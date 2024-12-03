#!/usr/bin/env python3

import os
import sys
import stat
from pathlib import Path
import pwd
import grp
import platform
from typing import Any

def get_user_info():
    """Get current user information"""
    return pwd.getpwuid(os.getuid())

def create_yubicrypt_dir():
    """Create and configure the ~/.yubiCrypt directory"""
    # Get user's home directory
    home_dir = Path.home()
    yubicrypt_dir = home_dir / '.yubiCrypt' / 'keys'

    # Check if directory already exists
    if yubicrypt_dir.exists():
        print(f"Directory {yubicrypt_dir} already exists.")

        # Verify permissions
        current_mode = os.stat(yubicrypt_dir).st_mode
        if not (current_mode & stat.S_IRWXU == stat.S_IRWXU):
            print("Fixing directory permissions...")
            os.chmod(yubicrypt_dir, stat.S_IRWXU)

        return True

    try:
        # Create directory with proper permissions (700 - only owner can read/write/execute)
        yubicrypt_dir.mkdir(mode=stat.S_IRWXU)

        # Get user information
        user_info = get_user_info()

        # Set ownership to current user
        os.chown(yubicrypt_dir, user_info.pw_uid, user_info.pw_gid)

        print(f"Successfully created {yubicrypt_dir} with secure permissions.")

        # Create a README file in the directory
        readme_path = yubicrypt_dir / 'README.md'
        readme_content = """# YubiCrypt Directory

This directory is used for storing encrypted files using age with YubiKey.
Please ensure:
- Keep your YubiKey safe
- Backup your recovery codes
- Don't share the contents of this directory
- Maintain secure permissions (700) on this directory

For more information, visit:
https://github.com/str4d/age-plugin-yubikey
"""

        with open(readme_path, 'w') as f:
            f.write(readme_content)

        # Set README permissions to 600 (owner read/write only)
        os.chmod(readme_path, stat.S_IRUSR | stat.S_IWUSR)

        return True

    except Exception as e:
        print(f"Error creating directory: {e}", file=sys.stderr)
        return False

def verify_directory_permissions():
    """Verify the permissions of the ~/.yubiCrypt directory"""
    yubicrypt_dir = Path.home() / '.yubiCrypt'

    if not yubicrypt_dir.exists():
        return False

    # Check directory permissions
    mode = os.stat(yubicrypt_dir).st_mode
    owner_uid = os.stat(yubicrypt_dir).st_uid

    # Verify owner is current user
    current_uid = os.getuid()
    if owner_uid != current_uid:
        print("Warning: Directory is owned by another user!")
        return False

    # Verify permissions are 700
    if not (mode & stat.S_IRWXU == stat.S_IRWXU):
        print("Warning: Directory permissions are not secure!")
        return False

    return True

def main() -> bool:
    print('\n--------------------------------------------')
    print(__file__)
    print('--------------------------------------------\n')
    print("Checking YubiCrypt directory...")

    # Create directory if it doesn't exist
    if create_yubicrypt_dir():
        # Verify permissions
        if verify_directory_permissions():
            print("YubiCrypt directory is properly configured.")
        else:
            print("Warning: YubiCrypt directory permissions need attention!")
            return False
            sys.exit(1)
    else:
        print("Failed to configure YubiCrypt directory!")
        sys.exit(1)

    # Print directory information
    yubicrypt_dir = Path.home() / '.yubiCrypt'
    print("Directory Information:")
    print(f"Location: {yubicrypt_dir}")
    print(f"Owner: {pwd.getpwuid(os.stat(yubicrypt_dir).st_uid).pw_name}")
    print(f"Permissions: {oct(os.stat(yubicrypt_dir).st_mode)[-3:]}")
    return True

if __name__ == "__main__":
    main()

# Created/Modified files during execution:
# - ~/.yubiCrypt/ (directory)
# - ~/.yubiCrypt/README.md
