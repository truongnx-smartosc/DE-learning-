from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum
import pandas as pd
from sqlalchemy import create_engine

spark = SparkSession.builder.appName("Exercise2").getOrCreate()

input_csv_path = 'data.csv'  
df = spark.read.option("header", True).option("inferSchema", True).csv(input_csv_path)

print("Dữ liệu ban đầu:")
df.show()

filtered_df = df.filter(col("value") > 15)

result_df = filtered_df.groupBy("category").agg(sum("value").alias("total_value"))

print("Dữ liệu sau xử lý:")
result_df.show()

output_csv_path = 'processed_data'
result_df.coalesce(1).write.csv(output_csv_path, header=True, mode='overwrite')
print(f"Đã lưu dữ liệu ra thư mục {output_csv_path}.")

import glob

csv_files = glob.glob(f"{output_csv_path}/part-*.csv")
csv_file = csv_files[0]   

import pandas as pd
from sqlalchemy import create_engine


postgresql_uri = 'postgresql://postgres:030201@localhost:5432/postgres'

engine = create_engine(postgresql_uri)

data = pd.read_csv(csv_file)

data.to_sql('yuchi_table', con=engine, if_exists='replace', index=False)
print("Đã tải dữ liệu vào PostgreSQL thành công.")

spark.stop()
