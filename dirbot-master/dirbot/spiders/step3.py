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
import copy
import json

error_payloads = ["+and+SLAP(10)+--+",
					"'kasdgh",
					"+AND+SEELCT"]
links = open('linksToAttack.txt','r')
urls = links.readlines()
links.close()
items = []
fin = []
dic = {}

class step3(Spider):
	name = "step3"
	with open('input.json') as data_file:
		data = json.load(data_file)
	start_urls = [data['appurl']]
	login_user = [data['username']]
	login_pass = [data['password']]
	params = []
	
	def parse(self, response):
		print response
		args, url, method = fill_login_form(self.start_urls[0], response.body, self.login_user[0], self.login_pass[0])
		print args
		
		for x in query_string.split('&'):
			y = x.split('=')
			self.params.append((y[0], y[1]))
		
		return FormRequest(url, method=method, formdata=args, callback=self.after_login)

	def __init__(self):
		dispatcher.connect(self.spider_closed, signals.spider_closed)

	def after_login(self, response):
 		if (((("ERROR: Invalid username") or ("The username/password combination you have entered is invalid"))	in response.body) or (response.url is self.start_urls[0])):
			self.log("Login failed", level=log.ERROR)
			yield
		# continue scraping with authenticated session...
		else:
			self.log("Login succeed!", level=log.DEBUG)
			print response.url
			'''f = open("app4login.html", "w")
			f.write(response.body)
			f.close()'''
			print "response end!!\n"
			for temp in urls:
					if self.start_urls[0] in temp:
							yield Request(url=temp, meta={'temp':temp} , callback=self.save_original_resp)
			#file2 = open("vulnerableinks.txt","w")
			#for item in items:
					#file2.write(item+"\n")
			#write(temp+"\n")
			#file2.close()
			#temp = login_url + attack_url + "?" + query_string
			#yield Request(url=temp, callback=self.save_original_resp)
		return 
	'''
	def after_login(self, response):
		print "i am here" 
		temp = login_url + attack_url
		#print temp + ": " + str(self.params)
		return FormRequest(temp, formdata=self.params, callback=self.save_original_resp)
	'''
	def save_original_resp(self, response):
		temp = response.request.meta['temp']
		newfile = open('linksWithFalsePayloads.txt','a')
		#print "Response: " + response.url
		file = open("original_response.html", "w")
		file.write(response.body)
		file.close()
		for error in error_payloads:
				attack_with_payload = temp+error
				newfile.write(attack_with_payload+"\n")
				yield Request(attack_with_payload, meta={'temp':temp}, callback=self.save_attack_resp)
				if "&" in temp:
						queryVals = temp.split('&')
						length = len(queryVals)
						for i in range(0,length-1):
								dupVals = copy.copy(queryVals);
								dupVals[i] = dupVals[i]+error
								finLink = "";
								for i in range(0,length-1):
										if i == 0:
												finLink += dupVals[i]
										else:
												finLink += "&"+dupVals[i]
								newfile.write(finLink+"\n")
								yield Request(finLink, meta={'temp':temp}, callback=self.save_attack_resp)
				print "Did you see this"
		newfile.close()
		return 

	def save_attack_resp(self, response):
		file = open("attack_response.html", "w")
		file.write(response.body)
		file.close()
		temp = response.request.meta['temp']

		searchterms = ["mysql error","sql syntax", "mysql server version", "unknown column", "fatal error", "stack trace"]
		#if searchterms in response.body:
		if any(term in response.body.lower() for term in searchterms):
			self.log("\tVulnerable link: " + response.url, level=log.INFO)
			if (temp not in items):
					items.append(temp)
					file2 = open("vulnerableinks.txt","a")
					file2.write(temp+"\n")
					file2.close()
					dic1 ={}
					dic1["method"] = "" #Pending
					dic1["LoginRequired"] = "" #Pending
					dic1["username"] = self.login_user[0]
					dic1["password"] = self.login_pass[0]
					#OtherParameterToWrite #Pending
					dic[response.url] = [dic1]
		return None

	def spider_closed(self, spider):
		fin.append(dic)
		f = open("step3outputWithFakeAttacks.json", 'w')
		f.write(json.dumps(fin,indent= 4, sort_keys = True))
		f.close()