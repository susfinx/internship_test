import requests

api_key = 'fRxs4plHp801WsgmsyUtc6Fkg2Mtg7lx'
url = 'https://magicproxy.net/api'
params = {
    'api_key': api_key,
    'country': 'ru',  # Страна (необязательный параметр)
    'type': 'http',  # Тип прокси (необязательный параметр)
    'latency': 7000  # Максимальная задержка (необязательный параметр)
}

response = requests.get(url, params=params)

if response.status_code == 200:
    print("Текст ответа:")
    print(response.text)

    # Разбиваем ответ на строки и добавляем префикс перед каждой записью
    proxy_list = [f'http://{proxy}' for proxy in response.text.split('\n') if proxy.strip()]

    with open('proxy_list.txt', 'w') as file:
        for proxy in proxy_list:
            file.write(proxy + '\n')

    print("Список прокси сохранен в файле 'proxy_list.txt'")
else:
    print(f"Произошла ошибка при выполнении запроса: {response.status_code}")
