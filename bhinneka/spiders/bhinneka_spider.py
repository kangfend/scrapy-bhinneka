from scrapy.spider import Spider
from scrapy import Selector
from scrapy.http import Request

from bhinneka.items import BhinnekaItem
from bhinneka.utils import get_absolute_url


class BhinnekaSpider(Spider):
    name = "bhinneka"
    allowed_domains = ["www.bhinneka.com"]
    start_urls = ["http://www.bhinneka.com/categories.aspx"]
    items = set([])

    def parse(self, response):
        selector = Selector(response)
        categories = selector.xpath(
            '//*[@id="categories"]//li[@class="item"]/a[2]/@href'
        )
        for category in categories:
            url = get_absolute_url(category.extract())
            yield Request(url, callback=self.parse_category)

    def parse_category(self, response):
        selector = Selector(response)
        items = selector.xpath('//*[@class="box"]/table/tr')
        for item in items:
            product_item = BhinnekaItem()
            product_item['link'] = get_absolute_url(item.xpath('td[1]/a/@href').extract()[0])
            product_item['name'] = item.xpath('td[1]/a/text()').extract()[0]
            product_item['category'] = item.xpath('td[2]/text()').extract()[0]
            product_item['price'] = item.xpath('td[3]/text()').extract()[0]
            self.items.add(product_item)
        return self.items
