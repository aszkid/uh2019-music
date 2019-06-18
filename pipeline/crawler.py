import requests 
import re


stack = list() 
num = 1
burl = "https://www.ultimate-guitar.com/explore?page={}&type[]=Chords"

# for x in range(1,21): 
# 	page = requests.get(burl.format(x))
# 	# print(page.text)
# 	html = re.findall(r"window\.UGAPP\.store\.page = (.*);",page.text)
# 	print(html[0])
# 	# print(html.group(0))

import json 
import pprint

a = []
g = open("test.json","r")

for x in range(1,21):
	a.append(json.loads(g.readline()))

g.close()
print(pprint.pprint(a))