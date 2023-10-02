import pandas as pd
import requests
import re

# Загрузите данные из файла Excel
df = pd.read_excel('1.xls')

# Создайте новый столбец "Адрес" и инициализируйте его пустыми значениями
df['Адрес'] = ''

# Функция для получения адреса по ИНН
def get_address(inn, api_key):
    # URL API ФНС
    url = 'https://api-fns.ru/api/egr'

    # Параметры запроса
    params = {
        'req': inn,
        'key': api_key
    }

    try:
        # Отправляем GET-запрос к API ФНС
        response = requests.get(url, params=params)

        # Проверяем статус ответа
        if response.status_code == 200:
            # Используем регулярное выражение для поиска "АдресПолн"
            address_match = re.search(r'"АдресПолн":"([^"]+)"', response.text)

            if address_match:
                address = address_match.group(1)
                return address

            return "АдресПолн не найден в ответе."

        else:
            # Если возникла ошибка, возвращаем статус код и текст ошибки
            return f"Ошибка {response.status_code}: {response.text}"
    except Exception as e:
        # Если произошла какая-либо другая ошибка, возвращаем сообщение об ошибке
        return f"Произошла ошибка: {str(e)}"

# Пройдитесь по строкам DataFrame и получите адресы
for index, row in df.iterrows():
    inn = str(row['ИНН'])
    api_key = '94dec2b946240190f780835300237c2d7fb7b5b3'  # Замените на ваш ключ API ФНС

    # Получите адрес по ИНН и обновите столбец "Адрес"
    address = get_address(inn, api_key)
    df.at[index, 'Адрес'] = address

# Сохраните обновленный DataFrame в новый файл Excel
df.to_excel('1_with_addresses.xls', index=False)
