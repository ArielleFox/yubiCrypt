#!/usr/bin/env python3  
  
import os  
import subprocess  
import platform  
import sys  
  
def get_linux_distribution():  
    """Detect the Linux distribution."""  
    try:  
        with open('/etc/os-release', 'r') as f:  
            lines = f.readlines()  
            dist_info = {}  
            for line in lines:  
                if '=' in line:  
                    key, value = line.strip().split('=', 1)  
                    dist_info[key] = value.strip('"')  
            return dist_info.get('ID', '').lower()  
    except FileNotFoundError:  
        return None  
  
def check_root():  
    """Check if script is running with root privileges."""  
    if os.geteuid() != 0:  
        print("This script must be run as root (sudo).")  
        sys.exit(1)  
  
def run_command(command):  
    """Execute a shell command and handle errors."""  
    try:  
        subprocess.run(command, shell=True, check=True)  
    except subprocess.CalledProcessError as e:  
        print(f"Error executing command: {command}")  
        print(f"Error message: {str(e)}")  
        sys.exit(1)  
  
def check_dependencies():  
    """Check if required build dependencies are installed."""  
    dependencies = {  
        'cachyos': ['base-devel', 'pkg-config', 'libusb', 'systemd'],  
        'debian': ['build-essential', 'pkg-config', 'libusb-1.0-0-dev', 'libudev-dev'],  
        'ubuntu': ['build-essential', 'pkg-config', 'libusb-1.0-0-dev', 'libudev-dev'],  
        'fedora': ['gcc', 'gcc-c++', 'make', 'pkgconfig', 'libusbx-devel', 'systemd-devel'],  
        'rhel': ['gcc', 'gcc-c++', 'make', 'pkgconfig', 'libusbx-devel', 'systemd-devel'],  
        'centos': ['gcc', 'gcc-c++', 'make', 'pkgconfig', 'libusbx-devel', 'systemd-devel'],  
        'arch': ['base-devel', 'pkg-config', 'libusb', 'systemd'],  
        'opensuse': ['gcc', 'gcc-c++', 'make', 'pkg-config', 'libusb-1_0-devel', 'systemd-devel'],  
        'gentoo': ['sys-devel/gcc', 'dev-util/pkgconfig', 'dev-libs/libusb', 'sys-apps/systemd']  
    }  
      
    distro = get_linux_distribution()  
    if distro not in dependencies:  
        print(f"Unsupported distribution: {distro}")
        print(f"Please submit your distrobution with the value of: <{distro}> and the name of their <package-manager> for integration as git issue.")
        sys.exit(1)  
      
    return dependencies[distro]  
  
def install_pcsclite():  
    """Install PCSC-Lite based on the detected distribution."""  
    check_root()  
    distro = get_linux_distribution()  
      
    print(f"Detected Linux distribution: {distro}")  
      
    # Package names for different distributions  
    packages = { 
        'cachyos': 'pcsclite ccid',
        'debian': 'pcscd libpcsclite1 libpcsclite-dev',  
        'ubuntu': 'pcscd libpcsclite1 libpcsclite-dev',  
        'fedora': 'pcsc-lite pcsc-lite-devel',  
        'rhel': 'pcsc-lite pcsc-lite-devel',  
        'centos': 'pcsc-lite pcsc-lite-devel',  
        'arch': 'pcsclite ccid',  
        'opensuse': 'pcsc-lite pcsc-lite-devel',  
        'gentoo': 'sys-apps/pcsc-lite'  
    }  
      
    if distro not in packages:  
        print(f"Unsupported distribution: {distro}")  
        sys.exit(1)  
      
    # Update package manager  
    update_commands = {  
        'cachyos': 'pacman -Sy',
        'debian': 'apt-get update',  
        'ubuntu': 'apt-get update',  
        'fedora': 'dnf check-update',  
        'rhel': 'yum check-update',  
        'centos': 'yum check-update',  
        'arch': 'pacman -Sy',  
        'opensuse': 'zypper refresh',  
        'gentoo': 'emerge --sync'  
    }  
      
    # Install commands  
    install_commands = {  
        'debian': f"apt-get install -y {packages[distro]}",  
        'ubuntu': f"apt-get install -y {packages[distro]}",  
        'fedora': f"dnf install -y {packages[distro]}",  
        'rhel': f"yum install -y {packages[distro]}",  
        'centos': f"yum install -y {packages[distro]}",  
        'arch': f"pacman -S --noconfirm {packages[distro]}",  
        'cachyos': f"pacman -S --noconfirm {packages[distro]}",  
        'opensuse': f"zypper install -y {packages[distro]}",  
        'gentoo': f"emerge {packages[distro]}"  
    }  
      
    # Check and install dependencies  
    deps = check_dependencies()  
    print("Installing dependencies...")  
    if distro in ['debian', 'ubuntu']:  
        run_command(f"apt-get install -y {' '.join(deps)}")  
    elif distro in ['fedora', 'rhel', 'centos']:  
        run_command(f"yum install -y {' '.join(deps)}")  
    elif distro in ['arch', 'cachyos']:  
        run_command(f"pacman -S --noconfirm {' '.join(deps)}")  
    elif distro == 'opensuse':  
        run_command(f"zypper install -y {' '.join(deps)}")  
    elif distro == 'gentoo':  
        run_command(f"emerge {' '.join(deps)}")  
      
    # Update package manager  
    print("Updating package manager...")  
    run_command(update_commands[distro])  
      
    # Install PCSC-Lite  
    print("Installing PCSC-Lite...")  
    run_command(install_commands[distro])  
      
    # Start and enable the pcscd service  
    print("Starting PCSC-Lite daemon...")  
    run_command("systemctl enable pcscd")  
    run_command("systemctl start pcscd")  
      
    print("PCSC-Lite installation completed successfully!")  
    print("You can verify the installation by running: pcsc_scan")  
  
if __name__ == "__main__":  
    if platform.system() != "Linux":  
        print("This script only works on Linux systems.")  
        sys.exit(1)  
      
    try:  
        install_pcsclite()  
    except Exception as e:  
        print(f"An error occurred: {str(e)}")  
        sys.exit(1)  
