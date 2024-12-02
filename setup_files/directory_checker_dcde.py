#!/usr/bin/env python3

import os
from pathlib import Path
import stat
import sys
from typing import Any

def check_and_create_directory():
    """
    Check if ~/dcde/src/ exists, and if not, create it with secure permissions.
    """
    # Define the target directory
    target_dir = Path.home() / "dcde" / "src"

    try:
        # Check if the directory exists
        if target_dir.exists():
            print(f"📁 Directory already exists: {target_dir}")
        else:
            # Create the directory with parents if it doesn't exist
            print(f"📁 Creating directory: {target_dir}")
            target_dir.mkdir(parents=True, mode=0o700)  # 700 permissions (owner only)

            # Set secure permissions explicitly
            os.chmod(target_dir, stat.S_IRWXU)  # 700 permissions

            print(f"✅ Successfully created directory: {target_dir}")

        # Verify permissions
        current_mode = os.stat(target_dir).st_mode
        if not (current_mode & stat.S_IRWXU == stat.S_IRWXU):
            print(f"⚠️  Warning: Directory permissions are not secure for {target_dir}")
        else:
            print(f"🔒 Directory permissions are secure (700): {target_dir}")

    except PermissionError:
        print(f"❌ Error: Permission denied while accessing or creating {target_dir}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    print('\n--------------------------------------------')
    print(__file__)
    print('--------------------------------------------\n')
    print("🔍 Checking ~/dcde/src/ directory...")
    check_and_create_directory()
    return True

if __name__ == "__main__":
    main()
