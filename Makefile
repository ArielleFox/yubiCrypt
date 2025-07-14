all: prepare install rust

prepare:
	chmod +x *.py

install:
	sudo python3 setup_files/install_age.py
	sudo python3 setup_files/install_age_plugin.py
	python3 setup_files/directory_checker_yubicrypt.py
	mkdir -p  ~/.yubiCrypt/keys
	mkdir -p  ~/.yubiCrypt/yubiCryptImporter
	cp -r ./yubiCryptImporter/*.py ~/.yubiCrypt/yubiCryptImporter/
	mkdir -p  ~/.yubiCrypt/yubiCryptImporter/modules
	cp -r ./yubiCryptImporter/modules/ ~/.yubiCrypt/yubiCryptImporter/
	python3 setup_files/copy_run_files.py
	python3 setup_files/directory_checker_dcde.py
	python3 setup_files/add_aliases.py

rust:
	cd alpha_rust_rewrite/; cargo build --release; cd -;
