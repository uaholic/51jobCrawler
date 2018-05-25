from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re
from w3lib.html import remove_tags

from example.items import ExampleItem


def pages():
    urls = []
    for i in range(1,196):
        urls.append(f'https://search.51job.com/list/020000,000000,0000,00,9,99,大数据,2,{i}.html')
    return urls

class DmozSpider(CrawlSpider):
    """Follow categories and extract links."""
    name = '51job'
    allowed_domains = ['51job.com']
    start_urls = pages()
    rules = [
        Rule(LinkExtractor(
            allow=('https://jobs.51job.com/shanghai.*/.*.html?.*',)
        ), callback='parse_directory', follow=False),
    ]

    def parse_directory(self, response):
        url=response.url
        title=response.selector.xpath('//h1[@title]/text()').extract()
        title=title[0]
        loc=response.selector.xpath('//span[@class="lname"]/text()').extract()
        loc=loc[0]
        sar = response.selector.xpath('//div[@class="cn"]//strong/text()').extract()
        if sar:
            sar = sar[0]
        else:
            sar='面议'
        req = response.selector.xpath('//div[@class ="jtag inbox"]//div[@class ="t1"]//span[@class="sp4"]/text()').extract()
        exp = req[0]
        if req[1][0] == '招':
            xueli='不限'
            num=req[1]
        else:
            xueli = req[1]
            num = req[2]
        desc = response.selector.xpath('//div[@class ="bmsg job_msg inbox"]').extract()
        content = remove_tags(desc[0])
        desc=re.sub(r'[\t\r\n\s]', '', content)
        # print('标题:', title)
        # print('地点:', loc)
        # print('工资:', sar)
        # print('经验要求:', exp)
        # print('学历要求:', xueli)
        # print('招聘人数:', num)
        # print('任职要求:',desc)
        # print('url',url)

        po=ExampleItem()
        po['title']=title
        po['loc']=loc
        po['sar']=sar
        po['exp']=exp
        po['xueli']=xueli
        po['num']=num
        po['desc']=desc
        po['url']=url

        yield po
        # ms=response.body
        #
        # mm=mstr=str(ms,"gbk")
        # print(mm)
    # def parse_directory(self, response):
    #     for div in response.css('.title-and-desc'):
    #         yield {
    #             'name': div.css('.site-title::text').extract_first(),
    #             'description': div.css('.site-descr::text').extract_first().strip(),
    #             'link': div.css('a::attr(href)').extract_first(),
    #         }
