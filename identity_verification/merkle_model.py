import hashlib

def hash_leaf(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()

def build_merkle_tree(leaves: list) -> list:
    if not leaves:
        return []

    current_level = [hash_leaf(leaf) for leaf in leaves]
    tree = [current_level]

    while len(current_level) > 1:
        next_level = []
        for i in range(0, len(current_level), 2):
            left = current_level[i]
            right = current_level[i + 1] if i + 1 < len(current_level) else left
            combined = left + right
            parent_hash = hashlib.sha256(combined.encode()).hexdigest()
            next_level.append(parent_hash)
        current_level = next_level
        tree.append(current_level)

    return tree

def get_merkle_root(tree: list) -> str:
    return tree[-1][0] if tree else None

def get_merkle_proof(tree: list, index: int) -> list:
    proof = []
    for level in tree[:-1]:
        sibling_index = index ^ 1  # flip last bit
        if sibling_index < len(level):
            proof.append(level[sibling_index])
        else:
            proof.append(level[index])
        index //= 2
    return proof

def verify_proof(leaf: str, proof: list, root: str) -> bool:
    current_hash = hash_leaf(leaf)
    for sibling in proof:
        combined = current_hash + sibling if current_hash < sibling else sibling + current_hash
        current_hash = hashlib.sha256(combined.encode()).hexdigest()
    return current_hash == root
