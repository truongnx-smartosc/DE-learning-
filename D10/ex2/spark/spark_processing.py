# spark/spark_processing.py

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, LongType

# Khởi tạo SparkSession
spark = SparkSession.builder \
    .appName("KafkaSparkProcessor") \
    .getOrCreate()

# Định nghĩa schema của dữ liệu
schema = StructType([
    StructField("id", IntegerType(), True),
    StructField("value", StringType(), True),
    StructField("timestamp", LongType(), True)
])

# Đọc dữ liệu từ Kafka
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "my_data_topic") \
    .load()

# Chuyển dữ liệu sang dạng có thể xử lý
json_df = df.selectExpr("CAST(value AS STRING) as json_value") \
    .select(from_json("json_value", schema).alias("data")) \
    .select("data.*")

# Xử lý dữ liệu: ví dụ in ra, hoặc lưu vào database
query = json_df.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

query.awaitTermination()
