# -*- coding: utf-8 -*-
import scrapy
from scrapy import FormRequest
from scrapy.utils.response import open_in_browser


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    # allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/login']

    def parse(self, response):
        token = response.xpath('//*[@name="csrf_token"]/@value').extract_first()
        return FormRequest.from_response(response,
                                         formdata={'csrf_token': token, 'password': 'foo', 'username': 'foo'},
                                         callable=self.scrapy_home_page)

    def scrapy_home_page(self, response):
        open_in_browser(response)
        # h1_tag = response.xpath('//h1/a/text()').extract_first()
        # tags = response.xpath('//*[@class="tag-item"]/a/text()').extract()
        # yield {'H1 Tag': h1_tag, 'Tags': tags}

        quotes = response.xpath('//*[@class="quote"]')
        for quote in quotes:
            text = quote.xpath('.//*[@class="text"]/text()').extract_first()
            author = quote.xpath('.//*[@itemprop="author"]/text()').extract_first()
            tags = quote.xpath('.//*[@itemprop="keywords"]/@content').extract_first()

            yield {
                'Quote': text,
                'Author': author,
                'Tag': tags
            }

        next_page_url = response.xpath("//*[@class='next']/a/@href").extract_first()
        absolute_next_page_url = response.urljoin(next_page_url)
        yield scrapy.Request(absolute_next_page_url)
        # yield scrapy.Request(absoulute_next_page_url, callback=self.parse)
        # command:: scrapy crawl quotes -o items.xml

