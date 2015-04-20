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
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy.utils.url import urljoin_rfc
from scrapy.utils.response import get_base_url
import json

class DmozSpider(Spider):
    name = "step1"
    allowed_domains = []
    sta =[]
    start_urls = []
    login_user ="" 
    login_pass ="" 

    dic={}
    fin = []
    urllis =[]
    #obj = open('data.json', 'wb')
    #obj.write("{")
    def parse(self,response):
        print "Status:",response.status
        #args, url, method = fill_login_form(response.url, response.body, self.login_user, self.login_pass)
        #print "args",args
        #self.firstloginscrape()
        #yield FormRequest(start_urls[0], method=method, formdata=args,dont_filter=True,callback=self.firstpagescrape)
        #yield FormRequest(self.start_urls[0], meta={'url':self.start_urls[0]},callback=self.firstpagescrape)
        yield FormRequest( self.start_urls[0],callback=self.parse1)

        """
        if name:
                yield FormRequest.from_response(response, method=method, formdata=args, formname=name, callback=self.after_login)
        else:
                yield FormRequest.from_response(response, method=method, formdata=args, formnumber=number, callback=self.after_login)
        """

    def __init__(self):
        main_file = open("Singleinput.json",'r')
        infoList1 = json.load(main_file)
        infoList = infoList1[0]
        for key,value in infoList.iteritems():
            self.start_urls =  [str(key)]
            self.sta = self.start_urls
            self.login_url = [value[0].get("loginurl")]
            #self.login_user = value[0].get("params")[0].get("username")
            #self.login_pass = value[0].get("params")[0].get("password")
            urlDomain = self.login_url[0][self.login_url[0].find("//"):]
            urlDomain = urlDomain[2:]
            if (urlDomain.find("/") != -1):
                self.allowed_domains = [urlDomain[0:urlDomain.find("/")]]
            else:
                self.allowed_domains = [urlDomain]
      
        dispatcher.connect(self.spider_closed, signals.spider_closed)

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
            print "response end!!\n"
            return Request(url=response.url,
                           callback=self.parse1)

    def firstpagescrape(self,response):
        sel = Selector(response)
        #Wsites = sel.xpath('//ul/li')
        forms = sel.xpath("//ul/li/@onclick").extract()
        print "forms",forms
        sites = sel.xpath('//a/@href').extract()
        actions=sel.xpath("//form/@action").extract()
        texts=sel.xpath("//input[@type='text']/@name").extract()
        pwds= sel.xpath("//input[@type='password']/@name").extract()
        bts = sel.xpath("//input[@type='submit']/@name").extract()
        filist =texts+pwds+bts
        print sites
        print actions
        print texts
        print pwds
        print filist
        print "ssssssss"
        #print sites1
        items = []
        urls=[]
        for site in sites:
            new_url1 =""
            print "dsds",str(site)
            if(len(str(site)) != 1):
                if((str(site).startswith("http")) or (str(site).startswith("https"))):
                    new_url = str(site)
                else:
                    if((str(site).startswith("/www")) or (str(site).startswith("www"))):
                        new_url = urljoin_rfc(get_base_url(response),str(site))#str(baseUrl)+str(site)
                    else:
                        new_url = urljoin_rfc(get_base_url(response),str(site))#str(baseUrl)+str(site)
            else :
                continue
            if new_url in self.urllis:
                continue
            self.urllis.append(new_url)
            """
            if(new_url1!=""):
               self.urllis.append(new_url1)
            """
            if("logout" in str(new_url) or "calendar" in str(new_url)):
                return
            dic={}

            dic["url"] =str(new_url)
            dic["method"] =""
            dic["param"] = []
            self.fin.append(dic)
            #self.obj.write(str(self.allowed_domains[0])+":"+str(dic)+",")

            #yield Request(new_url, meta={'url':new_url},callback=self.parse1)
            #if (str(new_url1)!= "") :
            #    yield Request(str(new_url1), meta={'url':new_url},callback=self.parse_items)
        for act in actions:
            new_url1 = ""
            print "sssssddddd",str(act)
            if(len(str(act)) != 1):
                if((str(act).startswith("http")) or (str(act).startswith("https"))):
                    new_url = str(act)
                else:
                    if((str(act).startswith("/www")) or (str(act).startswith("www"))):
                        new_url = urljoin_rfc(get_base_url(response),str(act))#str(baseUrl)+str(act)
                    else:
                        new_url = urljoin_rfc(get_base_url(response),str(act))#str(baseUrl)+str(act)
            else :
                continue
            if new_url in self.urllis:
                continue
            if("logout" in str(new_url) or "calendar" in str(new_url)):
                return
            self.urllis.append(new_url)
            """
            if(new_url1!=""):
                self.urllis.append(new_url1)
            """

            dic = {}
            dic["url"] = str(new_url)
            dic["method"] ="POST"
            dic["param"] = filist
            self.fin.append(dic)

            #self.obj.write(str(self.allowed_domains[0])+":"+str(act)+",")
            #yield Request(new_url, meta={'url':new_url},callback=self.parse1)
            #if (str(new_url1)!= "") :
            #    yield Request(str(new_url1), meta={'url':new_url},callback=self.parse_items)
        for f in forms :
            new_url1 =""
            print "qwqw",str(f)
            pos = str(f).find('\'')
            locVal = str(f)[pos+1:len(str(f))-1]
            actstr = str(locVal)
            print "bvbvbv",actstr
            if(len(str(actstr)) != 1):
                if((str(actstr).startswith("http")) or (str(actstr).startswith("https"))):
                    new_url = str(actstr)
                else:
                    if((str(actstr).startswith("/www")) or (str(actstr).startswith("www"))):
                        new_url = urljoin_rfc(get_base_url(response),str(actstr))#str(baseUrl)+str(actstr)
                    else:
                        new_url = urljoin_rfc(get_base_url(response),str(actstr))#str(baseUrl)+str(actstr)
            else :
                continue
            if new_url in self.urllis:
                continue
            if("logout" in str(new_url) or "calendar" in str(new_url)):
                return

            self.urllis.append(new_url)
            """
            if(new_url1!=""):
                self.urllis.append(new_url1)
            """
            dic = {}
            dic["url"] = new_url
            dic["method"] =""
            dic["param"] = []
            self.fin.append(dic)

            #self.obj.write(str(self.allowed_domains[0])+":"+str(act)+",")
            #yield Request(new_url, meta={'url':new_url},callback=self.parse1)

    def parse1(self, response):

        print "response" ,response.url
        posbaseUrl = str(response.url).rfind("/")
        print "posbaseUrl",posbaseUrl
        baseUrl = str(response.url)[0:posbaseUrl+1]
        print "baseUrl",baseUrl
        """
        if(str(response.url) in self.urllis or "logout" in str(response.url)):
            return
        """
        sel = Selector(response)
        #Wsites = sel.xpath('//ul/li')
        forms = sel.xpath("//ul/li/@onclick").extract()
        print "forms",forms
        sites = sel.xpath('//a/@href').extract()
        actions=sel.xpath("//form/@action").extract()
        texts=sel.xpath("//input[@type='text']/@name").extract()
        pwds= sel.xpath("//input[@type='password']/@name").extract()
        bts = sel.xpath("//input[@type='submit']/@name").extract()
        filist =texts+pwds+bts
        print sites
        print actions
        print texts
        print pwds
        print filist
        print "ssssssss"
        #print sites1
        items = []
        urls=[]
        for site in sites:
            new_url1 =""
            print "dsds",str(site)
            if(len(str(site)) != 1):
                if((str(site).startswith("http")) or (str(site).startswith("https"))):
                    new_url = str(site)
                else:
                    if((str(site).startswith("/www")) or (str(site).startswith("www"))):
                        new_url = urljoin_rfc(get_base_url(response),str(site))#str(baseUrl)+str(site)
                    else:
                        new_url = urljoin_rfc(get_base_url(response),str(site))#str(baseUrl)+str(site)
            else :
                continue
            if new_url in self.urllis:
                continue
            self.urllis.append(new_url)
            """
            if(new_url1!=""):
               self.urllis.append(new_url1)
            """
            if("logout" in str(new_url) or "calendar" in str(new_url)):
                return
            dic={}

            dic["url"] =str(new_url)
            dic["method"] =""
            dic["param"] = []
            self.fin.append(dic)
            #self.obj.write(str(self.allowed_domains[0])+":"+str(dic)+",")

            yield Request(new_url, meta={'url':new_url},callback=self.parse1)
            #if (str(new_url1)!= "") :
            #    yield Request(str(new_url1), meta={'url':new_url},callback=self.parse_items)
        for act in actions:
            new_url1 = ""
            print "sssssddddd",str(act)
            if(len(str(act)) != 1):
                if((str(act).startswith("http")) or (str(act).startswith("https"))):
                    new_url = str(act)
                else:
                    if((str(act).startswith("/www")) or (str(act).startswith("www"))):
                        new_url = urljoin_rfc(get_base_url(response),str(act))#str(baseUrl)+str(act)
                    else:
                        new_url = urljoin_rfc(get_base_url(response),str(act))#str(baseUrl)+str(act)
            else :
                continue
            if new_url in self.urllis:
                continue
            self.urllis.append(new_url)
            if("logout" in str(new_url) or "calendar" in str(new_url)):
                return
            """
            if(new_url1!=""):
                self.urllis.append(new_url1)
            """
            dic = {}
            dic["url"] = str(new_url)
            dic["method"] =""
            dic["param"] = filist
            self.fin.append(dic)

            #self.obj.write(str(self.allowed_domains[0])+":"+str(act)+",")
            yield Request(new_url, meta={'url':new_url},callback=self.parse1)
            #if (str(new_url1)!= "") :
            #    yield Request(str(new_url1), meta={'url':new_url},callback=self.parse_items)
        for f in forms :
            new_url1 =""
            print "qwqw",str(f)
            pos = str(f).find('\'')
            locVal = str(f)[pos+1:len(str(f))-1]
            actstr = str(locVal)
            print "bvbvbv",actstr
            if(len(str(actstr)) != 1):
                if((str(actstr).startswith("http")) or (str(actstr).startswith("https"))):
                    new_url = str(actstr)
                else:
                    if((str(actstr).startswith("/www")) or (str(actstr).startswith("www"))):
                        new_url = urljoin_rfc(get_base_url(response),str(actstr))#str(baseUrl)+str(actstr)
                    else:
                        new_url = urljoin_rfc(get_base_url(response),str(actstr))#str(baseUrl)+str(actstr)
            else :
                continue
            if new_url in self.urllis:
                continue
            self.urllis.append(new_url)
            if("logout" in str(new_url) or "calendar" in str(new_url)):
                return
            """
            if(new_url1!=""):
                self.urllis.append(new_url1)
            """
            dic = {}
            dic["url"] = new_url
            dic["method"] =""
            dic["param"] = []
            self.fin.append(dic)

            #self.obj.write(str(self.allowed_domains[0])+":"+str(act)+",")
            yield Request(new_url, meta={'url':new_url},callback=self.parse1)
            #if (str(new_url1)!= "") :
            #   yield Request(str(new_url1), meta={'url':new_url},callback=self.parse_items)
        print self.fin

    def parse_items(self, response):
        print "response@@@" ,response.url
        """
        if(str(response.url) in self.urllis or "logout" in str(response.url)) :
            return
        """
        posbaseUrl = str(response.url).rfind("/")
        print "posbaseUrl",posbaseUrl
        baseUrl = str(response.url)[0:posbaseUrl+1]
        print "baseUrl",baseUrl
        sel = Selector(response)
        #Wsites = sel.xpath('//ul/li')
        forms = sel.xpath("//ul/li/@onclick").extract()
        print "forms",forms
        sites = sel.xpath('//a/@href').extract()
        actions=sel.xpath("//form/@action").extract()
        texts=sel.xpath("//input[@type='text']/@name").extract()
        pwds= sel.xpath("//input[@type='password']/@name").extract()
        bts = sel.xpath("//input[@type='submit']/@name").extract()
        filist =texts+pwds+bts
        print sites
        print actions
        print texts
        print pwds
        print filist
        print "mmmmmmm"
        #print sites
        #print actions
        #print texts
        #print "ssssssss"
        #print sites1
        items = []
        urls=[]
        for site in sites:
            new_url1 =""
            print "dsds",str(site)
            if((str(site).startswith("/"))):
                site = str(site)[1:]
            if(len(str(site)) != 1):
                if((str(site).startswith("http")) or (str(site).startswith("https"))):
                    new_url = str(site)
                else:
                    if((str(site).startswith("/www")) or (str(site).startswith("www"))):
                        new_url = str(baseUrl)+str(site)
                    else:
                        new_url = str(baseUrl)+str(site)
            else :
                continue
            if new_url in self.urllis:
                continue
            self.urllis.append(new_url)
            #if(new_url1!=""):
            #   self.urllis.append(new_url1)
            dic={}

            dic["url"] =str(new_url)
            dic["method"] =""
            dic["param"] = []
            self.fin.append(dic)
            #self.obj.write(str(self.allowed_domains[0])+":"+str(dic)+",")
            if("logout" in str(new_url)):
                return
            yield Request(new_url, meta={'url':new_url},callback=self.parse_items)

        for act in actions:
            new_url1 = ""
            print "sssssddddd",str(act)
            if((str(act).startswith("/"))):
                act = str(act)[1:]
            if(len(str(act)) != 1):
                if((str(act).startswith("http")) or (str(act).startswith("https"))):
                    new_url = str(act)
                else:
                    if((str(act).startswith("/www")) or (str(act).startswith("www"))):
                        new_url = str(baseUrl)+str(act)
                    else:
                        new_url = str(baseUrl)+str(act)
            else :
                continue
            if new_url in self.urllis:
                continue
            self.urllis.append(new_url)
            #if(new_url1!=""):
            #    self.urllis.append(new_url1)
            dic = {}
            dic["url"] = str(new_url)
            dic["method"] =""
            dic["param"] = filist
            self.fin.append(dic)
            if("logout" in str(new_url)):
                return
            #self.obj.write(str(self.allowed_domains[0])+":"+str(act)+",")
            yield Request(new_url, meta={'url':new_url},callback=self.parse_items)

        for f in forms :
            new_url1 =""
            print "qwqw",str(f)
            if((str(f).startswith("/"))):
                f = str(f)[1:]
            pos = str(f).find('\'')
            locVal = str(f)[pos+1:len(str(f))-1]
            actstr = str(locVal)
            print "bvbvbv",actstr
            if(len(str(actstr)) != 1):
                if((str(actstr).startswith("http")) or (str(actstr).startswith("https"))):
                    new_url = str(actstr)
                else:
                    if((str(actstr).startswith("/www")) or (str(actstr).startswith("www"))):
                        new_url = str(baseUrl)+str(actstr)
                    else:
                        new_url = str(baseUrl)+str(actstr)
            else :
                continue
            if new_url in self.urllis:
                continue
            self.urllis.append(new_url)
            #if(new_url1!=""):
            #    self.urllis.append(new_url1)
            self.urllis.append(new_url)
            dic = {}
            dic["url"] = new_url
            dic["method"] =""
            dic["param"] = []
            self.fin.append(dic)
            if("logout" in str(new_url)):
                return
            #self.obj.write(str(self.allowed_domains[0])+":"+str(act)+",")
            yield Request(new_url, meta={'url':new_url},callback=self.parse_items)
        #print self.fin
     #   print self.dic
     #   print "result"


    def spider_closed(self, spider):
       # for s in self.json_objects:
        #  print s
#       all_json_objects = {}
 #      all_json_objects["injections"] =  self.json_objects
       f = open("data.json", 'wb')
 #      jsonString = json.dumps(jsonObj)
       f.write(json.dumps(self.fin,indent= 4, sort_keys = True))
       f.close()
       #self.callback_function =  """payload_generation("Stage2.json")"""
    #   self.parse()
   #    self.parse1(url = self.start_urls[0])
       #self.payload_generation("Stage2.json")



    def collect_item(self, item):
        return item
