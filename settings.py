BOT_NAME = 'StageTest'

SPIDER_MODULES = ['StageTest.spiders']
NEWSPIDER_MODULE = 'StageTest.spiders'

# Добавляем Middleware для обработки прокси
DOWNLOADER_MIDDLEWARES = {
    'middlewares.ProxyRotationMiddleware': 350,
}
