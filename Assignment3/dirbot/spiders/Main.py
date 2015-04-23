import json
import os
import subprocess

#MAIN PROCESSSING
temp_file = open("input.json",'r')
data = json.load(temp_file)
data2 = data[0]
index=0

# call scanner for all values in the input file
for key,value in data2.iteritems():
	abc = []
	tempKey = key
	tempValue = value
	if ((type(value) is list) & (len(tempValue)>1)):
		index=len(tempValue)
		while (index!=0):
			abc=[]
			index=index-1
			value1 = [tempValue[index]]
			print "typ1"
			print type(value1)
			if ((value1[0].get("params")[0].get("username") is None)
			or (value1[0].get("params")[0].get("password") is None)):
				value1[0]["loginRequired"]="false"
			else:
				value1[0]["loginRequired"]="true"
			abc.append({key:value1})
			f1 = open("Singleinput.json",'w')
			print abc
			f1.write(json.dumps(abc, indent=4))
			f1.close()
#			os.system("scrapy crawl step1 > abc.txt")
#			os.system("scrapy crawl step1login > abc1.txt")
#			os.system("scrapy crawl step3 -s LOG_ENABLED=0")
#			os.system("python -c 'import step4; print step4.main();'")
	else:
		print type(value[0])
		print (value[0])
		if ((value[0].get("params")[0].get("username") is None)
			or (value[0].get("params")[0].get("password") is None)):
				value[0]["loginRequired"]="false"
		else:
				value[0]["loginRequired"]="true"
		abc.append({key:value})
		f1 = open("Singleinput.json",'w')
		print abc
		f1.write(json.dumps(abc, indent=4))
		f1.close()
#		os.system("scrapy crawl step1 > abc.txt")
#		os.system("scrapy crawl step1login > abc1.txt")
#		os.system("scrapy crawl step3 -s LOG_ENABLED=0")
#		os.system("python -c 'import step4; print step4.main();'")
#subprocess.Popen(["scrapy","crawl","step1"])
#subprocess.Popen(["scrapy","crawl","step1login"])
#subprocess.Popen(["scrapy","crawl","step3","-s","LOG_ENABLED=0"])
#subprocess.Popen(["python -c 'import step4; print step4.main();'"])

