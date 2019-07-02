# -*- coding: utf-8 -*-
import scrapy
import json
from ..items import BarronItem
import re
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd


class BarronfetchSpider(scrapy.Spider):
    name = 'barronfetch'
    custom_settings = {
        'ITEM_PIPELINES': {
            'barron.pipelines.BarronfetchPipeline': 400
                },
        'HTTPCACHE_ENABLED': True
            }
    header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
            }
    start_urls = ['https://accounts.barrons.com/login?opts=0&target=https%3A%2F%2Fwww.barrons.com%2F']
    def parse(self, response):
        options = webdriver.FirefoxOptions()
        options.add_argument('-headless')
        driver = webdriver.Firefox(firefox_options=options)
        driver.get('https://accounts.barrons.com/login?opts=0&target=https%3A%2F%2Fwww.barrons.com%2F')
        inputemail = driver.find_element_by_name("username")
        inputpwd = driver.find_element_by_name('password')
        inputemail.send_keys("jameswong1974cc@gmail.com")
        inputpwd.send_keys('531720cc')
        inputpwd.submit()
        try:
            WebDriverWait(driver, 60).until(EC.title_contains("Verify your Email Address"))
        finally:
            cookie = driver.get_cookies()
            print(cookie,'+++++++++++++++++++++++++++++++++')
            sreach_window=driver.current_window_handle
            time.sleep(5)
            driver.find_element_by_id("brand-label").click()
            driver.quit()
            yield scrapy.Request(url='https://www.barrons.com/',callback=self.parse_list,cookies=cookie,headers=BarronfetchSpider.header,meta={'dont_cache':True})
    def parse_list(self,response):
        data = pd.read_csv('output.csv', sep='~')
        for i in range(len(data)):
            link = data.url[i]
            category = data.category[i]
            subtitle = data.subtitle[i]
            yield scrapy.Request(url = link,callback = self.parse_body,meta = {'subtitle':subtitle,'category':category})
    def parse_body(self,response):
        item = BarronItem()
        item['url'] = response.url
        item['title'] = response.xpath("//meta[@name='article.headline']/@content").extract_first()
        item['subtitle'] = response.meta['subtitle']
        item['category'] = response.meta['category']
        datetimes = response.xpath('//*[@id="article-contents"]/header/div[2]/time/text()').extract_first()
        item['date'] = ' '.join(datetimes.strip().split(' ')[1:4]) if datetimes.strip().split(' ')[0] == 'Updated' else ' '.join(datetimes.strip().split(' ')[:3])
        tag = response.xpath("//meta[@name='keywords']/@content").extract_first()
        item['tags'] = tag
        bodys = response.xpath('//*[@class="snippet__body"]//p//text()').extract()
        b = ''.join(bodys)
        re_h =re.compile(r'\s+')
        item['body'] = re_h.sub(' ',b).replace('\ufeff',' ')
        tags = tag if tag else 'nan'
        tagss = tags.split(',')[0].islower()
        item['company'] = 'nan' if tagss else tag.split(',')[0]
        yield item
