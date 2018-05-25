# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
from datetime import datetime

class ExamplePipeline(object):
    def __init__(self):
        self.count=1
        self.mfile=open("51jobs-shanghai.txt","w",encoding="utf-8")
    def process_item(self, item, spider):
        item["crawled"] = datetime.utcnow()
        item["spider"] = spider.name
        title = item["title"]
        loc = item["loc"]
        sar = item["sar"]
        exp = item["exp"]
        xueli = item["xueli"]
        num = item["num"]
        desc = item["desc"]
        url = item["url"]
        self.count+=1
        self.mfile.write(f'标题:{title}    地点:{loc}    工资:{sar}    经验要求:{exp}    学历要求:{xueli}    招聘人数:{num}    任职要求:{desc}    url:{url}\n')
        if self.count%20==0:
            self.mfile.flush()
        return item
    def close_spider(self,spider):
        self.mfile.close()
