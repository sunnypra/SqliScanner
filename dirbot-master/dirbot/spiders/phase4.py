#!/usr/bin/python
from selenium import webdriver
import selenium.webdriver.common.keys
import selenium.webdriver.common.alert
from selenium.webdriver.common.by import By
import json

# store all values for one url in a dictionary
def getKeyValue(params,keyValues):
	paramsDic = params[0]
	for key,value in paramsDic.iteritems():
		if type(value) is list:
			getKeyValue(value,keyValues)
		else:
			keyValues[key]=value


#find the login url from url1
def findLoginURL(urlDomain,totalList):
	urlDict = totalList[0]
	for key,value in urlDict.iteritems():
		if (urlDomain in key):
			if type(value) is list:
				tempList = value[0]
				loginURL = tempList.get("loginURL",key)
				return loginURL;

#login function
def login(driver,uname,passwd,loginURL,usernameID,passwdID):
		driver.get(loginURL)
		
		if (len(driver.find_elements_by_name(usernameID)) > 0):
			nameele = driver.find_element_by_name(usernameID)
		elif (len(driver.find_elements_by_id(usernameID)) > 0):
			nameele = driver.find_element_by_id(usernameID)
		nameele.send_keys(uname)

		if (len(driver.find_elements_by_name(passwdID)) > 0):
			passele = driver.find_element_by_name(passwdID)
		elif (len(driver.find_elements_by_id(passwdID)) > 0):
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
				if(url2 == loginURL):
					print "login attempt failed"
				else:
					driver.get(url2)
					print "login successful"
					return "true"
		return "false"


# attack if the method is post
def	postAttack(driver,url,fieldID,fieldValue,buttonID):
	driver.get(url)
	fieldIDele = driver.find_element_by_name(fieldID)
	fieldIDele.send_keys(fieldValue)
	buttonEle = driver.find_element_by_name(buttonID)
	buttonEle.click()



#MAIN PROCESSSING
temp_file = open("Step3output.json",'r')
data = json.load(temp_file)
data2 = data[0]
keyValues = {}

#Load main file to get login url
main_file = open("LoginData.json",'r')
urlList = json.load(main_file)

# try possible attacks in json file
for key,value in data2.iteritems():
	url1 = key
	print url1
	getKeyValue(value,keyValues)

	#get login url
	urlDomain = url1[url1.find("//"):]
	urlDomain = urlDomain[2:]
	urlDomain = urlDomain[:urlDomain.find("/")]
	loginURL = findLoginURL(urlDomain,urlList)

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
	  	driver = webdriver.Firefox()
	  	loginStatus = login(driver,uname,passwd,loginURL,usernameID,passwdID)
	  	if(loginStatus == "true"):
			#login successful, now use the attack url
			if(method == "POST"):
				fieldID = keyValues.get("fieldID")
				fieldVal = keyValues.get("fieldValue",None)
				buttonID = keyValues.get("buttonID",None)
				postAttack(driver,url1,fieldID,fieldValue,buttonID)
			else:
				driver.get(url1)
		else:
			#login failed. Exit!
			scr = "alert('login failed');"
			driver.execute_script(scr)
	#if loginRequired is false then two attack options:
	# 1) Login attack
	# 2) No login, only attack by the url
	else:
		if(uname or passwd):
			driver1 = webdriver.Firefox()
		  	loginStatus = login(driver1,uname,passwd,loginURL,usernameID,passwdID)
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




