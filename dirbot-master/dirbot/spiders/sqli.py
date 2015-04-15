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
import json


class DmozSpider(Spider):
    name = "sqli1"
    allowed_domains = [
        "app1.com",
        "app4.com",
        "app5.com",
                    ]
    sta =["https://app5.com/"]
    credentials = {
        "http://zencart.com/index.php?main_page=login":['student@student.com','student'], #zencart
        "http://192.168.56.102/phpScheduleIt/":['student@email.com','student'], #phpscheduleit
        "http://192.168.56.106/index.php/customer/account/login/":['student@student.com','student'], #magneto
        "http://192.168.56.101/profile.php?action=login": ['student@student.com','student'], #Astrospaces
        "http://192.168.56.102/CubeCart/index.php?_a=login" : ['student@student.com','student'], #Cubecart
        "http://192.168.56.103/dokeos/index.php":['student','student'], #Dokeos
        "http://192.168.56.104/efront/www/index.php?":['student','student'], #eFront
        "http://192.168.56.105/elgg/":['student','student'], #Elgg
        "http://192.168.56.107/owncloud/":['student','student'], #owncloud
        "http://192.168.56.108/index.php?route=account/login":['student@student.com','student'], #opencart
        "http://192.168.56.109/index.php/site/login":['student','student'], #x2crm
        "http://192.168.56.110/src/login.php":['student','student'], #squirrelmail
        "http://192.168.56.101/catalog/login.php":['student@student.com','student'], #osCommerce
        "http://192.168.56.103/piwigo-2.0.0/identification.php":['student','student'], #Piwigo
        "http://192.168.56.102/login.php":['student','student'], #Phorum
        "http://192.168.56.109/prestashop/authentication.php":['student@student.com','student'], #PrestaShop
        "http://192.168.56.106/cpg/login.php?referer=index.php":['student','student'] #Gallery
    }
    """
    start_urls = [
        "https://app1.com/users/login.php",
#         "https://app1.com",
#         "http://app4.com",
#         "http://app5.com",
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

    """
    start_urls = [
                  "https://app5.com/www/index.php"
        #"https://app1.com/users/login.php",
#         "https://app1.com",
#         "http://app4.com",
#         "http://app5.com",
                    ]
    dic={}
    def parse(self,response):
        #print "Status:",response.status
        #print "Request Headers"
        #print response.request.headers.items()
        #print "\n\n"
        #print "Response Headers"
        #print response.headers.items()
        #print "\n\n"

        login_user = "admin"#self.credentials[response.request.url][0]
        login_pass = "admin"#self.credentials[response.request.url][1]
        args, url, method = fill_login_form(response.url, response.body, login_user, login_pass)
        yield FormRequest(response.url, method=method, formdata=args,dont_filter=True,callback=self.after_login)
        """
        if name:
                yield FormRequest.from_response(response, method=method, formdata=args, formname=name, callback=self.after_login)
        else:
                yield FormRequest.from_response(response, method=method, formdata=args, formnumber=number, callback=self.after_login)
        """



    def after_login(self, response):
        # check login succeed before going on
        if (((("ERROR: Invalid username") or
            ("The username/password combination you haventered is invalid"))
            in response.body) or
            (response.url is self.start_urls[0])):
            self.log("Login failed", level=log.ERROR)
            return
        # continue scraping with authenticated session...
        else:
            self.log("Login succeed!", level=log.DEBUG)
            print response.url
            print "response end!!"+ response.url
            return Request(url=response.url,
                           callback=self.parse1)


    def parse1(self, response):
        print response
        sel = Selector(response)
        texts=sel.xpath("//input[@type='text']")
        print "ttttttt"
        print texts
        print "sssssss"
        sites = sel.xpath("//ul/li[@onclick]")
        print sites
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
                 new_url = str(self.sta[0])+str(item['url'][0])
                 print "new_url :"+new_url
                 yield Request(new_url, meta={'item':item,'url':new_url},callback=self.parse_items)
            items.append(item)
        self.dic[str(self.start_urls[0])]=items;
        #yield self.collect_item(self.dic)
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
                new_url = str(self.sta[0])+str(item['url'][0]);
                yield Request(new_url, meta={'item':item},callback=self.parse_items)
                self.dic[url]=items;
            items.append(item)
            yield self.collect_item(self.dic)



    def collect_item(self, dic):
        print "sunny_res"+self.dic
        self.file = open('phase1items.json', 'wb')
        json.dumps([{'name': k, 'size': v} for k,v in self.dic.items()], indent=4)
        #self.file.write(line)
        #return item
