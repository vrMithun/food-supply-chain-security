# save as generate_sensor_data.py

import json
import random
import hashlib
from datetime import datetime, timedelta
import os

# Sensor definitions: fixed sensor ID and location
SENSORS = {
    "sensor_A": {"secret": "secret_key_A123", "location": "Zone-A"},
    "sensor_B": {"secret": "secret_key_B456", "location": "Zone-B"},
    "sensor_C": {"secret": "secret_key_C789", "location": "Zone-C"}
}

def hash_secret(secret):
    return hashlib.sha256(secret.encode()).hexdigest()

def generate_sensor_data(entries_per_sensor=333):
    base_time = datetime(2025, 1, 1, 0, 0, 0)
    data = []

    for sensor_id, info in SENSORS.items():
        secret = info["secret"]
        location = info["location"]
        auth_token_hash = hash_secret(secret)

        for i in range(entries_per_sensor):
            timestamp = (base_time + timedelta(minutes=i)).isoformat() + "Z"
            temperature = round(random.uniform(20.0, 30.0), 2)
            humidity = random.randint(40, 70)

            entry = {
                "timestamp": timestamp,
                "temperature": temperature,
                "humidity": humidity,
                "location": location,
                "entity_id": sensor_id,
                "auth_token_hash": auth_token_hash
            }
            data.append(entry)

    return {"sensor_data": data}

# Ensure output directory exists
os.makedirs("data", exist_ok=True)

# Save to file
output_path = "data/sensor_values.json"
with open(output_path, "w") as f:
    json.dump(generate_sensor_data(), f, indent=4)

print(f"Generated realistic sensor data at {output_path}")
