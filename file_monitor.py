import hashlib
import os
import json

# Change this path to the directory you want to monitor
DIRECTORY_TO_MONITOR = r"C:\TASK 1"  # Use raw string or double backslashes
HASH_RECORD_FILE = "file_hashes.json"

def calculate_hash(file_path):
    sha256 = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            while chunk := f.read(4096):
                sha256.update(chunk)
        return sha256.hexdigest()
    except FileNotFoundError:
        return None

def scan_directory(directory):
    file_hashes = {}
    for root, _, files in os.walk(directory):
        for file in files:
            full_path = os.path.join(root, file)
            hash_val = calculate_hash(full_path)
            if hash_val:
                file_hashes[full_path] = hash_val
    return file_hashes

def load_previous_hashes():
    if os.path.exists(HASH_RECORD_FILE):
        with open(HASH_RECORD_FILE, "r") as f:
            return json.load(f)
    return {}

def save_hashes(hashes):
    with open(HASH_RECORD_FILE, "w") as f:
        json.dump(hashes, f, indent=4)

def compare_hashes(old, new):
    modified = []
    deleted = []
    new_files = []

    for path, hash_val in old.items():
        if path not in new:
            deleted.append(path)
        elif new[path] != hash_val:
            modified.append(path)

    for path in new:
        if path not in old:
            new_files.append(path)

    return modified, deleted, new_files

def main():
    print("[*] Scanning directory...")
    new_hashes = scan_directory(DIRECTORY_TO_MONITOR)
    old_hashes = load_previous_hashes()

    modified, deleted, new_files = compare_hashes(old_hashes, new_hashes)

    print("\n[*] Integrity Report:")
    if modified:
        print("\n[!] Modified Files:")
        for file in modified:
            print(f" - {file}")
    if deleted:
        print("\n[-] Deleted Files:")
        for file in deleted:
            print(f" - {file}")
    if new_files:
        print("\n[+] New Files:")
        for file in new_files:
            print(f" - {file}")
    if not (modified or deleted or new_files):
        print("[✓] No changes detected.")

    save_hashes(new_hashes)
    print("\n[*] Hashes saved for future comparison.")

if __name__ == "__main__":
    main()
