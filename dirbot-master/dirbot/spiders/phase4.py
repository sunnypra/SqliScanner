#!/usr/bin/python
from selenium import webdriver
import selenium.webdriver.common.keys
import selenium.webdriver.common.alert
from selenium.webdriver.common.by import By
import json

temp_file = open("Step3output.json",'r')
data = json.load(temp_file)
data2 = data[0]
keyValues = {}

# store all values for one url in a dictionary
def getKeyValue(params,keyValues):
	paramsDic = params[0]
	for key,value in paramsDic.iteritems():
		if type(value) is list:
			getKeyValue(value,keyValues)
		else:
			keyValues[key]=value


#login function
def login(driver,username,passwd,url,usernameID,passwdID):
		driver.get(url)
		if (driver.find_element(By.name(usernameID)).size() > 0):
			nameele = driver.find_element_by_name(usernameID)
		elif (driver.findElements(By.id(usernameID)).size() > 0):
			nameele = driver.find_element_by_id(usernameID)
		nameele.send_keys(username)

		if (driver.findElements(By.name(passwdID)).size() > 0):
			passele = driver.find_element_by_name(passwdID)
		elif (driver.findElements(By.id(passwdID)).size() > 0):
			passele = driver.find_element_by_id(passwdID)
		passele.send_keys(passwd)

		inp_elems = driver.find_elements_by_tag_name('input')
		for i in inp_elems:
			if (((i.get_attribute('type') == 'button') or (i.get_attribute('type') == 'submit')) & 
				((i.get_attribute('value') == 'Login') or (i.get_attribute('value') == 'login'))):
				i.click()
				url2= driver.current_url
				#to verify is login is successful or not,
				#we wil verify if the username is available somewhere on the webpage
				if(url2 == url):
					print "login attempt failed"
				else:
					driver.get(url2)
					print "login successful"
					return "true"
		return "false"


# attack if the method is post
def	postAttack(driver,url,fieldID,fieldValue,buttonID):
	driver.get(url1)
	fieldIDele = driver.find_element_by_name(fieldID)
	fieldIDele.send_keys(fieldValue)
	buttonEle = driver.find_element_by_name(buttonID)
	buttonEle.click()


# try possible attacks in json file
for key,value in data2.iteritems():
	url1 = key
	print url1
	getKeyValue(value,keyValues)

	# check if attack is using a url only,no login required 
	loginCheck = keyValues.get("LoginRequired","false")
	uname = keyValues.get("username",None)
	passwd = keyValues.get("password",None)
	usernameID = keyValues.get("userID",None)
	passwdID = keyValues.get("passID",None)
	method = keyValues.get("method","GET")

	# loginRequired = true then login and load the url
	# two urls required -> one for login and other as the attack
	if (loginCheck == "true"):
	  	print "true loginCheck"
	  	driver = webdriver.Firefox()
	  	loginStatus = login(driver,uname,passwd,url1,usernameID,passwdID)
	  	if(loginStatus == "true"):
			#login successful, now use the attack url
			if(method == "POST"):
				fieldID = keyValues.get("fieldID")
				fieldVal = keyValues.get("fieldValue",None)
				buttonID = keyValues.get("buttonID",None)
				postAttack(driver,url,fieldID,fieldValue,buttonID)
			else:
				driver.get(attack_url)
		else:
			#login failed. Exit!
			scr = "alert('login failed');"
			driver.execute_script(scr)
	#if loginRequired is false then two attack options:
	# 1) Login attack
	# 2) No login, only attack by the url
	else:
		print "false loginCheck"
		if(uname or passwd):
			driver1 = webdriver.Firefox()
		  	loginStatus = login(driver1,uname,passwd,url1,usernameID,passwdID)
	  		if(loginStatus == "true"):
				#login attack successful, now use the attack url
				scr = "alert('attack successful');"
				driver1.execute_script(scr)
			else:
				#login failed. Exit!
				scr = "alert('attack failed');"
				driver1.execute_script(scr)
		else:
			driver2 = webdriver.Firefox()
			#if the attack is a only using url then it may be using a post request
			methodVal = keyValues.get("method","GET")
			if(methodVal == "POST"):
				fieldID = keyValues.get("fieldID")
				fieldVal = keyValues.get("fieldValue",None)
				buttonID = keyValues.get("buttonID",None)
				postAttack(driver,url,fieldID,fieldValue,buttonID)
			else:
				driver2.get(url1)




