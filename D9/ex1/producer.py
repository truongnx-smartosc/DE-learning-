import time
import random
from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

topic = 'sensor_data'

try:
    while True:
        data = {
            'sensor_id': random.randint(1, 10),
            'temperature': round(random.uniform(20, 30), 2),
            'humidity': round(random.uniform(30, 70), 2),
            'timestamp': int(time.time())
        }
        producer.send(topic, data)
        print(f"Đã gửi: {data}")
        time.sleep(2)
except KeyboardInterrupt:
    print("Dừng gửi dữ liệu")
finally:
    producer.flush()
    producer.close()
