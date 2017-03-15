# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.exceptions import CloseSpider
from sportsClasses.items import SportsClassItem

def tryExtract(row, selector):
    name_list = row.select(selector).extract()
    if name_list:
        return name_list[0]
    else:
        return 'Keine Angaben'

def parseDetails(self, response):
    try:
        sportsClass = SportsClassItem()
        sportsClass['url'] = response.url
        sportsClass['name'] = response.xpath("//div[@class='bs_head']/text()").extract()[0]
        sportsClass['description'] = "\n".join(response.css(".bs_kursbeschreibung > p::text").extract())
        hxs = HtmlXPathSelector(response)
        tables = hxs.select("//table[@class='bs_kurse']/tbody/tr")
        dates = []
        for row in tables:
            date = {}

            date["name"] = tryExtract(row, "./td[2]/text()")

            date["day"] = tryExtract(row, "./td[3]/text()")

            date["time"] = tryExtract(row, "./td[4]/text()")

            date["place"] = tryExtract(row, "./td[5]/a/text()")

            date["timeframe"] = row.select("./td[6]/a/text()").extract()[0]

            priceList = row.select("./td[8]/div/text()").extract()
            if len(priceList) < 1:
                priceList = row.select("./td[8]/text()").extract()
            date['price'] = priceList[0]

            bookableList = row.select("./td[9]/input/@value")
            if len(bookableList) > 0:
                date["bookable"] = row.select("./td[9]/input/@value")[0].extract()
            else:
                date["bookable"] = row.select("./td[9]/span/text()").extract()[0]



            dates.append(date)

            sportsClass['dates'] = dates
        return sportsClass
    except Exception as e:
        raise CloseSpider(response.url)
