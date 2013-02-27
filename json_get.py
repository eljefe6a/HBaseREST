#!/usr/bin/env python
from common import *
import json
import base64
import requests

# Get the bleats
request = requests.get(baseurl + "/" + tablename + "/shakespeare-comedies-*", headers={"Accept" : "application/json"})

if issuccessful(request) == False:
	print "Could not get messages from HBase. Text was:\n" + request.text
	quit()

bleats = json.loads(request.text)

for row in bleats['Row']:
	message = ''
	lineNumber = 0
	username = ''

	for cell in row['Cell']:
		columnname = base64.b64decode(cell['column'])
		value = cell['$']
		
		if value == None:
			continue

		if columnname == cfname + ":" + messagecolumn:
			message = base64.b64decode(value)
		elif columnname == cfname + ":" + linenumbercolumn:
			lineNumber = decode(str(value))
		elif columnname == cfname + ":" + usernamecolumn:
			username = base64.b64decode(value)

	rowKey = base64.b64decode(row['key'])

	# Output only messages whose line numbers are divisible by 10
	# and have the word again in them.
	if lineNumber % 10 == 0 and message.find("again") != -1:
		print(rowKey + ":" + str(lineNumber) + ":" + username + ":" + message);
		