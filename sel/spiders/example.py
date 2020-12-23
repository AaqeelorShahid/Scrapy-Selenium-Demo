# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.keys import Keys


class ExampleSpider(scrapy.Spider):
    name = 'example'
    def start_requests(self):
        yield SeleniumRequest(
            url = 'https://www.duckduckgo.com',
            wait_time=3,
            screenshot=True,
            callback=self.parse
        )

    def parse(self, response):
        # image = response.meta['screenshot']

        # with open ('screenshot.png', 'wb') as f:
        #     f.write(image)

        driver = response.meta['driver']
        search_input = driver.find_element_by_xpath("//input[@id='search_form_input_homepage']")
        search_input.send_keys("My User Agent")
        driver.save_screenshot("After_filling.png")

        search_btn = driver.find_element_by_xpath("//input[@id='search_button_homepage']")
        search_btn.send_keys(Keys.ENTER)
        driver.save_screenshot("After_Searching.png")

        html = driver.page_source
        res_obj = Selector(text=html)

        links = res_obj.xpath("//a[contains(@class, 'result__url')]")

        for link in links:
            yield{
                "URL": link.xpath(".//@href").get()
            }

