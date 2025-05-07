# producer_full.py
from kafka import KafkaProducer
import json
import time
import csv
import random

# Khởi tạo Kafka Producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

topic = 'sensor_data'

# Đọc toàn bộ danh sách user đa dạng
with open('users_full.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    users = [row for row in reader]

print(f"Đã đọc {len(users)} người dùng từ file CSV.")

try:
    while True:
        user = random.choice(users)
        data = {
            'name': user['name'],
            'sdt': user['sdt'],
            'province': user['province'],
            'sex': user['sex'],
            'sensor_id': 'sensor_1',
            'vent': random.randint(0, 1),
            'timestamp': int(time.time())
        }
        # Gửi dữ liệu
        producer.send(topic, data)
        print(f"Gửi: {data}")
        time.sleep(1)
except KeyboardInterrupt:
    print("Dừng gửi.")
finally:
    producer.close()
