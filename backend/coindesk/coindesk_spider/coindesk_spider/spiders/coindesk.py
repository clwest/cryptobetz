import scrapy
from coindesk_spider.items import CoindeskSpiderItem
from datetime import datetime
from dateutil import parser
from scrapy import Spider, signals
import os
import sys



import django

sys.path.append('/Users/chriswest/Development/CryptoBetz/backend')

os.environ['DJANGO_SETTINGS_MODULE'] = 'crypto_project.settings'

django.setup()

class CoindeskSpider(scrapy.Spider):
    name = "coindesk"
    allowed_domains = ["www.coindesk.com"]

    def __init__(self, tag=None, *args, **kwargs):
        super(CoindeskSpider, self).__init__(*args, **kwargs)
        self.start_urls = [f"https://www.coindesk.com/tag/{tag}"]

    def parse(self, response):
        links = response.xpath("//div[@class='article-cardstyles__AcTitle-q1x8lc-1 bzAuaw articleTextSection ']")
        for link in links:
            article_url = link.xpath("./h6/a/@href").get()
            if "podcast" in article_url or "video" in article_url or "indices" in article_url:
                continue
            yield response.follow(article_url, callback=self.parse_article)

        next_page = response.css('[rel="next"] ::attr(href)').get()      
        if next_page is not None:
            next_page_url = response.urljoin(next_page)
            yield response.follow(next_page_url, callback=self.parse)

    def parse_article(self, response):
        article_item = CoindeskSpiderItem()
        article_item['category'] = response.xpath("//div[@class='at-category']//span/text()").get()
        article_item['title'] = response.xpath("//div[@class='at-headline']//h1/text()").get()
        article_item['author'] = response.xpath("//div[@class='at-authors']//a/text()").get()
        article_item['date'] = response.xpath("//div[@class='at-created label-with-icon']//span/text()").get()
        article_item['content'] = response.xpath("//div[@class='typography__StyledTypography-owin6q-0 bYmaON at-text']/p/text()").getall()
        article_item['url'] = response.url
        
        date_str = response.css('time::attr(datetime)').get()
        
        if date_str is not None:
            date_obj = parser.parse(date_str)
            formatted_date = date_obj.strftime('%Y-%m-%d %H:%M:%S%z')
        else:
            formatted_date = None
            self.logger.warning("Failed to extract date string from the article at %s", response.url)

        article_item['date'] = formatted_date
        yield article_item


