#!/usr/bin/env python3
from typing import Any
import subprocess
import platform
import os
import sys

def check_age_installed():
    """Check if age is installed by trying to run 'age --version'"""
    try:
        subprocess.run(['age', '--version'], capture_output=True, text=True)
        return True
    except FileNotFoundError:
        return False

def install_age():
    """Install age based on the operating system"""
    system = platform.system().lower()

    if system == 'darwin':  # macOS
        try:
            print("Installing age using Homebrew...")
            subprocess.run(['brew', 'install', 'age'], check=True)
        except subprocess.CalledProcessError:
            print("Error: Failed to install age using Homebrew")
            print("Please make sure Homebrew is installed: https://brew.sh")
            sys.exit(1)

    elif system == 'linux':
        # Check for different package managers
        if os.path.exists('/usr/bin/apt'):  # Debian/Ubuntu
            try:
                print("Installing age using apt...")
                subprocess.run(['sudo', 'apt', 'update'], check=True)
                subprocess.run(['sudo', 'apt', 'install', 'age'], check=True)
            except subprocess.CalledProcessError:
                print("Error: Failed to install age using apt")
                sys.exit(1)

        elif os.path.exists('/usr/bin/dnf'):  # Fedora
            try:
                print("Installing age using dnf...")
                subprocess.run(['sudo', 'dnf', 'install', 'age'], check=True)
            except subprocess.CalledProcessError:
                print("Error: Failed to install age using dnf")
                sys.exit(1)

        elif os.path.exists('/usr/bin/pacman'):  # Arch Linux
            try:
                print("Installing age using pacman...")
                subprocess.run(['sudo', 'pacman', '-S', 'age'], check=True)
            except subprocess.CalledProcessError:
                print("Error: Failed to install age using pacman")
                sys.exit(1)
        else:
            print("Unsupported Linux distribution or package manager not found")
            print("Please install age manually: https://github.com/FiloSottile/age")
            sys.exit(1)

    elif system == 'windows':
        try:
            print("Installing age using Scoop...")
            # First check if Scoop is installed
            subprocess.run(['scoop', '--version'], check=True)
            subprocess.run(['scoop', 'install', 'age'], check=True)
        except FileNotFoundError:
            print("Error: Scoop is not installed")
            print("Please install Scoop first: https://scoop.sh")
            print("Or install age manually: https://github.com/FiloSottile/age")
            sys.exit(1)
        except subprocess.CalledProcessError:
            print("Error: Failed to install age using Scoop")
            sys.exit(1)
    else:
        print(f"Unsupported operating system: {system}")
        print("Please install age manually: https://github.com/FiloSottile/age")
        sys.exit(1)

def main() -> bool:
    print('\n--------------------------------------------')
    print(__file__)
    print('--------------------------------------------\n')

    if check_age_installed():
        print("age is already installed on your system!")
        return True
    else:
        print("age is not installed. Attempting to install...")
        install_age()

        # Verify installation
        if check_age_installed():
            print("age has been successfully installed!")
            return True
        else:
            print("Failed to verify age installation. Please install manually.")
            return False

if __name__ == "__main__":
    main()

# Created/Modified files during execution:
# No files are created or modified by this script
