import scrapy
import sqlite3
from scrapy.loader import ItemLoader
from ..items import ScrapItem
from w3lib.html import remove_tags
from itemloaders.processors import TakeFirst, MapCompose
from scrapy.exceptions import DropItem


##### spiders/scrapy_countries.py
#####################################
class ScrapyCountriesSpider(scrapy.Spider):
    name = "scrapy_countries"
    allowed_domains = ["www.scrapethissite.com"]
    start_urls = ["https://www.scrapethissite.com/pages/simple/"]

    def parse(self, response):
        items = ScrapItem()
        for country in response.css('div.country'):
            l = ItemLoader(item=ScrapItem(), selector=country)

            l.add_css('name', 'h3.country-name')
            l.add_css('capital', 'span.country-capital::text')
            l.add_css('population', 'span.country-population::text')

            yield l.load_item()


#### items.py
######################################
def to_strip(value):
    return value.strip()


def to_upper(value):
    return value.upper()


class ScrapItem(scrapy.Item):
    name = scrapy.Field(input_processor=MapCompose(remove_tags, to_strip, to_upper), output_processor=TakeFirst())
    capital = scrapy.Field(output_processor=TakeFirst())
    population = scrapy.Field(output_processor=TakeFirst())


#### pipelines.py
#######################################
class ScrapPipeline:
    def __init__(self):
        self.con = sqlite3.connect('countries.db')
        self.cur = self.con.cursor()
        self.create_table()

    def create_table(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS countries(
            name TEXT PRIMARY KEY, capital TEXT, population INTEGER
        )""")

    def process_item(self, item, spider):
        self.cur.execute("""
            INSERT OR IGNORE INTO countries VALUES (?, ?, ?)
        """, (item['name'], item['capital'], item['population']))
        self.con.commit()
        return item

class PopulationPipline:
    def process_item(self, item, spider):
        if int(item['population']) < 50000000:
            raise DropItem('population is less than 50M...')
        else:
            return item


##### settings.py
##########################################
ITEM_PIPELINES = {
   "scrap.pipelines.ScrapPipeline": 300,
   "scrap.pipelines.PopulationPipline": 200,
}
