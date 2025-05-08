from kafka import KafkaProducer
import time
import json

producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))

def generate_data():
    for i in range(100):
        data = {'number': i}
        producer.send('stream_topic', value=data)
        print(f"Sent: {data}")
        time.sleep(1)

if __name__ == "__main__":
    generate_data()
