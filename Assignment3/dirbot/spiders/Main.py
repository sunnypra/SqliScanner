import json
import os

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
			newList = tempValue[index]
			value1 = [tempValue[index]]
			abc.append({key:value1})
			f1 = open("Singleinput.json",'w')
			f1.write(json.dumps(abc, indent=4))
			f1.close()
			#os.system("scrapy crawl Group5 > abc.txt")
			#os.system("scrapy crawl step3 -s LOG_ENABLED=0")
			os.system("sh Main.sh")
			#os.system("python step4.py")

	else:
		abc.append({key:value})
		f1 = open("Singleinput.json",'w')
		f1.write(json.dumps(abc, indent=4))
		f1.close()
		#os.system("scrapy crawl Group5 > abc.txt")
		#os.system("scrapy crawl step3 -s LOG_ENABLED=0")
		os.system("sh Main.sh")
		#os.system("python step4.py")
