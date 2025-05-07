from pyspark.sql import SparkSession
from pyspark.sql.functions import col  # Thêm dòng này

# Khởi tạo SparkSession
spark = SparkSession.builder.appName("Bai1_Filter").getOrCreate()

# Đọc dữ liệu CSV
df = spark.read.option("header", True).option("inferSchema", True).csv("sales_data.csv")

# Hiển thị dữ liệu ban đầu
print("=== Dữ liệu ban đầu ===")
df.show()

# Lọc theo điều kiện: quantity > 3
filtered_df = df.filter(col("quantity") > 3)

# In kết quả lọc
print("=== Dữ liệu sau lọc (quantity > 3) ===")
filtered_df.show()

# In rõ từng dòng
print("Dữ liệu sau lọc (quantity > 3):")
for row in filtered_df.collect():
    print(row)

# Dừng Spark
spark.stop()
