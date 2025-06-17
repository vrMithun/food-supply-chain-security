import hashlib
from decimal import Decimal, getcontext

# Set decimal precision
getcontext().prec = 12

# Hash input to decimal value
def hash_input(input_str):
    digest = hashlib.sha256(input_str.encode()).hexdigest()
    return Decimal(int(digest, 16) % 10**5)

# Generate homomorphic MAC
def generate_mac_for_value(label: str, value: float, key: Decimal) -> Decimal:
    composite = f"{label}-{value}"
    return hash_input(composite) * key

# Verify aggregate MAC
def verify_mac_for_value(label: str, value: float, provided_mac: Decimal, key: Decimal) -> bool:
    expected_mac = generate_mac_for_value(label, value, key)
    print(f"[DEBUG] Expected MAC for {label}: {expected_mac}")
    print(f"[DEBUG] Provided MAC: {provided_mac}")
    return abs(expected_mac - provided_mac) < Decimal("0.000001")

# Node used only for structure (no rebuild needed now)
class HMACTreeNode:
    def __init__(self, timestamp, temperature, key):
        self.timestamp = timestamp
        self.temperature = Decimal(str(temperature))
        self.key = Decimal(str(key))
        self.tag = self.compute_tag()

    def compute_tag(self):
        composite = f"{self.timestamp}-{self.temperature}"
        hashed = hash_input(composite)
        return hashed * self.key

class HMACTree:
    def __init__(self, key):
        self.key = Decimal(str(key))
        self.aggregate_tag = Decimal(0)
        self.nodes = []

    def insert(self, timestamp, temperature):
        temperature_decimal = Decimal(str(temperature))
        node = HMACTreeNode(timestamp, temperature_decimal, self.key)
        self.nodes.append(node)
        self.aggregate_tag += node.tag  # Algebraic update of the tag

    def compute_aggregates_and_macs(self):
        if not self.nodes:
            return None, None, None, None, None, None

        temperatures = [node.temperature for node in self.nodes]

        avg = sum(temperatures) / len(temperatures)
        min_val = min(temperatures)
        max_val = max(temperatures)

        avg_mac = generate_mac_for_value("AVG", avg, self.key)
        min_mac = generate_mac_for_value("MIN", min_val, self.key)
        max_mac = generate_mac_for_value("MAX", max_val, self.key)

        return avg, min_val, max_val, avg_mac, min_mac, max_mac

    def verify_aggregate_mac(self, label, value, provided_mac):
        return verify_mac_for_value(label, value, provided_mac, self.key)
