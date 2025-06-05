import scrapy
from urllib.parse import urljoin
from newspaperbot.items import NewspaperbotItem

class CnnSpider(scrapy.Spider):
    name = 'cnn'
    allowed_domains = ['edition.cnn.com']
    start_urls = [
        'https://edition.cnn.com/sport',
        'https://edition.cnn.com/sport/football',
        'https://edition.cnn.com/sport/tennis',
        'https://edition.cnn.com/sport/us-sports',
        'https://edition.cnn.com/sport/paris-olympics-2024',
        'https://edition.cnn.com/entertainment',
        'https://edition.cnn.com/entertainment/movies',
        'https://edition.cnn.com/entertainment/tv-shows',
        'https://edition.cnn.com/entertainment/celebrities',
        'https://edition.cnn.com/health',
        'https://edition.cnn.com/health/life-but-better/fitness',
        'https://edition.cnn.com/health/life-but-better/food',
        'https://edition.cnn.com/health/life-but-better/sleep',
        'https://edition.cnn.com/health/life-but-better/mindfulness',
        'https://edition.cnn.com/health/life-but-better/relationships',
        'https://edition.cnn.com/business',
        'https://edition.cnn.com/business/tech',
        'https://edition.cnn.com/business/media',
        'https://edition.cnn.com/business/financial-calculators',
        'https://edition.cnn.com/style',
        'https://edition.cnn.com/style/arts',
        'https://edition.cnn.com/style/design',
        'https://edition.cnn.com/style/fashion',
        'https://edition.cnn.com/style/architecture',
        'https://edition.cnn.com/style/beauty'
    ]

    def parse(self, response):
        url = response.url
        if '/sport' in url:
            cate = 'sport'
        elif '/entertainment' in url:
            cate = 'entertainment'
        elif '/health' in url:
            cate = 'health'
        elif '/business' in url:
            cate = 'business'
        elif '/style' in url:
            cate = 'style'
        else:
            cate = 'other' 
        articles = response.css('a::attr(href)').getall()
        articles = [a for a in articles if '/202' in a]  # Chỉ lấy link bài viết

        # cate = response.url.split('/')[-1]
        for article in articles:
            url = urljoin(response.url, article)
            yield scrapy.Request(url, callback=self.parse_article, meta={'cate': cate})

    def parse_article(self, response):
        article = NewspaperbotItem()

        # Title
        article['title'] = (
            response.css('h1::text').get()
            or response.xpath('//h1/text()').get()
        )

        # Author
        article['author'] = (
            response.css('meta[name="author"]::attr(content)').get()
            or 'CNN'
        )

        # Published time
        article['publication_date'] = response.css('meta[property="article:published_time"]::attr(content)').get()

        # Nội dung bài viết
        paragraphs = response.css('div.article__content p::text').getall()
        if not paragraphs:
            paragraphs = response.css('section p::text').getall()
        if not paragraphs:
            paragraphs = response.xpath('//article//p/text()').getall()

        content = ' '.join(p.strip() for p in paragraphs if p.strip())

        # Chỉ yield nếu đủ dữ liệu quan trọng
        if article['title'] and content:
            article['cate'] = response.meta['cate']
            article['content'] = content
            article['source_url'] = response.url
            yield article

# import scrapy
# from scrapy.spiders import CrawlSpider, Rule
# from scrapy.linkextractors import LinkExtractor
# from scrapy.item import Item, Field
# from newspaperbot.items import Article

# class CNNSpider(scrapy.Spider):
#     name = "cnn"
#     allowed_domains = ['edition.cnn.com']
#     start_urls = ['https://edition.cnn.com/']

#     # Extracts all the links for the categories
#     def parse(self, response):
#         for href in response.xpath('//div[@class="header__nav-item"]//a/@href'):
#             url = response.urljoin(href.extract())
#             yield scrapy.Request(url, callback = self.getCategory)
        
#     # Extracts all the links for the articles in the categories
#     def getCategory(self, response):
#         fetched_category = response.xpath('//head/meta[@name="meta-section"]/@content').get()

#         # iterate through all the categories
#         for href in response.xpath('//a[@class="container__link container__link--type-article container_lead-plus-headlines__link"]/@href').getall():
#             url = response.urljoin(href)

#             # Checks if the category is in not in DB and if it is not, then returns None
#             if fetched_category == 'video' or fetched_category == 'cnn-underscored':
#                 yield None
#             else:      
#                 yield scrapy.Request(url, callback = self.getArticle)
                
#     # Extracts all the information from the article
#     def getArticle(self, response):
#         item = Article()
        
#         item['name'] = response.xpath('//head/meta[@property="og:title"]/@content').get()
#         item['author'] = response.xpath('//head/meta[@name="author"]/@content').get() or 'cnn'
#         item['publication_date'] = response.xpath('//head/meta[@property="article:published_time"]/@content').get()
#         item['body'] = response.xpath('//p[contains(@class, "paragraph inline-placeholder")]//text()').getall()

#         if not item['body']:
#             return None

#         # cleaning up the body, removing line breaks, empty items and whitespace
#         for i in reversed(range(len(item['body']))):
#             text = item['body'][i].replace("\n", "").strip()
#             item['body'][i] = text

#             # removing empty items from list
#             if len(item['body'][i]) == 0:
#                 del item['body'][i]

#         # merging links into paragraphs
#         for i in reversed(range(len(item['body']))):
#             text = item['body'][i]
#             if (text[len(text)-1] != "." and text[len(text)-1] != '"' and i+1 != len(item['body'])):
#                 item['body'][i] = text + " " + item['body'][i+1]
#                 del item['body'][i+1]

#         category = response.xpath('//head/meta[@name="meta-section"]/@content').get()

#         # reassign category and get rids of unwanted categories
#         if category == 'us':
#             category = 'world'
#         elif category == 'cnn-underscored':
#             # do not return item
#             return None 
        
#         item['category'] = category
        
#         item['source_url'] = response.url
#         item['cover_url'] = response.xpath('//head/meta[@property="og:image"]/@content').get()

#         # Checks for different layouts
#         if response.xpath('//div[@class="gallery-inline__container"]'):
#             item['body'] = response.xpath('//span[@class="inline-placeholder"]/text()').getall()
#             # item['cover_url'] = response.xpath('//picture[@class="image_gallery-image__picture"]/img/@src').getall()
        
#         if not item['body']:
#             item['body'] = response.xpath('//head/meta[@name="description"]/@content').get()
        
#         # print(item)
#         yield item