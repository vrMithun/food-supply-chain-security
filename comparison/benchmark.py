import time
import json
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from merkle_tool.merkle import build_merkle_tree, get_merkle_root, hash_sensor_entry
from hmac_tool.hmac import generate_key, generate_mac, verify_aggregate_mac

# Load sensor data
with open(r'D:\workspace\food-supply-chain-security\data\sensor_values.json', 'r') as f:
    sensor_data = json.load(f)["sensor_data"]

# Prepare temperature list and leaf nodes
temperatures = [round(float(entry["temperature"]), 2) for entry in sensor_data]
leaves = [hash_sensor_entry(entry) for entry in sensor_data]

print("--- Benchmarking Merkle Tree ---")
start = time.time()
tree = build_merkle_tree(leaves)
merkle_root = get_merkle_root(tree)
end = time.time()
print(f"Merkle Root: {merkle_root}")
print(f"Merkle Tree Build Time: {round(end - start, 6)} seconds")

print("\n--- Benchmarking HMAC ---")
key = generate_key()

start = time.time()
macs = [generate_mac(temp, key) for temp in temperatures]
average = round(sum(temperatures) / len(temperatures), 2)
tag_sum = sum(macs)
hmac_valid = verify_aggregate_mac(average, len(temperatures), key, tag_sum)
end = time.time()

print(f"HMAC Verification: {hmac_valid}")
print(f"HMAC Processing Time: {round(end - start, 6)} seconds")
