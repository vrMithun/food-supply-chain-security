# save as generate_sensor_data.py

import json
import random
from datetime import datetime, timedelta

def generate_sensor_data(num_entries=1000):
    base_time = datetime(2025, 1, 1, 0, 0, 0)
    data = []

    for i in range(num_entries):
        timestamp = (base_time + timedelta(minutes=i)).isoformat() + "Z"
        temperature = round(random.uniform(20.0, 30.0), 2)
        humidity = random.randint(40, 70)
        location = f"Zone-{random.choice(['A', 'B', 'C'])}"

        entry = {
            "timestamp": timestamp,
            "temperature": temperature,
            "humidity": humidity,
            "location": location
        }
        data.append(entry)

    return {"sensor_data": data}

# Save to file
output_path = "data/sensor_values.json"
with open(output_path, "w") as f:
    json.dump(generate_sensor_data(), f, indent=4)

print(f"Generated 1000+ sensor entries at {output_path}")
