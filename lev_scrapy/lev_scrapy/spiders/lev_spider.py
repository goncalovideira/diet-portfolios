import scrapy


class LevSpiderSpider(scrapy.Spider):
    name = 'lev_spider'
    allowed_domains = ['lev.pt', 'levcms.live.afonso.se']
    start_urls = ['https://levcms.live.afonso.se/wp-json/wc/v3/products?include=325,314,190,468,346,184,3669,324&per_page=100&page=1&catalog_visibility=visible']

    def parse(self, response):
        pass
