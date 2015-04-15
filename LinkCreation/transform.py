import json
import copy
from pprint import pprint

with open('file1.json') as data_file:
    data = json.load(data_file)

payloadtxt = open('payload.txt')
payloads = payloadtxt.readlines()
links = open('temp.txt','w')

for key1, value1 in data.items():
    for val in value1:
        jsonval = json.dumps(val)
        data2 = json.loads(jsonval)
        for key2, value2 in data2.items():
            if type(value2).__name__=="unicode":
                        for payload in payloads:
                            links.write("http:/"+key1+key2+"?"+value2+payload+"\n")
                            if "&" in value2:
                                queryVals = value2.split('&')
                                length = len(queryVals)
                                for i in range(0,length-1):
                                    dupVals = copy.copy(queryVals);
                                    dupVals[i] = dupVals[i]+""+payload
                                    finQuery = "";
                                    for dupVal in dupVals:
                                        finQuery += "&"+dupVal
                                    final2 = "http:/"+key1+key2+"?"+finQuery
                                    links.write(final2+"\n")

links.close()
finalfile = open('linksWithPayloads.txt','w')
with open('temp.txt','r') as temp:
    for line in temp:
        if line.strip():
            finalfile.write(line)
finalfile.close()

