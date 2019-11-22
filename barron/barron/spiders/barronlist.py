# -*- coding: utf-8 -*-
import scrapy
import json
from ..items import BarronItem
import re

class BarronlistSpider(scrapy.Spider):
    name = 'barronlist'
    custom_settings = {
        'ITEM_PIPELINES': {
            'barron.pipelines.BarronPipeline': 400
                },
        'HTTPCACHE_ENABLED': False
            }
    allowed_domains = ['www.barrons.com']
    urls = ['https://www.barrons.com/topics/technology/{}?id=%7B%22db%22%3A%22barrons%2Cbarronsblog%22%2C%22query%22%3A%22technology%22%2C%22queryType%22%3A%22type%22%2C%22page%22%3A%22{}%22%2C%22count%22%3A15%2C%22subjectValue%22%3A%22BARINDTECH%22%7D&type=topics_search'.format(i,i) for i in range(2,50)]
    links = ['https://www.barrons.com/topics/markets/{}?id=%7B%22db%22%3A%22barrons%2Cbarronsblog%22%2C%22query%22%3A%22markets%22%2C%22queryType%22%3A%22type%22%2C%22page%22%3A%22{}%22%2C%22count%22%3A15%2C%22subjectValue%22%3A%22BARMKTS%22%7D&type=topics_search'.format(i,i) for i in range(2,50)]
    start_urls = ['https://www.barrons.com/topics/technology?id=%7B%22db%22%3A%22barrons%2Cbarronsblog%22%2C%22query%22%3A%22technology%22%2C%22queryType%22%3A%22type%22%2C%22page%22%3A1%2C%22count%22%3A15%2C%22subjectValue%22%3A%22BARINDTECH%22%7D&type=topics_search','https://www.barrons.com/topics/markets/?id=%7B%22db%22%3A%22barrons%2Cbarronsblog%22%2C%22query%22%3A%22markets%22%2C%22queryType%22%3A%22type%22%2C%22page%22%3A1%2C%22count%22%3A15%2C%22subjectValue%22%3A%22BARMKTS%22%7D&type=topics_search'] + links + urls
    def parse(self, response):
        jsonresponse = json.loads(response.body_as_unicode())
        collection = jsonresponse['collection']
        art_ids = [x['id'] for x in collection]
        link = response.url
        links = link.split('/',4)[4]
        link_name = links.split('?')[0].split('/')[0] if '/' in links.split('?')[0] else links.split('?')[0]
        for art_id in art_ids:
            url = ('https://www.barrons.com/topics/{}?id={}&type=article'
                .format(link_name,art_id))
            yield scrapy.Request(url=url, callback=self.parse_url,meta = {'link_name':link_name})
    def parse_url(self, response):
        jsonresponse = json.loads(response.body_as_unicode())
        url = jsonresponse['data']['url']
        subtitle = jsonresponse['data']['summary']
        link_name = response.meta['link_name']
        yield scrapy.Request(url = url,callback = self.parse_body,meta = {'subtitle':subtitle,'link_name':link_name})
    def parse_body(self,response):
        item = BarronItem()
        item['url'] = response.url
        item['title'] = response.xpath("//meta[@name='article.headline']/@content").extract_first()
        item['subtitle'] = response.meta['subtitle']
        item['category'] = response.meta['link_name']
        datetimes = response.css('time.timestamp::text').extract_first()
        item['date'] = ' '.join(datetimes.strip().split(' ')[1:4]) if datetimes.strip().split(' ')[0] == 'Updated' else ' '.join(datetimes.strip().split(' ')[:3])
        yield item
