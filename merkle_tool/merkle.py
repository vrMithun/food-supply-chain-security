import hashlib
import json

# Hash a single sensor entry into a leaf
def hash_sensor_entry(entry):
    sensor_str = f"{entry['timestamp']}|{entry['temperature']}|{entry['humidity']}|{entry['location']}"
    return hashlib.sha256(sensor_str.encode()).hexdigest()

# Build the full Merkle Tree
def build_merkle_tree(leaves):
    if not leaves:
        return []
    tree = [leaves[:]]  # Copy initial leaves
    while len(tree[-1]) > 1:
        current_level = tree[-1]
        next_level = []
        for i in range(0, len(current_level), 2):
            left = current_level[i]
            right = current_level[i + 1] if i + 1 < len(current_level) else left
            combined = left + right
            parent = hashlib.sha256(combined.encode()).hexdigest()
            next_level.append(parent)
        tree.append(next_level)
    return tree

# Extract Merkle root
def get_merkle_root(tree):
    return tree[-1][0] if tree else None

# Load sensor data and compute leaves
def load_sensor_data(filename):
    with open(filename, "r") as f:
        data = json.load(f)
    sensor_data = data["sensor_data"]
    leaves = [hash_sensor_entry(entry) for entry in sensor_data]
    return sensor_data, leaves

# Merkle proof
def get_merkle_proof(tree, index):
    proof = []
    for level in tree[:-1]:
        sibling_index = index ^ 1
        proof.append(level[sibling_index] if sibling_index < len(level) else level[index])
        index //= 2
    return proof

# Verify proof
def verify_merkle_proof(leaf_hash, proof, root, index):
    computed_hash = leaf_hash
    for sibling_hash in proof:
        if index % 2 == 0:
            combined = computed_hash + sibling_hash  # Left + Right
        else:
            combined = sibling_hash + computed_hash  # Left + Right
        computed_hash = hashlib.sha256(combined.encode()).hexdigest()
        index //= 2
    return computed_hash == root


