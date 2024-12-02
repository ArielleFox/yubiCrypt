import os

# Checking if key exists else generate first key
os.system("python3 ~/dcde/src/check_or_generate_key.py")
print('------------------------------------------------\n')
os.system("python3  ~/.yubiCrypt/run_files/check_keys.py")
