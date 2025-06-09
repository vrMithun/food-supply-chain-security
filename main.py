from merkle_tool.merkle import (
    load_sensor_data,
    build_merkle_tree,
    get_merkle_root,
    get_merkle_proof,
    verify_merkle_proof,
    hash_sensor_entry
)

from hmac_tool.hmac import (
    generate_key,
    generate_mac,
    verify_aggregate_mac
)

import json

# --- Merkle Tree Section ---
leaves = load_sensor_data('data/sensor_values.json')
tree = build_merkle_tree(leaves)
root = get_merkle_root(tree)

print(f"Merkle Root: {root}")

# Choose a leaf index to test
test_index = 2
leaf = leaves[test_index]
proof = get_merkle_proof(tree, test_index)

print(f"Proof for leaf index {test_index}: {proof}")

# Verify the proof
valid = verify_merkle_proof(leaf, proof, root)
print(f"Verification result: {valid}")

# --- HMAC Section ---
print("\n--- HMAC Section ---")

# Step 1: Load original temperature data
with open('data/sensor_values.json', 'r') as f:
    raw_data = json.load(f)["sensor_data"]

# Convert to float and round to 2 decimal places
temperatures = [round(float(entry["temperature"]), 2) for entry in raw_data]

# Step 2: Generate secret key
key = generate_key()
print(f"Secret Key: {key}")

# Step 3: Generate MACs
macs = [generate_mac(temp, key) for temp in temperatures]
print(f"MACs: {macs}")

# Step 4: Compute average
average = round(sum(temperatures) / len(temperatures), 2)
print(f"Average Temperature: {average}")

# Step 5: Verify average using HMAC
tag_sum = sum(macs)
valid = verify_aggregate_mac(average, len(temperatures), key, tag_sum)
print(f"HMAC Verification for Average: {valid}")

# Step 6: Simulate update (frequent update scenario)
update_index = 2
new_temp = round(28.0, 2)

# Update data
old_temp = temperatures[update_index]
temperatures[update_index] = new_temp
macs[update_index] = generate_mac(new_temp, key)

# Recompute values
updated_average = round(sum(temperatures) / len(temperatures), 2)
updated_tag_sum = sum(macs)

print("\n--- After Updating Index 2 ---")
print(f"Old Temp: {old_temp} -> New Temp: {new_temp}")
print(f"Updated Average Temperature: {updated_average}")

# Verify updated average
valid = verify_aggregate_mac(updated_average, len(temperatures), key, updated_tag_sum)
print(f"Updated HMAC Verification for Average: {valid}")

# --- Merkle Tree Update Simulation ---
print("\n--- Merkle Tree Update Simulation ---")

# Update raw data (simulate tampering)
new_data = raw_data[update_index].copy()
new_data["temperature"] = 30.0  # Changed value

# Update the corresponding leaf
leaves[update_index] = hash_sensor_entry(new_data)

# Rebuild the tree and get new root
updated_tree = build_merkle_tree(leaves)
updated_root = get_merkle_root(updated_tree)

print(f"Updated Merkle Root: {updated_root}")
print("Data Tampered!" if updated_root != root else "No Tampering Detected.")

# --- Tampering Simulation ---
print("\n--- Tampering Simulation ---")

# Tamper with the temperature without updating hash or MAC
tampered_temperatures = temperatures.copy()
tampered_temperatures[1] = 100.0  # unrealistic tampered value

# Recalculate average and tag sum without updating MACs
tampered_average = round(sum(tampered_temperatures) / len(tampered_temperatures), 2)
tampered_tag_sum = sum(macs)  # MACs were not updated!

# Verify HMAC with tampered average
hmac_valid = verify_aggregate_mac(tampered_average, len(tampered_temperatures), key, tampered_tag_sum)
print(f"HMAC Verification After Tampering: {hmac_valid}")

# Merkle part: verify leaf 1 with old proof against original root
tampered_leaf = str(tampered_temperatures[1])  # Fake leaf (not proper hash)
proof = get_merkle_proof(tree, 1)
merkle_valid = verify_merkle_proof(tampered_leaf, proof, root)
print(f"Merkle Verification After Tampering: {merkle_valid}")
