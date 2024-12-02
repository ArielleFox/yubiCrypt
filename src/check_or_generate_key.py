#!/bin/env python3

import os
import subprocess

def check_or_generate_key():
    # Define the path to the key file
    key_dir = os.path.expanduser("~/.yubiCrypt/keys")
    key_file = os.path.join(key_dir, "first.txt")

    # Ensure the key directory exists
    if not os.path.exists(key_dir):
        os.makedirs(key_dir)
        print(f"Created directory: {key_dir}")

    # Check if the key file exists and is not empty
    if os.path.isfile(key_file) and os.path.getsize(key_file) > 0:
        print(f"Key file exists and is not empty: {key_file}")
        return

    # Generate a new key using age-plugin-yubikey
    print(f"Key file does not exist or is empty. Generating a new key: {key_file}")
    try:
        # Run the age-plugin-yubikey command to generate a new key
        command = ["age-plugin-yubikey", "generate", "-o", key_file]
        print(f"Running command: {' '.join(command)}")
        subprocess.run(command, check=True)
        print(f"Successfully generated a new key: {key_file}")
    except FileNotFoundError:
        print("Error: The 'age-plugin-yubikey' tool is not installed or not in your PATH.")
        print("Please install it from https://github.com/str4d/age-plugin-yubikey.")
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to generate the key. Command output:\n{e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    check_or_generate_key()
