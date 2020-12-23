# -*- coding: utf-8 -*-
import scrapy
from scrapy_selenium import SeleniumRequest

class DealsSpider(scrapy.Spider):
    name = 'deals'

    def start_requests(self):
        yield SeleniumRequest(
            url = "https://slickdeals.net/computer-deals",
            callback = self.parse,
            wait_time= 3,
        )

    def parse(self, response):
        items = response.xpath ("//ul/li[contains(@class, 'fpGridBox ')]")
        for item in items:
            yield{
                'Name': item.xpath(".//a[contains(@class, 'itemTitle ')]/text()").get(),
                'Link': item.xpath(".//a[contains(@class, 'itemTitle ')]/@href").get(),
                'Price': item.xpath("normalize-space(.//div[contains(@class, 'itemPrice ')]/text())").get(),
            }
        
        next_page = response.xpath("//a[@data-role='next-page']/@href").get()

        if next_page:
            absolute_url = f"https://slickdeals.net{next_page}"
            yield SeleniumRequest(
                url = absolute_url,
                callback = self.parse,
                wait_time= 3
            )
