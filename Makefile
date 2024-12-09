all: prepare install

prepare:
	chmod +x *.py

install:
	sudo python3 setup_files/install_age.py
	sudo python3 setup_files/install_age_plugin.py
	python3 setup_files/directory_checker_yubicrypt.py
	mkdir -p  /home/$USER/.yubiCrypt/keys
	python3 setup_files/copy_run_files.py
	python3 setup_files/directory_checker_dcde.py
	python3 setup_files/add_aliases.py
