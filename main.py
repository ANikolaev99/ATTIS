# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# Делает dump базы attis на PostgreSQL и отсылает dump в S3 AWS два раза в день в 12 и 18
# Для выполнения данной задачи используем библиотеки psycopg2 для взаимодействия с PostgreSQL
# и boto3 для работы с Amazon S3 в AWS

import os
import subprocess
import datetime
#import psycopg2
import boto3
import tempfile
from botocore.exceptions import NoCredentialsError

# Параметры для подключения к PostgreSQL
db_params = {
    "dbname": "attis",
    "user": "postgres",
    "password": "5F9pXB0DsabqgVzLL6rK",
    "host": "localhost",
    "port": "5432"
}

# Параметры для подключения к Amazon S3
s3_bucket_name = "attistrade"
aws_access_key = "AKIA53F5EPHUHIM33EJO"
aws_secret_key = "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"

# Путь для сохранения дампа базы данных
#dump_file_path = r"D:\New Work\Temp\dump.sql"

def create_postgresql_dump():
    pg_dump_path = r"D:\Program Files\PostgreSQL\11\bin\pg_dump.exe"
    dump_file_path = tempfile.NamedTemporaryFile(delete=False).name
    dump_command = f'{pg_dump_path} -h {db_params["host"]} -p {db_params["port"]} -U {db_params["user"]} -d {db_params["dbname"]} -F c -f "{dump_file_path}"'
    print("Running dump command:", dump_command)
    subprocess.call(dump_command, shell=True)
    print("PostgreSQL dump created.")
    #with tempfile.NamedTemporaryFile(delete=False) as temp_file:
    #    dump_command = f'{pg_dump_path} -h {db_params["host"]} -p {db_params["port"]} -U {db_params["user"]} -d {db_params["dbname"]} -F c -f "{temp_file.name}"'
    #    print("Running dump command:", dump_command)
    #    subprocess.call(dump_command, shell=True)
    #    print("PostgreSQL dump created.")
    return dump_file_path

def upload_to_s3(file_path, s3_key):
    #s3_subfolder = "test/"
    #s3_key = "dump.sql"
    #full_s3_key = s3_subfolder + s3_key
    print(f"Uploading to S3 - File: {file_path}, Key: {s3_key}")
    s3 = boto3.client(
        "s3",
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key
    )
    try:
        s3.upload_file(file_path, s3_bucket_name, s3_key)
        print("Upload successful")
    except NoCredentialsError:
        print("Credentials not available")
    except Exception as e:
        print(f"Error uploading to S3: {e}")

def main():
    temp_file_path = create_postgresql_dump()
    current_hour = datetime.datetime.now().hour
    #s3_key = f"dump_{datetime.datetime.now().hour}.sql"
    s3_key = f"test/dump_{current_hour}.sql"  # Include "test/" in the key
    upload_to_s3(temp_file_path, s3_key)
    os.remove(temp_file_path)

if __name__ == "__main__":
    main()
