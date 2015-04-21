#!/usr/bin/python
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
				loginURL = tempList.get("loginurl",key)
				return loginURL;

#login function
def login(tempPyFil,uname,passwd,loginURL,usernameID,passwdID):
	tempPyFil.write("driver.get(\""+str(loginURL)+"\")\n")
	tempPyFil.write("if (len(driver.find_elements_by_name(\"" + str(usernameID) + "\")) > 0):\n")
	tempPyFil.write("nameele = driver.find_element_by_name(\"" + str(usernameID) + "\")\n")
	tempPyFil.write("elif (len(driver.find_elements_by_id(\"" + str(usernameID) + "\") > 0):\n")
	tempPyFil.write("nameele = driver.find_element_by_id(\""+str(usernameID)+"\")\n")
	tempPyFil.write("nameele.send_keys(\""+ str(uname) + "\")\n")

	tempPyFil.write("if (len(driver.find_elements_by_name(\"" + str(passwdID) + "\")) > 0):\n")
	tempPyFil.write("passele = driver.find_element_by_name(\"" + str(passwdID) + "\")\n")
	tempPyFil.write("elif (len(driver.find_elements_by_id(\"" + str(passwdID) + "\") > 0):\n")
	tempPyFil.write("passele = driver.find_element_by_id(\""+str(passwdID)+"\")\n")
	tempPyFil.write("passele.send_keys(\""+ str(passwd) + "\")\n")

	tempPyFil.write("inp_elems = driver.find_elements_by_tag_name('input')\n")
	tempPyFil.write("for i in inp_elems:\n")
	tempPyFil.write("if (((i.get_attribute('type') == 'button') or (i.get_attribute('type') == 'submit')) &\n")
	tempPyFil.write("((i.get_attribute('value') == 'Login') or (i.get_attribute('value') == 'login'))):\n")
	tempPyFil.write("i.click()\n")
	tempPyFil.write("url2= driver.current_url\n")

	tempPyFil.write("if(url2 == loginURL):\n")
	tempPyFil.write("print \"login attempt failed\"\n")
	tempPyFil.write("else:\n")
	tempPyFil.write("driver.get(url2)\n")
	tempPyFil.write("print \"login successful\"\n")
	tempPyFil.write("break\n\n")


# attack if the method is post
def	postAttack(tempPyFil,url,fieldID,fieldValue,buttonID):
	tempPyFil.write("driver.get(\""+str(url)+"\")\n")

	tempPyFil.write("if (len(driver.find_elements_by_name(\"" + str(fieldID) + "\")) > 0):\n")
	tempPyFil.write("\tfieldIDele = driver.find_element_by_name(\"" + str(fieldID) + "\")\n")
	tempPyFil.write("elif (len(driver.find_elements_by_id(\"" + str(fieldID) + "\")) > 0):\n")
	tempPyFil.write("\tfieldIDele = driver.find_element_by_id(\"" + str(fieldID) + "\")\n")
	tempPyFil.write("fieldIDele.send_keys(\"" + str(fieldValue) + "\")\n\n")

	#if button id is not found then search using the input tag name
	tempPyFil.write("if (\""+ str(buttonID) + "\" is None):\n")
	tempPyFil.write("\tinp_elems = driver.find_elements_by_tag_name('input')\n")
	tempPyFil.write("\tfor i in inp_elems:\n")
	tempPyFil.write("\t\tif (((i.get_attribute('type') == 'button') or (i.get_attribute('type') == 'submit'))):\n")
	tempPyFil.write("\t\t\ti.click()\n")
	tempPyFil.write("\t\t\turl2= driver.current_url\n")
	
	tempPyFil.write("\t\t\tif(url2 == url):\n")
	tempPyFil.write("\t\t\t\tprint \"attack attempt failed\"\n")
	tempPyFil.write("\t\t\telse:\n")
	tempPyFil.write("\t\t\t\tdriver.get(url2)\n")
	tempPyFil.write("\t\t\t\tprint \"attack successful\"\n")
	tempPyFil.write("\t\telse:\n")
	tempPyFil.write("\t\t\tbuttonEle = driver.find_elements_by_tag_name(\""+str(buttonID)+"\")\n")
	tempPyFil.write("\t\t\tbuttonEle.click()\n")
	


def main():
	#MAIN PROCESSSING
	temp_file = open("step3output.json",'r')
	data = json.load(temp_file)
	data2 = data[0]
	keyValues = {}

	#Load main file to get login url
	main_file = open("Singleinput.json",'r')
	urlList = json.load(main_file)
	index=0

	# try possible attacks in json file
	for key,value in data2.iteritems():
		index=index+1
		tempScriptFile = open("exploitScripts/attack"+str(index)+".sh",'w')
		tempScriptFile.write("#!/bin/bash \n")
		tempScriptFile.write("python attack"+str(index)+".py \n")
		tempScriptFile.close()
		tempPyFil = open("exploitScripts/attack"+str(index)+".py",'w')
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
		tempPyFil.write("from selenium import webdriver\n")
		tempPyFil.write("from selenium.webdriver.common.keys import Keys\n")
		tempPyFil.write("import httplib as http, urllib as url\n")
		tempPyFil.write("\n")
		tempPyFil.write("driver = webdriver.Firefox()\n")
		# loginRequired = true then login and load the url
		# two urls required -> one for login and other as the attack
		if (loginCheck == "true"):
			login(tempPyFil,uname,passwd,loginURL,usernameID,passwdID)
			#login successful, now use the attack url
			if(method == "POST"):
				fieldID = keyValues.get("fieldID")
				fieldVal = keyValues.get("fieldValue",None)
				buttonID = keyValues.get("buttonID",None)
				postAttack(tempPyFil,url1,fieldID,fieldVal,buttonID)
			else:
				tempPyFil.write("driver.get(\""+str(url1)+"\")\n")
		#if loginRequired is false then two attack options:
		# 1) Login attack
		# 2) No login, only attack by the url
		else:
			if(uname or passwd):
				login(tempPyFil,uname,passwd,loginURL,usernameID,passwdID)
			else:
				#if the attack is a only using url then it may be using a post request
				methodVal = keyValues.get("method","GET")
				if(methodVal == "POST"):
					fieldID = keyValues.get("fieldID")
					fieldVal = keyValues.get("fieldValue",None)
					buttonID = keyValues.get("buttonID",None)
					postAttack(tempPyFil,url1,fieldID,fieldVal,buttonID)
				else:
					tempPyFil.write("driver.get(\""+str(url1)+"\")\n")
		tempPyFil.close()




