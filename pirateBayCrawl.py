#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: ramonbeermann (aktualisiert)

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Join

class Torrent(scrapy.Item):
    url = scrapy.Field(output_processor=TakeFirst())
    tipo = scrapy.Field(output_processor=TakeFirst())
    torrentLink = scrapy.Field(output_processor=TakeFirst())
    size = scrapy.Field(output_processor=TakeFirst())
    description = scrapy.Field(output_processor=Join())
    seeders = scrapy.Field(output_processor=TakeFirst())
    leechers = scrapy.Field(output_processor=TakeFirst())
    category = scrapy.Field(output_processor=TakeFirst())
    upload_date = scrapy.Field(output_processor=TakeFirst())

class PirateBaySpider(CrawlSpider):
    name = 'thepiratebay'
    allowed_domains = ['thepiratebay.sx']
    start_urls = ['http://thepiratebay.sx/browse']
    
    rules = [Rule(LinkExtractor(allow=['/\d+']), callback='parse_torrent')]

    def parse_torrent(self, response):
        self.logger.info(f"Scraping: {response.url}")
        loader = ItemLoader(item=Torrent(), response=response)
        
        loader.add_value('url', response.url)
        loader.add_xpath('tipo', '//*[@id="searchResult"]/tr[1]/td[1]/center/a[2]//text()')
        loader.add_xpath('torrentLink', '//*[@id="searchResult"]/tr[1]/td[2]/a[2]/@href')
        loader.add_xpath('description', '//*[@id="searchResult"]/tr[1]/td[2]/div/a/@title')
        loader.add_xpath('size', '//*[@id="searchResult"]/tr[1]/td[2]/font/text()[2]')
        loader.add_xpath('seeders', '//*[@id="searchResult"]/tr[1]/td[3]/text()')
        loader.add_xpath('leechers', '//*[@id="searchResult"]/tr[1]/td[4]/text()')
        loader.add_xpath('category', '//*[@id="searchResult"]/tr[1]/td[1]/center/a[1]/text()')
        loader.add_xpath('upload_date', '//*[@id="searchResult"]/tr[1]/td[2]/font/text()[1]')

        return loader.load_item()
