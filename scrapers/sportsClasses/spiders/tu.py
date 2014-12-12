# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
from sportsClasses.items import SportsClassItem


class TuSpider(CrawlSpider):
    name = "tu"
    allowed_domains = ["www.tu-sport.de"]
    start_urls = ['http://www.tu-sport.de/index.php?id=2472']

    rules = [Rule(LinkExtractor(allow=['index.php\?id=2860.*']), callback='parseDetails')]

    def parseDetails(self, response):
        if u'Im Wintersemester sind keine' in response.body_as_unicode():
            return

        if u'Derzeit keine Angebote vorhanden.' in response.body_as_unicode():
            return

        sportsClass = SportsClassItem()
        sportsClass['url'] = response.url
        sportsClass['name'] = response.xpath("//h1/text()").extract()[0]
        sportsClass['description'] = "".join([part.strip() for part in response.xpath("//div[@class='contentstyle twocol']/*/text()").extract()[1:]])
        hxs = HtmlXPathSelector(response)
        tables = hxs.select("//tbody/tr")
        dates = []
        for row in tables:
            date = {}
            date["name"] = " ".join([p.strip() for p in row.select("./td[2]/*/text()").extract()])
            date["day"] = row.select("./td[5]/abbr/text()").extract()[0]

            try:
                date["time"] = row.select("./td[6]/text()").extract()[0]
            except IndexError:
                date["time"] = "Keine Angaben"
            place = row.select("./td[7]/descendant::*/text()").extract()
            if len(place) > 0:
                date["place"] = row.select("./td[7]/descendant::*/text()").extract()[0]
            else:
                date["place"] = row.select("./td[7]/text()").extract()[0]
            date["timeframe"] = row.select("./td[4]/text()").extract()[0]
            date["price"] = row.select("./td[9]/abbr/text()").extract()[0]
            date["bookable"] = row.select("./td[10]/*/text()").extract()[0].strip()

            dates.append(date)

        sportsClass['dates'] = dates
        return sportsClass


