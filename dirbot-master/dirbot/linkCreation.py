import json
from pprint import pprint

links = open('linksToAttack.txt','w')

with open('data.json') as data_file:
    data = json.load(data_file)

length = len(data)
for i in range(0,length-1):
    jsonval = json.dumps(data[i])
    data2 = json.loads(jsonval)
    links.write(data2['url']+"\n")

links.close()
