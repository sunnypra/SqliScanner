from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from dirbot.items import Website
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.exporter import JsonItemExporter
import scrapy
from scrapy.http.request import Request
from scrapy.http import FormRequest
from scrapy import log
from loginform import fill_login_form


class DmozSpider(Spider):
    name = "sqli"
    allowed_domains = [
        "app1.com",
        "app4.com",
        "app5.com",
                    ]
    sta =["https://app1.com"]
    start_urls = [
        "https://app1.com/users/login.php",
        "https://app1.com",
        "http://app4.com",
        "http://app5.com",
                    ]
    login_user = [
        "scanner2",
        "scanner1",
        "admin",
        "student",
        "professor",
        "student2",
        "admin@admin.com",
        "dev@dev.com",
        "manager@manager.com",
        "user@user.com",
                    ]

    login_pass = [
        "scanner2",
        "scanner1",
        "admin",
        "student",
        "professor",
        "student2",
        "admin",
        "developer",
        "manager",
        "user",
                    ]
    dic={}


    def parse(self, response):
        self.parse1(self.start_urls[1])
        args, url, method = fill_login_form(self.start_urls[0], response.body, self.login_user[1], self.login_pass[1])
        return FormRequest(url, method=method, formdata=args, callback=self.after_login)
  



    def after_login(self, response):
        # check login succeed before going on
        if (((("ERROR: Invalid username") or 
            ("The username/password combination you have entered is invalid"))
            in response.body) or 
            (response.url is self.start_urls[0])):
            print "sunny"
            self.log("Login failed", level=log.ERROR)
            return
        # continue scraping with authenticated session...
        else:
            self.log("Login succeed!", level=log.DEBUG)
            print "prakash"
            print response.url
            print "response end!!\n"
            return Request(url=self.start_urls[1],
                           callback=self.parse1)


    def parse1(self, response):
        print "sun"
        print response.url
        sel = Selector(response)
        sites = sel.xpath('//ul/li')

        items = []
        urls=[]
        for site in sites:
            item = Website()
            item['name'] = site.xpath('a/text()').extract()
            item['url'] = site.xpath('a/@href').extract()
            item['description'] = site.xpath('text()').re('-\s[^\n]*\\r')
            yield self.collect_item(item)
            if(len(item['url']) != 0):
               if(len(str(item['url'][0])) != 1):
                 print "shailza1\n\n\n"
                 print item['url'][0]
                 print "shailza2\n\n\n"
                 new_url = str(self.start_urls[1])+str(item['url'][0])
                 print "shailza3\n\n\n"
                 print new_url
                 print "shailza4\n\n\n"
                 yield Request(new_url, meta={'item':item,'url':new_url},callback=self.parse_items)
                #print item['name'] ,item['url'] ,item['description']
            items.append(item)
        self.dic[str(self.start_urls[0])]=items;
     #   print self.dic
     #   print "result"


    def parse_items(self, response):
        #print response
        sel = Selector(response)
        sites = sel.xpath('//ul/li')


        if response.status in [404,500,303]:
            raise CloseSpider("Met the page which doesn't exist")

        url= response.request.meta['url']
        print "ss"
        print url
        items = []
        for site in sites:
            item = Website()
            item['name'] = site.xpath('a/text()').extract()
            item['url'] = site.xpath('a/@href').extract()
            item['description'] = site.xpath('text()').re('-\s[^\n]*\\r')
            if(len(item['url']) != 0): 
              if(len(str(item['url'][0])) != 1):
                print "shailza5\n\n\n"
                new_url = str(self.sta[0])+str(item['url'][0]);
                print item['url'][0] + "ssss"
                print len(str(item['url'][0]))
                print new_url
                print "shailza6\n\n\n"
                yield Request(new_url, meta={'item':item},callback=self.parse_items)
                self.dic[url]=items;

            items.append(item)
            yield self.collect_item(item)
        print "final"
        print self.dic



    def collect_item(self, item):
        return item
