#!/usr/bin/env python3
from typing import Any
import os
import sys
import shutil
from pathlib import Path
import stat
import datetime
import hashlib

def calculate_file_hash(file_path):
    """Calculate SHA-256 hash of a file"""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def create_file_manifest(source_dir, dest_dir):
    """Create a manifest of copied files with their hashes"""
    manifest = []
    source_path = Path(source_dir)
    dest_path = Path(dest_dir)

    for src_file in source_path.rglob('*'):
        if src_file.is_file():
            rel_path = src_file.relative_to(source_path)
            dest_file = dest_path / rel_path

            manifest.append({
                'source_path': str(src_file),
                'dest_path': str(dest_file),
                'hash': calculate_file_hash(src_file),
                'size': src_file.stat().st_size,
                'timestamp': datetime.datetime.fromtimestamp(src_file.stat().st_mtime).isoformat()
            })

    return manifest

def verify_copy(manifest):
    """Verify that files were copied correctly using their hashes"""
    all_valid = True
    for file_info in manifest:
        dest_path = Path(file_info['dest_path'])
        if not dest_path.exists():
            print(f"❌ Missing file: {dest_path}")
            all_valid = False
            continue

        dest_hash = calculate_file_hash(dest_path)
        if dest_hash != file_info['hash']:
            print(f"❌ Hash mismatch for {dest_path}")
            all_valid = False
        else:
            print(f"✅ Verified: {dest_path}")

    return all_valid

def copy_with_permissions(src, dst, manifest_path):
    """
    Copy run_files directory to ~/.yubiCrypt/run_files/
    with proper permissions and verification
    """
    try:
        source_dir = Path(src).resolve()
        dest_dir = Path(dst).resolve()

        # Check if source directory exists
        if not source_dir.exists():
            print(f"Error: Source directory '{source_dir}' does not exist!")
            return False

        # Check if source directory is readable
        if not os.access(source_dir, os.R_OK):
            print(f"Error: No read permission for '{source_dir}'!")
            return False

        # Create destination directory if it doesn't exist
        dest_dir.mkdir(parents=True, exist_ok=True)

        # Set secure permissions on destination directory
        os.chmod(dest_dir, stat.S_IRWXU)  # 700 permissions

        print(f"📁 Copying files from {source_dir} to {dest_dir}")
        print("=" * 60)

        # Create manifest before copying
        manifest = create_file_manifest(source_dir, dest_dir)

        # Copy files
        for item in manifest:
            src_path = Path(item['source_path'])
            dst_path = Path(item['dest_path'])

            # Create parent directories if they don't exist
            dst_path.parent.mkdir(parents=True, exist_ok=True)

            # Copy file
            print(f"Copying: {src_path.relative_to(source_dir)}")
            shutil.copy2(src_path, dst_path)

            # Set secure permissions (600) for files
            os.chmod(dst_path, stat.S_IRUSR | stat.S_IWUSR)

        # Save manifest
        manifest_file = dest_dir / "copy_manifest.txt"
        with open(manifest_file, 'w') as f:
            for item in manifest:
                f.write(f"File: {item['dest_path']}\n")
                f.write(f"Hash: {item['hash']}\n")
                f.write(f"Size: {item['size']} bytes\n")
                f.write(f"Timestamp: {item['timestamp']}\n")
                f.write("-" * 50 + "\n")

        # Set secure permissions for manifest file
        os.chmod(manifest_file, stat.S_IRUSR | stat.S_IWUSR)

        print("🔍 Verifying copied files...")
        print("=" * 60)

        # Verify the copy
        if verify_copy(manifest):
            print("✅ All files copied and verified successfully!")
            print(f"📝 Manifest saved to: {manifest_file}")
        else:
            print("❌ Some files failed verification!")
            return False

        # Print summary
        total_size = sum(item['size'] for item in manifest)
        print("📊 Summary:")
        print(f"Total files copied: {len(manifest)}")
        print(f"Total size: {total_size:,} bytes")
        print(f"Manifest location: {manifest_file}")

        return True

    except Exception as e:
        print(f"Error during copy operation: {e}", file=sys.stderr)
        return False

def main():
    print('\n--------------------------------------------')
    print(__file__)
    print('--------------------------------------------\n')

    # Source directory
    source_dir = "run_files"
    source_dir_2 = "src"

    # Destination directory in ~/.yubiCrypt
    dest_dir = Path.home() / ".yubiCrypt" / "run_files"
    # Destination directory in ~/dcde/src
    dest_dir_2 = Path.home() / "dcde" / "src"

    # Manifest path
    manifest_path = dest_dir / "copy_manifest.txt"

    print(f"🚀 Starting secure copy operation...")


    # Check if ~/.yubiCrypt exists
    yubicrypt_dir = Path.home() / ".yubiCrypt"
    if not yubicrypt_dir.exists():
        print(f"Error: {yubicrypt_dir} does not exist!")
        print("Please create it first with proper permissions.")
        sys.exit(1)

    # Perform the copy for .yubiCrypt and dcde
    if copy_with_permissions(source_dir, dest_dir, manifest_path):
        print("✨ Operation completed successfully!")
    else:
        print("❌ Operation failed!")
        return False
        sys.exit(1)
    if copy_with_permissions(source_dir_2, dest_dir_2, manifest_path):
        print("✨ Operation completed successfully!")
        return True
    else:
        print("❌ Operation failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()

# Created/Modified files during execution:
# - ~/.yubiCrypt/run_files/* (copied files)
# - ~/.yubiCrypt/run_files/copy_manifest.txt
