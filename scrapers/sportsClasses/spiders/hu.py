# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
from sportsClasses.items import SportsClassItem
import sportsSpider

class HuSpider(CrawlSpider):
    name = "hu"
    allowed_domains = ["zeh2.zeh.hu-berlin.de"]
    start_urls = (
        'http://zeh2.zeh.hu-berlin.de/sportarten/aktueller_zeitraum/index.html',
    )

    rules = [Rule(LinkExtractor(allow=['_.+\.html']), callback='parseDetails')]

    def parseDetails(self, response):
        return sportsSpider.parseDetails(self, response)
