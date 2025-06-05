import scrapy

class NewspaperbotItem(scrapy.Item):
    title = scrapy.Field()
    cate = scrapy.Field()
    content = scrapy.Field()
    author = scrapy.Field()
    publication_date = scrapy.Field()
    source_url = scrapy.Field()
