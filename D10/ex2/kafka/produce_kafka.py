# kafka/produce_kafka.py

from kafka import KafkaProducer
import json
import time

# Cấu hình Kafka
KAFKA_BROKER = 'localhost:9092'
TOPIC = 'my_data_topic'

def produce():
    producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER,
                             value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    data_samples = [
        {"id": 1, "value": "Dữ liệu mẫu 1", "timestamp": int(time.time())},
        {"id": 2, "value": "Dữ liệu mẫu 2", "timestamp": int(time.time())}
    ]

    for data in data_samples:
        producer.send(TOPIC, value=data)
        print(f"Đã gửi: {data}")
        time.sleep(1)

if __name__ == "__main__":
    produce()
