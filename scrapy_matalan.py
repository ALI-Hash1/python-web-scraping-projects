from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re


class ScrapyMatalanSpider(CrawlSpider):
    name = "scrapy_matalan"
    allowed_domains = ["www.matalan.co.uk"]
    start_urls = ["https://www.matalan.co.uk/mens/suits.list"]

    rules = [
        Rule(LinkExtractor(allow=re.compile(r"/clothing/taylor-wright-*")), callback="parse_item", follow=True)
    ]

    def parse_item(self, response):
        item = {}
        item['product_id'] = response.xpath(
            '/html/body/div[1]/div[5]/div/main/div/div/div[3]/div/div[1]/div/div[2]/div/section/div/div[4]/div/text()').get()
        return item
