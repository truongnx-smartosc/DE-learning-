from kafka import KafkaConsumer
import json
import datetime
import time
import threading

# Khởi tạo Kafka Consumer
consumer = KafkaConsumer(
    'sensor_data',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    group_id='user_data_group',
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

# Biến đếm
count_data = []

def show_count():
    while True:
        time.sleep(60)  # đợi 60 giây
        total = len(count_data)
        now_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"{now_str} - Số dữ liệu trong phút này: {total}")
        count_data.clear()

# Chạy thread in ra số lượng dữ liệu mỗi phút
threading.Thread(target=show_count, daemon=True).start()

print("Bắt đầu nghe Kafka... Nhấn Ctrl+C để dừng.")

try:
    for message in consumer:
        # Chỉ đếm dữ liệu
        count_data.append(1)
except KeyboardInterrupt:
    print("Kết thúc.")
finally:
    consumer.close()
