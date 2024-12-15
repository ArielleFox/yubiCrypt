#!/bin/env python3.14
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import OrderedDict
import threading
import ast
import os
import queue

class ThreadSafeDict:
    def __init__(self):
        self._dict = {}
        self._lock = threading.Lock()

    def __setitem__(self, key, value):
        with self._lock:
            self._dict[key] = value

    def __getitem__(self, key):
        with self._lock:
            return self._dict[key]

    def items(self):
        with self._lock:
            return self._dict.copy().items()

    def keys(self):
        with self._lock:
            return self._dict.copy().keys()

    def __bool__(self):
        with self._lock:
            return bool(self._dict)

    def to_dict(self):
        with self._lock:
            return self._dict.copy()

class ResultPrinter:
    def __init__(self):
        self._print_lock = threading.Lock()
        self._print_queue = queue.Queue()
        self._print_thread = threading.Thread(target=self._print_worker, daemon=True)
        self._print_thread.start()

    def print(self, message):
        self._print_queue.put(message)

    def _print_worker(self):
        while True:
            message = self._print_queue.get()
            with self._print_lock:
                print(message)

def read_existing_data(filename='identities.dict'):
    """Read existing data from file if it exists"""
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as f:
                content = f.read()
                if content:
                    return ast.literal_eval(content)
        except (SyntaxError, ValueError) as e:
            print(f"Error reading existing file: {e}")
    return {}

def compare_and_merge_data(new_data, existing_data):
    """Compare and merge new data with existing data"""
    merged_data = existing_data.copy()
    changes = False

    for slot, identity in new_data.items():
        if slot not in existing_data or existing_data[slot] != identity:
            merged_data[slot] = identity
            changes = True

    return merged_data, changes

def save_data(data, filename='identities.dict'):
    """Save data to file"""
    with open(filename, 'w') as f:
        f.write(str(dict(data)))

def run_yubikey_command(slot):
    command = f"age-plugin-yubikey --identity --slot {slot}"
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
        return None
    except Exception as e:
        print(f"Error running command for slot {slot}: {e}")
        return None

def worker(slot: int, shared_dict: ThreadSafeDict, printer: ResultPrinter) -> None:
    printer.print(f"Checking slot {slot}...")
    result = run_yubikey_command(slot)

    if result:
        shared_dict[slot] = result
        printer.print(f"Found valid slot {slot}: {result}")

def process_slots_threaded(slot_range, max_workers=8):
    shared_dict = ThreadSafeDict()
    printer = ResultPrinter()

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for slot in slot_range:
            future = executor.submit(worker, slot, shared_dict, printer)
            futures.append(future)

        # Wait for all futures to complete
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                printer.print(f"Error in thread: {e}")

    return shared_dict.to_dict()

def print_sorted_results(results_dict):
    if results_dict:
        print("\nValid Slots Found (Sorted):")
        sorted_slots = OrderedDict(sorted(results_dict.items(), key=lambda x: x[0]))
        for slot, identity in sorted_slots.items():
            print(f"\nSlot {slot}:")
            print(f"Identity: {identity}")
    else:
        print("No valid slots found.")

def main():
    # Read existing data
    existing_data = read_existing_data()
    print("Checking slots...")

    # Process slots with threads
    slot_range = range(22)  # 0-21
    results = process_slots_threaded(slot_range)

    # Final results sorted by slot number
    print("\nFinal Results:")
    print_sorted_results(results)

    # Compare and merge with existing data
    merged_data, changes = compare_and_merge_data(results, existing_data)

    if changes:
        print("\nNew changes detected. Updating file...")
        save_data(merged_data)
    else:
        print("\nNo new changes detected. File remains unchanged.")

if __name__ == "__main__":
    main()

# Created/Modified files during execution:
# identities.dict (only if changes are detected)
