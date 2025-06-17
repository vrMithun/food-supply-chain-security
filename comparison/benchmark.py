import time
import json
import sys
import os
from decimal import Decimal

# Add root directory to system path for module access
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from merkle_tool.merkle import build_merkle_tree, get_merkle_root, hash_sensor_entry
from hmac_tool.hmac import HMACTree

# --- Load sensor data ---
data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'sensor_values.json')
if not os.path.exists(data_path):
    raise FileNotFoundError(f"Sensor data file not found at: {data_path}")

with open(data_path, 'r') as f:
    sensor_data = json.load(f)["sensor_data"]

print(f"Total Data Points: {len(sensor_data)}")

# Split the data
initial_entries = sensor_data[:10]
insertion_entries = sensor_data[10:]

# ========== MERKLE TREE BENCHMARK ==========
print("\n--- Benchmarking Merkle Tree ---")

# Build phase
initial_leaves = [hash_sensor_entry(entry) for entry in initial_entries]
start_build = time.perf_counter()
merkle_tree = build_merkle_tree(initial_leaves)
merkle_root = get_merkle_root(merkle_tree)
end_build = time.perf_counter()

# Insertion phase (simulate full rebuilds for each new entry)
insert_start = time.perf_counter()
for entry in insertion_entries:
    initial_leaves.append(hash_sensor_entry(entry))
    merkle_tree = build_merkle_tree(initial_leaves)  # Rebuild
insert_end = time.perf_counter()

print(f"Merkle Root after initial build: {merkle_root}")
print(f"Initial Merkle Build Time: {round(end_build - start_build, 6)} seconds")
print(f"Merkle Tree Insertion (Rebuild) Time: {round(insert_end - insert_start, 6)} seconds")

# ========== HMAC TREE BENCHMARK ==========
print("\n--- Benchmarking HMAC Tree ---")
key = Decimal('7.25')
hmac_tree = HMACTree(key)

# Build phase
start_build = time.perf_counter()
for entry in initial_entries:
    hmac_tree.insert(entry["timestamp"], entry["temperature"])
end_build = time.perf_counter()

# Insertion phase
insert_start = time.perf_counter()
for entry in insertion_entries:
    hmac_tree.insert(entry["timestamp"], entry["temperature"])
insert_end = time.perf_counter()

print(f"Initial HMAC Tree Build Time: {round(end_build - start_build, 6)} seconds")
print(f"HMAC Tree Insertion (Rebuild) Time: {round(insert_end - insert_start, 6)} seconds")
