import os
import requests


# API DaData
DADATA_API_KEY = os.getenv('DADATA_API_KEY')
DADATA_URL = 'https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/address'

def validate_and_correct_address(address):
    """
    Валидация адреса
    """

    # запрос к API DaData
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Token {DADATA_API_KEY}'
    }
    data = {
        'query': address,
    }
    response = requests.post(DADATA_URL, headers=headers, json=data)

    # проверка статуса ответа
    if response.status_code == 200:
        # получение списка подходящих адресов
        suggestions = response.json().get('suggestions', [])
        if suggestions:
            # выбор первого подходящего адреса
            corrected_address = suggestions[0]['value']

            # получение координат
            geo_data = suggestions[0]['data']
            lat = geo_data.get('geo_lat')
            lon = geo_data.get('geo_lon')

            if lat and lon:
                return corrected_address, (float(lat), float(lon))

    return None, (None, None)