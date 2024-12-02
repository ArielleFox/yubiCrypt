#!/bin/env python3
import os

def list_yubikeys() -> None:
	os.system('age-plugin-yubikey --list')

def generate_new_key() -> None:
	os.system('age-plugin-yubikey generate')

if __name__ == "__main__":
	list_yubikeys()
	generate_new_key()

