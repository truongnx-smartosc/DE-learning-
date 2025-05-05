from google.cloud import bigquery

# Gán tên project, dataset, table đúng của bạn
project_id = 'top-broker-458809-c0'
dataset_id = 'my_dataset'
table_id = 'sale_table'

# Đường dẫn tới file CSV của bạn
csv_file_path = './SalesData.csv'

# Tạo client
client = bigquery.Client(project=project_id)

# Cấu hình load dữ liệu
job_config = bigquery.LoadJobConfig(
    source_format=bigquery.SourceFormat.CSV,
    skip_leading_rows=1,
    autodetect=True,
)

# Mở file CSV để upload
with open(csv_file_path, 'rb') as source_file:
    load_job = client.load_table_from_file(
        source_file,
        f"{project_id}.{dataset_id}.{table_id}",
        job_config=job_config
    )

load_job.result()  # chờ xong

print(f"Đã upload {load_job.output_rows} dòng vào {dataset_id}.{table_id}")
