from scrapy.spider import Spider
from scrapy import Selector
from scrapy.http import FormRequest
from bhinneka.items import BhinnekaItem


class BhinnekaSpider(Spider):
    name = "smartphone"
    allowed_domains = ["www.bhinneka.com"]
    start_urls = ["http://www.bhinneka.com/category/smart_phone.aspx"]
    items = set([])

    def parse(self, response):
        return FormRequest(
            self.start_urls[0],
            formdata=self.get_formdata(response),
            callback=self.parse_items,
            dont_filter=True
        )

    def get_formdata(self, response):
        selector = Selector(response)
        form = selector.xpath('//form[@id="aspnetForm"]')
        viewstate = form.xpath('//input[@name="__VIEWSTATE"]/@value').extract()[0]
        return {
            '__EVENTTARGET': 'ctl00$content$listViewItemsPager$pagerNext$lbNext',
            '__EVENTARGUMENT': '',
            '__LASTFOCUS': '',
            '__VIEWSTATE': viewstate
        }

    def parse_items(self, response):
        selector = Selector(response)
        products = selector.xpath('//li[@class="prod-itm"]')
        for product in products:
            item = BhinnekaItem()
            item['name'] = product.xpath("a/span/span/text()").extract()
            item['price'] = product.xpath('div/div/div/a//*[@class="prod-itm-price"]/text()').extract()
            self.items.add(item)

        next_link = selector.xpath('//*[@id="ctl00_content_listViewItemsPager_pagerNext_lbNext"]').extract()
        next_page = True if next_link else False
        if next_page:
            return FormRequest(
                self.start_urls[0],
                formdata=self.get_formdata(response),
                callback=self.parse_items,
                dont_filter=True
            )
        return self.items
