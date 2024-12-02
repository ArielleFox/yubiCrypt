#!/bin/env python3
import os
from setup_files.install_age_plugin import main as age_plugin_check
from setup_files.install_age import main as age_check
from setup_files.directory_checker_yubicrypt import main as directory_checker
from setup_files.copy_run_files import main as copy_run_files
from setup_files.directory_checker_dcde import main as directory_dcde_checker
from setup_files.add_aliases import main as add_aliases

age_enabled: bool = age_check()
age_plugin_enabled: bool = age_plugin_check()
dir_enabled: bool = directory_checker()
dir_dcde_enabled: bool = directory_dcde_checker()
copy_files_enabled: bool = copy_run_files()
aliases_enabled: bool = add_aliases()

requirements: list[bool] = [age_enabled, age_plugin_enabled]
if all(requirements):
        print('Installation 33%')
#[dir_enabled, dir_dcde_enabled,
requirements2: list[bool] = [copy_files_enabled, aliases_enabled]
if all(requirements2):
        print('Installation 66%')
requirements3: list[bool] = [dir_dcde_enabled, dir_enabled]
if all(requirements3):
        print('Installation 99%')

print('Installation 100%')

