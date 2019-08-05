# -*- coding: utf-8 -*-
import scrapy
import json
from ..items import BarronItem
import re

class BarronlistSpider(scrapy.Spider):
    name = 'barronlist'
    # set ReuterPipeline
    custom_settings = {
        'ITEM_PIPELINES': {
            'barron.pipelines.BarronPipeline': 400
                },
        'HTTPCACHE_ENABLED': True
            }
    allowed_domains = ['www.barrons.com']
    # To crawl the URL of the data page
    links = ['https://www.barrons.com/topics/markets?id=%7B%22db%22%3A%22barrons%2Cbarronsblog%22%2C%22query%22%3A%22markets%22%2C%22queryType%22%3A%22type%22%2C%22page%22%3A1%2C%22count%22%3A15%2C%22subjectValue%22%3A%22BARMKTS%22%7D&type=topics_search','https://www.barrons.com/topics/technology?id=%7B%22db%22%3A%22barrons%2Cbarronsblog%22%2C%22query%22%3A%22technology%22%2C%22queryType%22%3A%22type%22%2C%22page%22%3A1%2C%22count%22%3A15%2C%22subjectValue%22%3A%22BARINDTECH%22%7D&type=topics_search']
    urls = ['https://www.barrons.com/topics/technology/{}?id=%7B%22db%22%3A%22barrons%2Cbarronsblog%22%2C%22query%22%3A%22technology%22%2C%22queryType%22%3A%22type%22%2C%22page%22%3A%22{}%22%2C%22count%22%3A15%2C%22subjectValue%22%3A%22BARINDTECH%22%7D&type=topics_search'.format(i,i) for i in range(2,4)]
    start_urls = ['https://www.barrons.com/topics/markets/{}?id=%7B%22db%22%3A%22barrons%2Cbarronsblog%22%2C%22query%22%3A%22markets%22%2C%22queryType%22%3A%22type%22%2C%22page%22%3A%22{}%22%2C%22count%22%3A15%2C%22subjectValue%22%3A%22BARMKTS%22%7D&type=topics_search'.format(i,i) for i in range(2,4)] + urls + links
    def parse(self, response):
        # Get the ID of the current URL
        jsonresponse = json.loads(response.body_as_unicode())
        collection = jsonresponse['collection']
        art_ids = [x['id'] for x in collection]
        link = response.url
        links = link.split('/',4)[4]
        link_name = links.split('?')[0].split('/')[0] if '/' in links.split('?')[0] else links.split('?')[0]
        # Splicing ID to generate a new URL
        for art_id in art_ids:
            url = ('https://www.barrons.com/topics/{}?id={}&type=article'
                .format(link_name,art_id))
            yield scrapy.Request(url=url, callback=self.parse_url,meta = {'link_name':link_name})
    def parse_url(self, response):
        # Get the url, title, date of each article through a new URL spliced from the previous layer
        jsonresponse = json.loads(response.body_as_unicode())
        url = jsonresponse['data']['url']
        subtitle = jsonresponse['data']['summary']
        link_name = response.meta['link_name']
        yield scrapy.Request(url = url,callback = self.parse_body,meta = {'subtitle':subtitle,'link_name':link_name})
    def parse_body(self,response):
        item = BarronItem()
        # Get url and store it in output.csv file through pipeline file
        item['url'] = response.url
        # Get title and store it in output.csv file through pipeline file
        item['title'] = response.xpath("//meta[@name='article.headline']/@content").extract_first()
        # Get subtitle and store it in output.csv file through pipeline file
        item['subtitle'] = response.meta['subtitle']
        # Get category and store it in output.csv file through pipeline file
        item['category'] = response.meta['link_name']
        datetimes = response.css('time.timestamp::text').extract_first()
        # Get date and store it in output.csv file through pipeline file
        item['date'] = ' '.join(datetimes.strip().split(' ')[1:4]) if datetimes.strip().split(' ')[0] == 'Updated' else ' '.join(datetimes.strip().split(' ')[:3])
        yield item
