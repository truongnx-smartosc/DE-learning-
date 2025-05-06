from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum
import pandas as pd
from sqlalchemy import create_engine
import glob
import os

# Khởi tạo SparkSession
spark = SparkSession.builder.appName("Exercise2").getOrCreate()

# 1. Đọc dữ liệu CSV gốc
input_csv_path = 'sales_data.csv'  # Thay bằng đường dẫn thực tế của bạn
df = spark.read.option("header", True).option("inferSchema", True).csv(input_csv_path)
print("Dữ liệu ban đầu:")
df.show()

# 2. Xử lý dữ liệu
result_df = df.groupBy("category").agg(
    sum("quantity").alias("total_quantity"),
    sum("total_price").alias("total_revenue")
)
print("Dữ liệu sau xử lý (tổng doanh thu theo category):")
result_df.show()

# 3. Lưu dữ liệu ra file CSV
output_dir = 'processed_data'
result_df.coalesce(1).write.csv(output_dir, header=True, mode='overwrite')
print(f"Dữ liệu đã lưu tại thư mục: {output_dir}")

# 4. Lấy file CSV duy nhất
csv_files = glob.glob(f"{output_dir}/part-*.csv")
processed_csv_path = csv_files[0]
print(f"File CSV đã tạo: {processed_csv_path}")

# 5. Đọc file CSV với pandas
data = pd.read_csv(processed_csv_path)

# 6. Kết nối tới PostgreSQL
# Thay đổi theo cấu hình của bạn
postgresql_uri = 'postgresql://postgres:030201@localhost:5432/postgres'
engine = create_engine(postgresql_uri)

# 7. Tải dữ liệu vào PostgreSQL
table_name = 'sales_summary'
data.to_sql(table_name, con=engine, if_exists='replace', index=False)
print(f"Dữ liệu đã được load vào bảng '{table_name}' trong PostgreSQL.")

# **Evidence 1: In ra dữ liệu đã lưu trên console**
print("\n=== DỮ LIỆU ĐÃ LƯU VÀO POSTGRESQL ===")
print(data)

# Dừng Spark
spark.stop()
