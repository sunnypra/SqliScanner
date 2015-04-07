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
    name = "dmoz"
    allowed_domains = ["app1.com"]
    """
    start_urls = [
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/",
                    ]
    """
    start_urls=["https://app1.com/users/login.php"]
    login_user = "admin"
    login_pass = "admin"
    #items = []
    dic={}
    #rules = (Rule(SgmlLinkExtractor(allow=('')), callback='parse_items',follow= True),)

    def parse(self, response):
        args, url, method = fill_login_form(self.start_urls[0], response.body, self.login_user, self.login_pass)
        return FormRequest(url, method=method, formdata=args, callback=self.after_login)
        #return [FormRequest(self.start_urls[0],formdata={'username': 'admin','password': 'admin'},callback=self.after_login)]
        #return FormRequest.from_response(response,formdata={'username': 'admin','password': 'admin'},callback=self.after_login)
    def after_login(self, response):
        # check login succeed before going on
        if "ERROR: Invalid username" in response.body:
            print "sunny"
            self.log("Login failed", level=log.ERROR)
            return

        # continue scraping with authenticated session...
        else:
            self.log("Login succeed!", level=log.DEBUG)
            print "prakash"
            print response.body
            return Request(url="https://app1.com/",
                           callback=self.parse1)


    def parse1(self, response):

        print response
        sel = Selector(response)
        sites = sel.xpath('//ul/li')

        items = []
        urls=[]
        for site in sites:
            item = Website()
            item['name'] = site.xpath('a/text()').extract()
            item['url'] = site.xpath('a/@href').extract()
            item['description'] = site.xpath('text()').re('-\s[^\n]*\\r')
            new_url = str(self.start_urls[0])+str(item['url'][0])
            yield Request(new_url, meta={'item':item,'url':new_url},callback=self.parse_items)
            #print item['name'] ,item['url'] ,item['description']
            items.append(item)
        self.dic[str(self.start_urls[0])]=items;
        print self.dic
        print "result"


    def parse_items(self, response):
        """
        The lines below is a spider contract. For more info see:
        http://doc.scrapy.org/en/latest/topics/contracts.html

        @url http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/
        @scrapes name
        """
        #print response
        sel = Selector(response)
        sites = sel.xpath('//ul/li')

        """print "sunny"
        print sites
        print "prakash"

        """


        if response.status in [404,500,303]:
            raise CloseSpider("Met the page which doesn't exist")

        url= response.request.meta['url']
        print "ss"
        print url
        #urls=[]
        items = []
        for site in sites:
            item = Website()
            item['name'] = site.xpath('a/text()').extract()
            item['url'] = site.xpath('a/@href').extract()
            item['description'] = site.xpath('text()').re('-\s[^\n]*\\r')
            new_url = str(self.start_urls[0])+str(item['url'][0]);
            #print new_url;
            #urls.append(new_url);
            yield Request(new_url, meta={'item':item},callback=self.parse_items)
            #print item['name'] ,item['url'] ,item['description']
            items.append(item)
        self.dic[url]=items;
        print "final"
        print self.dic
