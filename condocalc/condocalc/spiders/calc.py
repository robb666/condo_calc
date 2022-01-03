import scrapy

class PostsSpider(scrapy.Spider):
    name = 'posts'

    start_urls = [
        'portal.generali.pl',
        'https://serwis.uniqa.pl/partner',
        'eagent.warta.pl'
    ]

    def parse(self, response): pass
