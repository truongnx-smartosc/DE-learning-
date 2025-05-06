from pyspark.sql import SparkSession

# Khởi tạo SparkSession
spark = SparkSession.builder.appName("Bai1").getOrCreate()

# Đọc file CSV
df = spark.read.option("header", True).csv("sales_data.csv")

# Hiển thị dữ liệu
df.show()

# In schema
df.printSchema()

# Dừng Spark
spark.stop()
