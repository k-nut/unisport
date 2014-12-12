# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
from sportsClasses.items import SportsClassItem
import sportsSpider

class HtwSpider(CrawlSpider):
    name = "htw"
    allowed_domains = ["sport.htw-berlin.de"]
    start_urls = (
        'http://sport.htw-berlin.de/angebote/aktueller_zeitraum/index.html',
    )

    rules = [Rule(LinkExtractor(allow=['_.+\.html']), callback='parseDetails')]

    def parseDetails(self, response):
        return sportsSpider.parseDetails(self, response)
