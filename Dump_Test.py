# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# Делает dump базы attis на PostgreSQL и отсылает dump в S3 AWS два раза в день в 12 и 18
# Для выполнения данной задачи используем библиотеки psycopg2 для взаимодействия с PostgreSQL
# и boto3 для работы с Amazon S3 в AWS

import os
import subprocess
import datetime
import boto3
import tempfile
from botocore.exceptions import NoCredentialsError
import shutil

# Параметры для подключения к PostgreSQL
db_params = {
    "dbname": "attis_new",
    "user": "postgres",
    "password": "S?6wTGk2xQK7J`V5",
    "host": "localhost",
    "port": "5432"
}

# Параметры для подключения к Amazon S3
s3_bucket_name = "attistrade"
aws_access_key = "AKIA53F5EPHUHIM33EJO"
aws_secret_key = "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"

def create_postgresql_dump(file_path):
    dump_command = [
        r'C:\Program Files\PostgreSQL\11\bin\pg_dump.exe',
        '-h', db_params['host'],
        '-p', db_params['port'],
        '-U', db_params['user'],
        '-d', db_params['dbname'],
        '-F', 'c',
        '-f', file_path
    ]
    print("Running dump command:", ' '.join(dump_command))

    try:
        result = subprocess.run(dump_command, capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            print("PostgreSQL dump created.")
        else:
            print("Error executing dump command. Exit code:", result.returncode)
            print("Error message:", result.stderr)
    except subprocess.CalledProcessError as e:
        print("Error executing dump command:", e)

create_postgresql_dump('C:\\Temp\\manual_dump.sql')

def upload_to_s3(file_path, s3_key):
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
    temp_dir = r"C:\Temp"  # Замените на директорию, где у вас нет специальных символов в пути
    temp_file_path = os.path.join(temp_dir, 'manual_dump.sql')
    create_postgresql_dump(temp_file_path)
    current_hour = datetime.datetime.now().hour
    s3_key = f"test/dump_{current_hour}.sql"  # Include "test/" in the key
    upload_to_s3(temp_file_path, s3_key)
    os.remove(temp_file_path)

if __name__ == "__main__":
    main()
