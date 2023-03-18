from concurrent.futures import ThreadPoolExecutor
from coindesk.models import Coindesk

class CoindeskSpiderPipeline:
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=1)

    def close_spider(self, spider):
        self.executor.shutdown()

    def process_item(self, item, spider):
        coindesk_article = Coindesk()

        coindesk_article.category = item['category']
        coindesk_article.title = item['title']
        coindesk_article.author = item['author']
        coindesk_article.date = item['date']
        coindesk_article.content = " ".join(item['content'])

        self.executor.submit(coindesk_article.save)
        return item
