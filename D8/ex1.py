from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum

spark = SparkSession.builder.appName("Exercise1").getOrCreate()

df = spark.read.option("header", True).option("inferSchema", True).csv("data.csv")

df.show()

filtered_df = df.filter(col("value") > 15)

filtered_df.show()

grouped_df = filtered_df.groupBy("category").agg(sum("value").alias("total_value"))

grouped_df.show()

spark.stop()
