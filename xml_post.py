#!/usr/bin/env python
from common import *
import requests
import os
import os.path
from xml.etree.ElementTree import Element, SubElement, tostring, fromstring

# Delete table if it exists
request = requests.get(baseurl + "/" + tablename + "/schema", headers={"Accept" : "application/json"})

if issuccessful(request):
	request = requests.delete(baseurl + "/" + tablename + "/schema", headers={"Accept" : "application/json"})

	if issuccessful(request):
		print "Deleted table " + tablename
	else:
		print "Errored out.  Status code was " + str(request.status_code) + "\n" + request.text

# Create Messages Table
content =  '<?xml version="1.0" encoding="UTF-8"?>'
content += '<TableSchema name="' + tablename + '">'
content += '  <ColumnSchema name="' + cfname + '" />'
content += '</TableSchema>'

request = requests.post(baseurl + "/" + tablename + "/schema", data=content, headers={"Content-Type" : "text/xml", "Accept" : "text/xml"})

if issuccessful(request):
	print "Created table " + tablename
else:
	print "Errored out while creating table.  Status code was " + str(request.status_code) + "\n" + request.text
	quit()


# Create a message for every work of Shakespeare
sourceDir = "shakespeare"

for filename in os.listdir(sourceDir):
	shakespeare = open(os.path.join(sourceDir, filename), "rb")
	
	cellset = Element('CellSet')
	
	linenumber = 0;
		 
	for line in shakespeare:		
		rowKey = username + "-" + filename + "-" + str(linenumber).zfill(6)
		rowKeyEncoded = base64.b64encode(rowKey)
		
		row = SubElement(cellset, 'Row', key=rowKeyEncoded)
		
		messageencoded = base64.b64encode(line.strip())
		linenumberencoded = encode(linenumber)
		usernameencoded = base64.b64encode(username)
		
		# Add message cell
		cell = SubElement(row, 'Cell', column=messagecolumnencoded)
		cell.text = messageencoded
		
		# Add username cell
		cell = SubElement(row, 'Cell', column=usernamecolumnencoded)
		cell.text = usernameencoded
		
		# Add Line Number cell
		cell = SubElement(row, 'Cell', column=linenumbercolumnencoded)
		cell.text = linenumberencoded
				
		linenumber = linenumber + 1
		
	# Submit XML to REST server
	request = requests.post(baseurl + "/" + tablename + "/fakerow", data=tostring(cellset), headers={"Content-Type" : "text/xml", "Accept" : "text/xml"})

	if issuccessful(request):
		print "Added messages for " + filename
	else:
		print "Errored out while loading data.  Status code was " + str(request.status_code) + "\n" + request.text
		quit()

