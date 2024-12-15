#!/bin/env python3
import os

os.system('sudo ./install_pcsclite.py')
os.system('make all')
os.system('sudo python3 setup_files/install_age.py')
os.system('cargo install age-plugin-yubikey')
os.system('sudo python3 setup_files/install_age_plugin.py')
os.system('python3 setup_files/directory_checker_yubicrypt.py')
os.system('python3 setup_files/copy_run_files.py')
os.system('python3 setup_files/directory_checker_dcde.py')
os.system('python3 setup_files/add_aliases.py')
#os.system('mv ./yubiCryptImporter/ ')
