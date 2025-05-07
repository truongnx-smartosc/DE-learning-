from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'sensor_data',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    group_id='sensor_group',
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

print("Bắt đầu nhận dữ liệu...\n")
try:
    for message in consumer:
        print(f"Đã nhận: {message.value}")
except KeyboardInterrupt:
    print("Dừng nhận dữ liệu")
finally:
    consumer.close()
