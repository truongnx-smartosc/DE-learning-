# spark_processing_simulate.py

import time
import json

# Giả lập đọc dữ liệu từ Kafka
# Chỉ in dữ liệu giả định
sample_data = [
    {"id": 1, "value": "Sample data 1", "timestamp": 1683858293},
    {"id": 2, "value": "Sample data 2", "timestamp": 1683858294},
    {"id": 3, "value": "Sample data 3", "timestamp": 1683858295},
    {"id": 4, "value": "Sample data 4", "timestamp": 1683858296},
    {"id": 5, "value": "Sample data 5", "timestamp": 1683858297},
]

print("=== Starting Spark streaming simulation ===")
for record in sample_data:
    # Simulate processing (e.g., show processed data)
    print(f"Processed: {json.dumps(record)}")
    time.sleep(0.5)
print("=== End of simulation ===")
