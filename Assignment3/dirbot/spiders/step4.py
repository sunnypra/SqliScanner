#!/usr/bin/python
import json
import time

# store all values for one url in a dictionary
def getKeyValue(params,keyValues):
	paramsDic = params[0]
	for key,value in paramsDic.iteritems():
		if type(value) is list:
			getKeyValue(value,keyValues)
		else:
			keyValues[key]=value


#find the login url from url1
def findLoginURL():
	main_file1 = open("Singleinput.json",'r')
	infoList12 = json.load(main_file1)
	infoList11 = infoList12[0]
	for key11,value11 in infoList11.iteritems():
		loginURL = value11[0].get("loginurl")
		return loginURL;

#login function
def login(tempPyFil,uname,passwd,loginURL,usernameID,passwdID):

	tempPyFil.write("driver.get(\""+str(loginURL)+"\")\n")
	tempPyFil.write("loginURL=\""+str(loginURL)+"\"\n")
	tempPyFil.write("if (len(driver.find_elements_by_name(\"" + str(usernameID) + "\")) > 0):\n")
	tempPyFil.write("\tnameele = driver.find_element_by_name(\"" + str(usernameID) + "\")\n")
	tempPyFil.write("elif (len(driver.find_elements_by_id(\"" + str(usernameID) + "\")) > 0):\n")
	tempPyFil.write("\tnameele = driver.find_element_by_id(\""+str(usernameID)+"\")\n")
	tempPyFil.write("nameele.send_keys(\""+ str(uname) + "\")\n\n")

	tempPyFil.write("if (len(driver.find_elements_by_name(\"" + str(passwdID) + "\")) > 0):\n")
	tempPyFil.write("\tpassele = driver.find_element_by_name(\"" + str(passwdID) + "\")\n")
	tempPyFil.write("elif (len(driver.find_elements_by_id(\"" + str(passwdID) + "\")) > 0):\n")
	tempPyFil.write("\tpassele = driver.find_element_by_id(\""+str(passwdID)+"\")\n")
	tempPyFil.write("passele.send_keys(\""+ str(passwd) + "\")\n\n")

	tempPyFil.write("if (len(driver.find_elements_by_name(\"login\")) > 0):\n")
	tempPyFil.write("\tloginele = driver.find_element_by_name(\"login\")\n")
	tempPyFil.write("elif (len(driver.find_elements_by_id(\"login\")) > 0):\n")
	tempPyFil.write("\tloginele = driver.find_element_by_id(\"login\")\n")
	tempPyFil.write("elif (len(driver.find_elements_by_name(\"Login\")) > 0):\n")
	tempPyFil.write("\tloginele = driver.find_element_by_name(\"Login\")\n")
	tempPyFil.write("elif (len(driver.find_elements_by_id(\"Login\")) > 0):\n")
	tempPyFil.write("\tloginele = driver.find_element_by_id(\"Login\")\n")
	tempPyFil.write("else:\n")
	tempPyFil.write("\tinp_elems = driver.find_elements_by_tag_name('input')\n")
	tempPyFil.write("\tfor i in inp_elems:\n")
	tempPyFil.write("\t\tif (((i.get_attribute('type') == 'button') or (i.get_attribute('type') == 'submit')) &\n")
	tempPyFil.write("\t\t((i.get_attribute('value') == 'Login') or (i.get_attribute('value') == 'login'))):\n")
	tempPyFil.write("\t\t\ti.click()\n")
	tempPyFil.write("\t\t\turl2= driver.current_url\n")

	tempPyFil.write("\t\t\tif(url2 == loginURL):\n")
	tempPyFil.write("\t\t\t\tprint \"login attempt failed\"\n")
	tempPyFil.write("\t\t\telse:\n")
	tempPyFil.write("\t\t\t\tdriver.get(url2)\n")
	tempPyFil.write("\t\t\t\tprint \"login successful\"\n")
	tempPyFil.write("\t\t\t\tbreak\n\n")
	tempPyFil.write("if(loginele is not None):\n")
	tempPyFil.write("\tloginele.click()\n")


# attack if the method is post
def	postAttack(tempPyFil,url1,fieldID,fieldValue,buttonID):
	tempPyFil.write("driver.get(\""+str(url1)+"\")\n")
	tempPyFil.write("url=\""+str(url1)+"\"\n")
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
	tempPyFil.write("\t\t\tif (len(driver.find_elements_by_name(\"" + str(buttonID) + "\")) > 0):\n")
	tempPyFil.write("\t\t\t\tbuttonEle = driver.find_element_by_name(\"" + str(buttonID) + "\")\n")
	tempPyFil.write("\t\t\telif (len(driver.find_elements_by_id(\"" + str(buttonID) + "\")) > 0):\n")
	tempPyFil.write("\t\t\t\tbuttonEle = driver.find_element_by_id(\"" + str(buttonID) + "\")\n")
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
	inx=0;

	# try possible attacks in json file
	for key,value in data2.iteritems():
		inx=inx+1;
		ind=time.time();
		index=str(inx)+str(ind);
		tempScriptFile = open("exploitScripts/attack"+str(index)+".sh",'w')
		tempScriptFile.write("#!/bin/bash \n")
		tempScriptFile.write("python attack"+str(index)+".py \n")
		tempScriptFile.close()
		tempPyFil = open("exploitScripts/attack"+str(index)+".py",'w')
		url1 = str(key)
		print url1
		getKeyValue(value,keyValues)

		#get login url
		#loginURL= findLoginURL()
		loginURL=""

		# check if attack is using a url only,no login required 
		loginCheck = keyValues.get("LoginRequired","false")
		uname = keyValues.get("username",None)
		passwd = keyValues.get("password",None)
		usernameID = keyValues.get("loginid",None)
		passwdID = keyValues.get("passid",None)
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
				fieldID = keyValues.get("fieldid")
				fieldVal = keyValues.get("fieldValue",None)
				buttonID = keyValues.get("buttonid",None)
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
					fieldID = keyValues.get("fieldid")
					fieldVal = keyValues.get("fieldValue",None)
					buttonID = keyValues.get("buttonid",None)
					postAttack(tempPyFil,url1,fieldID,fieldVal,buttonID)
				else:
					tempPyFil.write("driver.get(\""+str(url1)+"\")\n")
		tempPyFil.close()
		tempLinkFile = open("attackURLnFile.txt",'a');
		tempLinkFile.write(" (filename) attack" + str(index) + ".txt : (Attack URL) "+ str(url1) + "\n\n");
		tempLinkFile.close()




