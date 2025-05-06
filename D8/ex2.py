from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum
import pandas as pd
from sqlalchemy import create_engine

# Khởi tạo SparkSession
spark = SparkSession.builder.appName("Exercise2").getOrCreate()

# Bước 1: Đọc dữ liệu CSV
# Đường dẫn tới file dữ liệu của bạn (thay đổi phù hợp)
input_csv_path = 'data.csv'  # Ví dụ: 'data.csv'
df = spark.read.option("header", True).option("inferSchema", True).csv(input_csv_path)

# Hiển thị dữ liệu
print("Dữ liệu ban đầu:")
df.show()

# Bước 2: Xử lý dữ liệu (ví dụ lọc và nhóm)
# Lọc các row có 'value' > 15
filtered_df = df.filter(col("value") > 15)

# Nhóm theo 'category' và tính tổng 'value'
result_df = filtered_df.groupBy("category").agg(sum("value").alias("total_value"))

print("Dữ liệu sau xử lý:")
result_df.show()

# Bước 3: Lưu DataFrame ra file CSV
output_csv_path = 'processed_data'
result_df.coalesce(1).write.csv(output_csv_path, header=True, mode='overwrite')
print(f"Đã lưu dữ liệu ra thư mục {output_csv_path}.")

# Đọc lại file CSV vừa tạo (để dùng pandas tải vào PostgreSQL)
# Lưu ý: pandas sẽ đọc file part-xxx của thư mục CSV đã tạo
import glob

csv_files = glob.glob(f"{output_csv_path}/part-*.csv")
csv_file = csv_files[0]  # lấy file đầu tiên

# Bước 4: Đưa dữ liệu vào PostgreSQL
import pandas as pd
from sqlalchemy import create_engine

# Đường dẫn kết nối tới PostgreSQL (thay đổi theo cấu hình của bạn)
# Ví dụ: 'postgresql://username:password@localhost:5432/mydb'
postgresql_uri = 'postgresql://postgres:030201@localhost:5432/postgres'

# Tạo engine
engine = create_engine(postgresql_uri)

# Đọc file CSV bằng pandas
data = pd.read_csv(csv_file)

# Tải dữ liệu vào bảng PostgreSQL
# Thay 'your_table' bằng tên bảng bạn muốn
data.to_sql('yuchi_table', con=engine, if_exists='replace', index=False)
print("Đã tải dữ liệu vào PostgreSQL thành công.")

# Dừng Spark
spark.stop()
