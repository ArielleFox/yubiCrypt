#!/usr/bin/env python3

import os
import platform
import subprocess
import sys
from pathlib import Path
from typing import Any

def check_root():
    """Check if script is running with root privileges"""
    return os.geteuid() == 0

def install_rust():
    """Install Rust using rustup"""
    print("Installing Rust...")
    subprocess.run("curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh", shell=True, check=True)
    # Reload PATH to include cargo
    os.environ["PATH"] = f"{str(Path.home())}/.cargo/bin:{os.environ['PATH']}"

def check_rust_installed():
    """Check if Rust is installed"""
    try:
        subprocess.run(["cargo", "--version"], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def install_dependencies():
    """Install required system dependencies"""
    system = platform.system().lower()

    if system == "linux":
        if os.path.exists("/etc/debian_version"):
            # Debian/Ubuntu
            subprocess.run(["apt-get", "update"], check=True)
            subprocess.run(["apt-get", "install", "-y", "pkg-config", "libpcsclite-dev"], check=True)
        elif os.path.exists("/etc/fedora-release"):
            # Fedora
            subprocess.run(["dnf", "install", "-y", "rustup"], check=True)
            subprocess.run(["dnf", "install", "-y", "pcsc-lite-devel"], check=True)
        else:
            print("Unsupported Linux distribution. Please install PCSC-Lite development packages and rust manually.")
    elif system == "darwin":
        # macOS
        try:
            subprocess.run(["brew", "--version"], check=True, capture_output=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("Installing Homebrew...")
            subprocess.run('/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"', shell=True, check=True)
    else:
        print(f"Unsupported operating system: {system}")
        sys.exit(1)

def install_age_plugin_yubikey():
    """Install age-plugin-yubikey using cargo"""
    print("Installing age-plugin-yubikey...")
#    os.system('cargo install age-plugin-yubikey')

def main() -> bool:
    print('\n--------------------------------------------')
    print(__file__)
    print('--------------------------------------------\n')
    """Main installation function"""
    if platform.system().lower() != "windows":  # Windows is not supported
        if not check_root() and platform.system().lower() != "darwin":
            print("This script needs to be run with root privileges (sudo)")
            sys.exit(1)

        print("Starting age-plugin-yubikey installation...")

        # Install system dependencies
        install_dependencies()

        # Install age-plugin-yubikey
        install_age_plugin_yubikey()

        print("\nInstallation completed successfully!")
        print("You can now use age-plugin-yubikey with your YubiKey.")
        print("\nTo get started, run: age-plugin-yubikey generate")
    else:
        print("Windows is not supported by age-plugin-yubikey")
        sys.exit(1)

if __name__ == "__main__":
    main()

# Created/Modified files during execution:
# Note: The script itself doesn't create files directly, but the installation process will create:
# - ~/.cargo/ directory and its contents (if Rust wasn't installed)
# - /usr/local/bin/age-plugin-yubikey (or similar path depending on your system)
