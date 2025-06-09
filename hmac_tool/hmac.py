import random

# Key generation
def generate_key():
    return random.randint(1000, 100000)

# Generate MAC tag for a value
def generate_mac(value, key):
    return round(value * key,2)

# Verify MAC tag for a value
def verify_mac(value, key, tag):
    return (value * key) == tag

# Verify aggregate value
def verify_aggregate_mac(average, n, key, tag_sum):
    return (average * n* key) == tag_sum
