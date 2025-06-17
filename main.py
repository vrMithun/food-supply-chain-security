from merkle_tool.merkle import (
    load_sensor_data,
    build_merkle_tree,
    get_merkle_root,
    get_merkle_proof,
    verify_merkle_proof,
    hash_sensor_entry
)

from hmac_tool.hmac import HMACTree  # Updated HMAC Tree
from decimal import Decimal
import json

print("\n--- Loading Initial Sensor Data ---")
raw_data, leaves = load_sensor_data('data/sensor_values.json')
tree = build_merkle_tree(leaves)
root = get_merkle_root(tree)
print(f"Merkle Root: {root}")

# Choose a leaf to verify
test_index = 2
proof = get_merkle_proof(tree, test_index)
print(f"Proof for leaf index {test_index}: {proof}")
valid = verify_merkle_proof(leaves[test_index], proof, root, test_index)  # PASS index here
print(f"Merkle Proof Verification: {valid}")

# --- HMAC Tree Section ---
print("\n--- HMAC Tree Section ---")

# Step 1: Initialize HMAC Tree
key = Decimal('7.25')  # Shared secret key
hmac_tree = HMACTree(key)

# Step 2: Insert data into HMAC Tree
for entry in raw_data:
    hmac_tree.insert(entry['timestamp'], entry['temperature'])

# Step 3: Compute and verify aggregates with MACs
average, min_temp, max_temp, avg_mac, min_mac, max_mac = hmac_tree.compute_aggregates_and_macs()
print(f"Average Temp: {average}")
print(f"Min Temp: {min_temp}")
print(f"Max Temp: {max_temp}")
print(f"MAC for AVG: {avg_mac}")
print(f"MAC for MIN: {min_mac}")
print(f"MAC for MAX: {max_mac}")

# Step 4: Verification
print(f"Verify AVG MAC: {hmac_tree.verify_aggregate_mac('AVG', average, avg_mac)}")
print(f"Verify MIN MAC: {hmac_tree.verify_aggregate_mac('MIN', min_temp, min_mac)}")
print(f"Verify MAX MAC: {hmac_tree.verify_aggregate_mac('MAX', max_temp, max_mac)}")

# --- Simulate New Sensor Data Insertion ---
print("\n--- Simulate New Sensor Data Insertion ---")
new_entry = {
    "timestamp": "2025-06-15T18:00:00Z",
    "temperature": 29.3,
    "humidity": 65,
    "location": "Zone-C"
}

# Insert into Merkle Tree
raw_data.append(new_entry)
leaves.append(hash_sensor_entry(new_entry))
updated_tree = build_merkle_tree(leaves)
updated_root = get_merkle_root(updated_tree)

# Insert into HMAC Tree
hmac_tree.insert(new_entry["timestamp"], new_entry["temperature"])

# Recompute and verify updated aggregates
updated_avg, updated_min, updated_max, updated_avg_mac, updated_min_mac, updated_max_mac = hmac_tree.compute_aggregates_and_macs()
print(f"Updated Merkle Root: {updated_root}")
print(f"Updated Average Temp: {updated_avg}")
print(f"Updated Min Temp: {updated_min}")
print(f"Updated Max Temp: {updated_max}")
print(f"Updated MAC for AVG: {updated_avg_mac}")
print(f"Updated MAC for MIN: {updated_min_mac}")
print(f"Updated MAC for MAX: {updated_max_mac}")
print(f"Updated Verify AVG MAC: {hmac_tree.verify_aggregate_mac('AVG', updated_avg, updated_avg_mac)}")

# --- Tampering Simulation ---
print("\n--- Tampering Simulation ---")

# Tamper with last entry's temperature
tampered_entry = raw_data[-1].copy()
tampered_entry["temperature"] = 100.0  # Simulate unrealistic tamper

# Verify Merkle proof with tampered data
tampered_hash = hash_sensor_entry(tampered_entry)
tampered_index = len(leaves) - 1
proof = get_merkle_proof(updated_tree, tampered_index)
valid_merkle = verify_merkle_proof(tampered_hash, proof, updated_root, tampered_index)  # Pass index
print(f"Merkle Verification After Tampering: {valid_merkle}")

# Tampered temperature values
tampered_temps = [Decimal(str(e["temperature"])) for e in raw_data[:-1]] + [Decimal('100.0')]
tampered_avg = round(sum(tampered_temps) / len(tampered_temps), 2)
print(f"Tampered Average: {tampered_avg}")
print(f"Verify AVG MAC After Tampering: {hmac_tree.verify_aggregate_mac('AVG', tampered_avg, updated_avg_mac)}")
