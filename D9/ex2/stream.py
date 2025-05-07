import faust

app = faust.App(
    'vent-count-stream',
    broker='kafka://localhost:9092',
    store='memory://'
)

# Topic nhận dữ liệu
vent_topic = app.topic('vent_data', value_type=dict)

# Table lưu đếm số vents theo tài khoản vent_id
vent_counts = app.Table('vent_counts', default=int)

# Timer mỗi 60 giây để in kết quả và reset đếm
@app.timer(interval=60.0)
async def display_and_reset():
    print("=== Thống kê vents trong phút vừa rồi ===")
    for vent_id, count in vent_counts.items():
        print(f"Vent ID: {vent_id} - Số lần: {count}")
    vent_counts.clear()
    print("=== Đã reset đếm ===\n")

# Agent xử lý dữ liệu đến
@app.agent(vent_topic)
async def process_vents(vents):
    async for vent in vents:
        vent_id = vent['vent_id']
        vent_counts[vent_id] += 1

if __name__ == '__main__':
    app.main()
