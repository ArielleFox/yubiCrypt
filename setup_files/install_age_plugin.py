#!/usr/bin/env python3

import subprocess
import platform
import os
import sys
import requests
import tarfile
import zipfile
from pathlib import Path
import shutil

def check_command_exists(command):
    """Check if a command exists by trying to run it"""
    try:
        subprocess.run([command, '--version'], capture_output=True, text=True)
        return True
    except FileNotFoundError:
        return False

def get_latest_release_info():
    """Get the latest release information from GitHub API"""
    api_url = "https://api.github.com/repos/str4d/age-plugin-yubikey/releases/latest"
    response = requests.get(api_url)
    if response.status_code != 200:
        print("Failed to fetch release information from GitHub")
        sys.exit(1)
    return response.json()

def download_file(url, filename):
    """Download a file from URL"""
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
    return False

def install_age_plugin_yubikey():
    """Install age-plugin-yubikey based on the operating system"""
    system = platform.system().lower()
    machine = platform.machine().lower()

    # Get the latest release info
    release_info = get_latest_release_info()

    if system == 'darwin':  # macOS
        try:
            print("Installing age-plugin-yubikey using Homebrew...")
            subprocess.run(['brew', 'install', 'age-plugin-yubikey'], check=True)
        except subprocess.CalledProcessError:
            print("Error: Failed to install age-plugin-yubikey using Homebrew")
            print("Attempting manual installation...")
            install_from_github(system, machine, release_info)

    elif system == 'linux':
        if os.path.exists('/usr/bin/apt'):  # Debian/Ubuntu
            try:
                print("Installing age-plugin-yubikey using apt...")
                # Add repository if needed
                # Note: As of now, age-plugin-yubikey might not be in standard repositories
                # Falling back to manual installation
                install_from_github(system, machine, release_info)
            except subprocess.CalledProcessError:
                print("Error: Failed to install using apt")
                install_from_github(system, machine, release_info)

        elif os.path.exists('/usr/bin/dnf'):  # Fedora
            try:
                print("Installing age-plugin-yubikey using dnf...")
                # Note: As of now, age-plugin-yubikey might not be in standard repositories
                # Falling back to manual installation
                install_from_github(system, machine, release_info)
            except subprocess.CalledProcessError:
                print("Error: Failed to install using dnf")
                install_from_github(system, machine, release_info)

        else:
            print("No package manager found, installing from GitHub...")
            install_from_github(system, machine, release_info)

    elif system == 'windows':
        try:
            print("Installing age-plugin-yubikey using Scoop...")
            subprocess.run(['scoop', 'install', 'age-plugin-yubikey'], check=True)
        except (FileNotFoundError, subprocess.CalledProcessError):
            print("Error: Failed to install using Scoop")
            install_from_github(system, machine, release_info)
    else:
        print(f"Unsupported operating system: {system}")
        sys.exit(1)

def install_from_github(system, machine, release_info):
    """Install age-plugin-yubikey from GitHub releases"""
    # Create temporary directory
    temp_dir = Path("./age-plugin-yubikey-temp")
    temp_dir.mkdir(exist_ok=True)

    try:
        # Determine correct asset to download
        arch_map = {
            'x86_64': 'x86_64',
            'amd64': 'x86_64',
            'arm64': 'arm64',
            'aarch64': 'arm64'
        }

        system_map = {
            'linux': 'linux',
            'darwin': 'darwin',
            'windows': 'windows'
        }

        arch = arch_map.get(machine, machine)
        sys_name = system_map.get(system)

        if not sys_name:
            print(f"Unsupported system: {system}")
            return False

        # Find matching asset
        asset = None
        for a in release_info['assets']:
            name = a['name'].lower()
            if sys_name in name and arch in name:
                asset = a
                break

        if not asset:
            print("Could not find matching release for your system")
            return False

        # Download the asset
        download_path = temp_dir / asset['name']
        print(f"Downloading {asset['name']}...")
        if not download_file(asset['browser_download_url'], download_path):
            print("Failed to download release")
            return False

        # Extract and install
        if system == 'windows':
            install_dir = Path(os.environ.get('USERPROFILE', '')) / '.age' / 'plugins'
        else:
            install_dir = Path.home() / '.age' / 'plugins'

        install_dir.mkdir(parents=True, exist_ok=True)

        if asset['name'].endswith('.tar.gz'):
            with tarfile.open(download_path, 'r:gz') as tar:
                tar.extractall(path=temp_dir)
        elif asset['name'].endswith('.zip'):
            with zipfile.ZipFile(download_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)

        # Find and copy the binary
        binary_name = 'age-plugin-yubikey'
        if system == 'windows':
            binary_name += '.exe'

        # Search for the binary in the extracted files
        for root, _, files in os.walk(temp_dir):
            for file in files:
                if file == binary_name:
                    src = Path(root) / file
                    dst = install_dir / file
                    shutil.copy2(src, dst)
                    os.chmod(dst, 0o755)  # Make executable
                    print(f"Installed to {dst}")
                    return True

        print("Could not find the binary in the extracted files")
        return False

    finally:
        # Cleanup
        shutil.rmtree(temp_dir)

def main() -> bool:
    # First check if age is installed
    if not check_command_exists('age'):
        print("Error: age is not installed. Please install age first.")
        return False
        sys.exit(1)

    # Check if age-plugin-yubikey is already installed
    if check_command_exists('age-plugin-yubikey'):
        print("age-plugin-yubikey is already installed!")
        return True
    else:
        print("age-plugin-yubikey is not installed. Attempting to install...")
        install_age_plugin_yubikey()

        # Verify installation
        if check_command_exists('age-plugin-yubikey'):
            print("age-plugin-yubikey has been successfully installed!")
            return True
        else:
            print("Failed to verify age-plugin-yubikey installation.")
            print("Please install manually: https://github.com/str4d/age-plugin-yubikey")
            return False

if __name__ == "__main__":
    main()

# Created/Modified files during execution:
# - ~/.age/plugins/age-plugin-yubikey (or age-plugin-yubikey.exe on Windows)
# - Temporary directory ./age-plugin-yubikey-temp (deleted after installation)
