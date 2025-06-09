import hashlib
import json

def hash_leaf(data):
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def build_merkle_tree(leaves):
    if len(leaves) == 0:
        return []

    tree = [leaves]
    while len(tree[-1]) > 1:
        current_level = tree[-1]
        next_level = []
        for i in range(0, len(current_level), 2):
            left = current_level[i]
            right = current_level[i+1] if i+1 < len(current_level) else left  # Duplicate last if odd
            combined = left + right
            parent = hashlib.sha256(combined.encode('utf-8')).hexdigest()
            next_level.append(parent)
        tree.append(next_level)
    return tree

def get_merkle_root(tree):
    return tree[-1][0] if tree else None

def load_sensor_data(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)['sensor_data']
    leaves = []
    for record in data:
        encoded = f"{record['timestamp']}|{record['temperature']}|{record['humidity']}|{record['location']}"
        leaves.append(hash_leaf(encoded))
    return leaves

def get_merkle_proof(tree, index):
    """
    Returns the Merkle proof (list of sibling hashes) for the leaf at given index.
    """
    proof = []
    for level in tree[:-1]:  # exclude root level
        sibling_index = index ^ 1  # get sibling (flip last bit)
        if sibling_index < len(level):
            proof.append(level[sibling_index])
        else:
            # If sibling doesn't exist (odd number), sibling is the node itself
            proof.append(level[index])
        index //= 2
    return proof

def verify_merkle_proof(leaf_hash, proof, root):
    """
    Verifies the leaf hash against the Merkle root using the proof.
    Proof is list of sibling hashes from leaf up to root.
    """
    computed_hash = leaf_hash
    for sibling_hash in proof:
        # Always concatenate the smaller hash first for consistency
        if computed_hash < sibling_hash:
            combined = computed_hash + sibling_hash
        else:
            combined = sibling_hash + computed_hash
        computed_hash = hashlib.sha256(combined.encode('utf-8')).hexdigest()
    return computed_hash == root

# Re-hash and replace the affected leaf
def hash_sensor_entry(entry):
    sensor_str = f"{entry['timestamp']}-{entry['temperature']}-{entry['humidity']}-{entry['location']}"
    return hashlib.sha256(sensor_str.encode()).hexdigest()

