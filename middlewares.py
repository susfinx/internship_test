from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
import random
from scrapy import signals
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import TCPTimedOutError

class ProxyRotationMiddleware(HttpProxyMiddleware):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.proxies = []

    @classmethod
    def from_crawler(cls, crawler):
        middleware = super().from_crawler(crawler)
        crawler.signals.connect(middleware.spider_opened, signal=signals.spider_opened)
        return middleware

    def spider_opened(self, spider):
        # Здесь можно загрузить список прокси из файла или из какого-либо источника
        with open('proxy_list.txt', 'r') as file:
            proxy_list = [line.strip() for line in file]
            self.proxies = proxy_list

    def process_request(self, request, spider):
        if 'proxy' not in request.meta:
            if self.proxies:
                selected_proxy = random.choice(self.proxies)
                print(f"Using proxy: {selected_proxy} for URL: {request.url}")
                request.meta['proxy'] = selected_proxy
            else:
                raise Exception("Список прокси-серверов исчерпан. Коннект не удался.")

    def process_exception(self, request, exception, spider):
        if isinstance(exception, (HttpError, TCPTimedOutError)):
            # Проверяем, если это ошибка HTTP 403 или ошибка TCP timeout
            if isinstance(exception, HttpError) and exception.response.status == 403:
                spider.logger.debug(f"Received 403 Forbidden for {request.url}")
            # Повторяем запрос с новым прокси
            return self._retry(request, exception, spider)

    def _retry(self, request, exception, spider):
        if 'proxy' in request.meta:
            current_proxy = request.meta['proxy']
            if current_proxy in self.proxies:
                self.proxies.remove(current_proxy)  # Удаляем текущий прокси из списка
                if self.proxies:
                    selected_proxy = random.choice(self.proxies)
                    print(f"Switching to proxy: {selected_proxy} for URL: {request.url}")
                    request.meta['proxy'] = selected_proxy
                    return request
                else:
                    raise Exception("Список прокси-серверов исчерпан. Коннект не удался.")
        return None

