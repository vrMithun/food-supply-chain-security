import json
import time
import os
import matplotlib.pyplot as plt

from merkle_model import (
    build_merkle_tree,
    get_merkle_root,
    get_merkle_proof,
    verify_proof
)

from zkp_model import (
    generate_zkp_commitment,
    verify_zkp_response
)

# Load entity data
with open(r"D:\workspace\food-supply-chain-security\identity_verification\authorized_entities.json", "r") as f:
    authorized_ids = json.load(f)["authorized_ids"]

test_entity = "EMP007"

# === Merkle Tree Identity Verification ===
print("=== Merkle Tree Identity Verification ===")
merkle_tree = build_merkle_tree(authorized_ids)
root = get_merkle_root(merkle_tree)
index = authorized_ids.index(test_entity)
proof = get_merkle_proof(merkle_tree, index)

start_merkle = time.perf_counter()
merkle_valid = verify_proof(test_entity, proof, root)
end_merkle = time.perf_counter()
merkle_time = round(end_merkle - start_merkle, 6)
print(f"Merkle Verification: {merkle_valid}")
print(f"Merkle Time: {merkle_time} seconds")

# === Zero-Knowledge Proof Identity Verification ===
print("\n=== Zero-Knowledge Proof Identity Verification ===")
challenge = "random_challenge"
commitment, nonce = generate_zkp_commitment(test_entity, challenge)

start_zkp = time.perf_counter()
zkp_valid = verify_zkp_response(commitment, test_entity, nonce)
end_zkp = time.perf_counter()
zkp_time = round(end_zkp - start_zkp, 6)
print(f"ZKP Verification: {zkp_valid}")
print(f"ZKP Time: {zkp_time} seconds")

# === Benchmark Summary ===
print("\n=== Benchmark Summary ===")
print(f"Merkle Tree Verification Time: {merkle_time} seconds")
print(f"ZKP Verification Time: {zkp_time} seconds")

# === Plotting ===
labels = ['Merkle Tree', 'Zero-Knowledge Proof']
times = [merkle_time, zkp_time]

plt.figure(figsize=(8, 5))
bars = plt.bar(labels, times, color=['#4CAF50', '#2196F3'])
plt.title('Identity Verification: Merkle Tree vs ZKP')
plt.ylabel('Time (seconds)')

# Add values on top
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, height + 0.00001, f'{height:.6f}', ha='center', va='bottom')

plt.tight_layout()
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()
