#!/usr/bin/env python
from common import *
import base64
import requests
from xml.etree.ElementTree import Element, SubElement, tostring, fromstring

# Get the messages
request = requests.get(baseurl + "/" + tablename + "/shakespeare-comedies-*", headers={"Accept" : "text/xml"})

if issuccessful(request) == False:
	print "Could not get request.  Status code " + str(request.status_code) + ". Output:\n" + request.text
	quit()

root = fromstring(request.text)

# Go through every row passed back
for row in root:
	message = ''
	linenumber = 0
	username = ''
	
	# Go through every cell in the row
	for cell in row:
		columnname = base64.b64decode(cell.get('column'))

		if cell.text == None:
			continue
	
		if columnname == cfname + ":" + messagecolumn:
			message = base64.b64decode(cell.text)
		elif columnname == cfname + ":" + linenumbercolumn:
			linenumber = decode(cell.text)
		elif columnname == cfname + ":" + usernamecolumn:
			username = base64.b64decode(cell.text)

	rowKey = base64.b64decode(row.get('key'))

	if linenumber % 10 == 0 and message.find("again") != -1:
		print(rowKey + ":" + str(linenumber) + ":" + username + ":" + message);
