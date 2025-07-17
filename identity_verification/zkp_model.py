import hashlib
import random

def hash_id(entity_id: str, nonce: str) -> str:
    return hashlib.sha256((entity_id + nonce).encode()).hexdigest()

def generate_zkp_commitment(entity_id: str, challenge: str) -> tuple:
    nonce = str(random.randint(100000, 999999))
    commitment = hash_id(entity_id, nonce)
    return commitment, nonce

def verify_zkp_response(commitment: str, entity_id: str, nonce: str) -> bool:
    expected_commitment = hash_id(entity_id, nonce)
    return commitment == expected_commitment
