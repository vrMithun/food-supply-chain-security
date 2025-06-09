# Food Supply Chain Security Using Homomorphic MAC and Merkle Tree

## Abstract

This project presents a secure and efficient approach for food supply chain management by integrating homomorphic Message Authentication Codes (MACs) with Merkle tree data structures.

- **Merkle Tree Layer:** Frequently updated sensor data (temperature, humidity, location) is stored in a Merkle tree, where each node is augmented with homomorphic MACs to allow authenticated updates and tamper-evident integrity verification.

- **Aggregate Verification Layer:** Critical aggregate metrics (minimum, maximum, average temperatures) computed during data collection are verified directly using homomorphic MACs, eliminating the need to retrieve and recompute underlying raw data—improving verification efficiency and privacy.

This dual-layer system ensures fine-grained traceability alongside efficient, privacy-preserving verification of key metrics, making it ideal for scalable, secure food supply chain applications.

---

## Features

- Secure storage and verification of sensor data with Merkle trees
- Homomorphic MAC-based authentication for frequent data updates
- Efficient verification of aggregate values (min, max, average) without full data retrieval
- Tamper-evident mechanisms to detect data manipulation
- Benchmarked performance comparison between Merkle tree and homomorphic MAC approaches

---

## Project Structure

- `data/` — Sample sensor data in JSON format
- `merkle_tool/` — Implementation of Merkle tree construction, hashing, and proof verification
- `hmac_tool/` — Homomorphic MAC generation and verification functions
- `comparison/benchmark.py` — Script for performance benchmarking of both approaches
- `main.py` — End-to-end demonstration of data authentication and update verification

---

## Requirements

- Python 3.8+
- Dependencies: `hashlib`, `json`, and other standard Python libraries

---

## Usage

1. Place sensor data in `data/sensor_values.json`.
2. Run `main.py` to:
   - Build and verify Merkle tree for sensor data
   - Generate and verify homomorphic MACs for aggregates
   - Simulate frequent data updates and verify integrity
3. Use `comparison/benchmark.py` to compare performance of Merkle tree vs. homomorphic MAC approaches.

---

## How It Works

- **Merkle Tree:** Data entries are hashed into leaves; internal nodes store combined hashes to form the root. Proofs verify inclusion of any leaf efficiently.
- **Homomorphic MACs:** Allow algebraic operations on authentication tags so aggregate values can be verified without exposing raw data.
- **Update Simulation:** Demonstrates integrity checks after sensor data changes, ensuring tamper evidence.

---

## Contact

For questions or contributions, please reach out to:

[Your Name]  
[Your Email]  
[GitHub Repository Link]
