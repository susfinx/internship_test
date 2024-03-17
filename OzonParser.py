import scrapy
from scrapy import Request
from scrapy.crawler import CrawlerProcess
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pandas as pd
from fake_useragent import UserAgent
import os
import time
from scrapy.exceptions import IgnoreRequest
#import subprocess

class OzonSmartphonesSpider(scrapy.Spider):
    name = 'ozon_smartphones'
    start_urls = ['https://www.ozon.ru/category/telefony-i-smart-chasy-15501/?from_global=true&sort=rating']

    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'DOWNLOAD_DELAY': 2,  # Задержка между запросами в секундах
        'RANDOMIZE_DOWNLOAD_DELAY': True,  # Случайное добавление дополнительной задержки для каждого запроса
    }

    def __init__(self):
        # Настройка Selenium
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Запуск браузера в фоновом режиме
        self.service = Service(
            'C:\\Users\\sx\\Downloads\\chromedriver_win64\\chromedriver.exe')  # Укажите путь к chromedriver
        self.driver = webdriver.Chrome(service=self.service, options=chrome_options)
        self.ua = UserAgent()

    def start_requests(self):
        random_user_agent = self.ua.random
        for url in self.start_urls:
            yield Request(url, callback=self.parse, headers={'User-Agent': random_user_agent})

    def parse(self, response):
        # Проверка на блокировку сервера
        if response.status == 403:
            self.logger.error("Сервер блокирует доступ: %s", response.url)
            return  # Прерываем обработку этой страницы

        smartphone_links = response.css('.a0c6 .a0v4 ::attr(href)').getall()[:100]
        for link in smartphone_links:
            yield Request(link, callback=self.parse_smartphone_page)

process = CrawlerProcess(settings={
    'DOWNLOADER_MIDDLEWARES': {
        'middlewares.ProxyRotationMiddleware': 543,
        # Другие middleware...
    },
    'PROXY_ENABLED': True,
})

process.crawl(OzonSmartphonesSpider)
process.start()



csv_file_path = 'ozon_smartphones.csv'
max_attempts = 20  # Максимальное количество попыток
attempt = 0

while attempt < max_attempts:
    if os.path.exists(csv_file_path) and os.stat(csv_file_path).st_size > 0:
        # Если файл существует и не пустой, считываем данные и выходим из цикла
        try:
            df = pd.read_csv(csv_file_path)
            distribution = df['OS Version'].value_counts()

            # Сохранение результатов в plain-text формате
            with open('os_distribution.txt', 'w') as f:
                for index, value in distribution.items():
                    f.write(f'{index} — {value}\n')

            break
        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")
    else:
        # Если файл не существует или пустой, ждем некоторое время
        print(f"Файл '{csv_file_path}' еще не содержит данных. Подождите...")
        time.sleep(5)  # Ждем 5 секунд перед следующей попыткой
        attempt += 1
else:
    print(f"Файл '{csv_file_path}' не был найден или остается пустым после {max_attempts} попыток.")
