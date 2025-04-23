#!/usr/bin/env python3

from typing import Any
import os
from pathlib import Path
import getpass
import time
from contextlib import contextmanager
from typing import Generator, IO, Any
from datetime import datetime

@contextmanager
def timer() -> Generator[None, Any, None]:
    start_time: float = time.perf_counter()
    print(f'Started at: {datetime.now():%H:%M:%S}')
    try:
        yield
    finally:
        end_time: float = time.perf_counter()
        print(f'Ended at: {datetime.now():%H:%M:%S}')
        print(f'Time: {end_time - start_time:.4f}s')


@contextmanager
def file_manager(path: str, mode: str) -> Generator[IO, Any, None]:
    with timer():
        file: IO= open(path, mode)
        print('Opening file')
        try:
            yield file
        except Exection as e:
            print(e)
        finally:
            print('Closing file...')
            if file:
                file.close()


def add_aliases_to_bash_aliases():
    """
    Add aliases to the user's ~/.bash_aliases file.
    If the file does not exist, ask the user for permission to create it.
    """
    # Get the current user's home directory and username
    home_dir = Path.home()
    bash_aliases_file = home_dir / ".bash_aliases"
    username = getpass.getuser()

    # Define the aliases to add
    aliases = [
        "alias yubienCrypt='python3 ~/dcde/src/encrypt.py'",
        "alias yubideCrypt='python3 ~/dcde/src/decrypt.py'",
        "alias yubiCryptImport='python3 ~/.yubiCrypt/yubiCryptImporter/import.py'",
    ]

    try:
        # Check if the ~/.bash_aliases file exists
        if not bash_aliases_file.exists():
            print(f"🔍 The file '{bash_aliases_file}' does not exist.")
            # Ask the user for permission to create the file
            response = input(f"Would you like to create a new ~/.bash_aliases file for {username}? (y/n): ").strip().lower()
            if response != 'y':
                print("❌ Operation canceled. No changes were made.")
                return
            else:
                # Create the file
                print(f"📁 Creating the file '{bash_aliases_file}'...")
                bash_aliases_file.touch(mode=0o600)  # Create the file with secure permissions

        # Read the existing aliases in the file
        existing_aliases = set()
        if bash_aliases_file.exists():
            with file_manager(bash_aliases_file, "r") as f:
                existing_aliases = set(line.strip() for line in f if line.strip().startswith("alias"))

        # Add new aliases if they don't already exist
        with file_manager(bash_aliases_file, "a") as f:
            added_aliases = []
            for alias in aliases:
                if alias not in existing_aliases:
                    f.write(f"{alias}\n")
                    added_aliases.append(alias)

        # Provide feedback to the user
        if added_aliases:
            print(f"✅ Added the following aliases to '{bash_aliases_file}':")
            for alias in added_aliases:
                print(f"   {alias}")
        else:
            print(f"ℹ️ All specified aliases already exist in '{bash_aliases_file}'.")
        # Suggest reloading the shell
        print("\n💡 To apply the changes, run: source ~/.bash_aliases")
        return True

    except PermissionError:
        print(f"❌ Error: Permission denied while accessing '{bash_aliases_file}'.")
        return False
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
        return False
def main() -> bool:
    print('\n--------------------------------------------')
    print(__file__)
    print('--------------------------------------------\n')
    print("🔧 Adding aliases to your ~/.bash_aliases file...")
    add_aliases_to_bash_aliases()
    return True

if __name__ == "__main__":
    main()
