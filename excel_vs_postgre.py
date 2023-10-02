# -*- coding: utf-8 -*-

import pandas as pd
import psycopg2
import numpy as np

# Параметры подключения к базе данных PostgreSQL
db_host = 'localhost'
db_port = '5432'
db_name = 'attis_new'
db_user = 'postgres'
db_password = 'S?6wTGk2xQK7J`V5'

# Путь к файлу Excel
excel_file = '1.xls'

# Чтение данных из Excel
data_frame = pd.read_excel(excel_file)

# Установка соединения с базой данных PostgreSQL
conn = psycopg2.connect(
    host=db_host,
    port=db_port,
    dbname=db_name,
    user=db_user,
    password=db_password
)

# Создание объекта "курсор" для выполнения SQL-запросов
cursor = conn.cursor()

# SQL-запрос для создания таблицы Excel
create_table_query = '''
CREATE TABLE Excel (
    "Организация" TEXT,
    "Регион" TEXT,
    "ИНН" TEXT,
    "Номер телефона" TEXT,
    "Номер телефона 2" TEXT,
    "Номер телефона 3" TEXT,
    "Дата звонка" DATE,
    "Итоговый результат" TEXT,
    "Комментарий" TEXT
)
'''

# Создание таблицы Excel
cursor.execute(create_table_query)

# Импорт данных в таблицу PostgreSQL
for index, row in data_frame.iterrows():
    # Замена значений NaT на None
    row = row.replace({pd.NaT: None, np.nan: None})
    # Формируем SQL-запрос для вставки данных
    query = "INSERT INTO Excel (\"Организация\", \"Регион\", \"ИНН\", \"Номер телефона\", \"Номер телефона 2\", \"Номер телефона 3\", \"Дата звонка\", \"Итоговый результат\", \"Комментарий\") VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = (
        row['Организация'], row['Регион'], row['ИНН'],
        row['Номер телефона'], row['Номер телефона 2'],
        row['Номер телефона 3'], row['Дата звонка'],
        row['Итоговый результат'], row['Комментарий'])  # Замени column1, column2 и column3 на реальные имена столбцов

    # Выполняем SQL-запрос
    cursor.execute(query, values)

# Фиксируем изменения в базе данных
conn.commit()

# Закрываем курсор и соединение
cursor.close()
conn.close()

print("Импорт данных из Excel в PostgreSQL выполнен успешно.")
