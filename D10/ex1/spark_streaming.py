from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, IntegerType

spark = SparkSession.builder.appName("KafkaSparkStream").getOrCreate()

# Định nghĩa schema của dữ liệu
schema = StructType().add("number", IntegerType())

# Đọc dữ liệu từ Kafka
df = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "stream_topic") \
    .load()

# Chuyển đổi dữ liệu nhị phân sang dạng JSON
json_df = df.selectExpr("CAST(value AS STRING) as json_str") \
    .select(from_json("json_str", schema).alias("data")) \
    .select("data.*")

# Hiển thị dữ liệu ra console
query = json_df.writeStream.outputMode("append").format("console").start()

query.awaitTermination()
