#!/usr/bin/env python
from common import *
import json
import base64
import requests
import os
import os.path
from ordereddict import OrderedDict

# Delete table if it exists
request = requests.get(baseurl + "/" + tablename + "/schema")

if issuccessful(request):
	request = requests.delete(baseurl + "/" + tablename + "/schema")

	if issuccessful(request):
		print "Deleted table " + tablename
	else:
		print "Errored out.  Status code was " + str(request.status_code) + "\n" + request.text
		

# Create Messages Table
content =  '<?xml version="1.0" encoding="UTF-8"?>'
content += '<TableSchema name="' + tablename + '">'
content += '  <ColumnSchema name="' + cfname + '" />'
content += '</TableSchema>'

# This JSON may work for table creation, but I haven't tried it
# {"name":"test5", "column_families":[{
#>              "name":"columnfam1",
#>              "bloomfilter":true,
#>              "time_to_live":10,
#>              "in_memory":false,
#>              "max_versions":2,
#>              "compression":"", 
#>              "max_value_length":50,
#>              "block_cache_enabled":true
#>           }
#> ]}

request = requests.post(baseurl + "/" + tablename + "/schema", data=content, headers={"Content-Type" : "text/xml", "Accept" : "text/xml"})

if issuccessful(request):
	print "Created table " + tablename
else:
	print "Errored out while creating table.  Status code was " + str(request.status_code) + "\n" + request.text
	quit()


# Create a message  for every work of Shakespeare
sourceDir = "shakespeare"

for filename in os.listdir(sourceDir):
	shakespeare = open(os.path.join(sourceDir, filename), "rb")
	
	lineNumber = 0;
	
	rows = []
	jsonOutput = { "Row" : rows }
	
	for line in shakespeare:
		rowKey = username + "-" + filename + "-" + str(lineNumber).zfill(6)
		rowKeyEncoded = base64.b64encode(rowKey)
		
		line = base64.b64encode(line.strip())
		lineNumberEncoded = encode(lineNumber)
		usernameEncoded = base64.b64encode(username)
	
		cell = OrderedDict([
			("key", rowKeyEncoded),
			("Cell", 
			[
				{ "column" : messagecolumnencoded, "$" : line },
				{ "column" : usernamecolumnencoded, "$" : usernameEncoded },
				{ "column" : linenumbercolumnencoded, "$" : lineNumberEncoded },
			])
		])
		
		rows.append(cell)
		
		lineNumber = lineNumber + 1
		
	# Submit JSON to REST server
	request = requests.post(baseurl + "/" + tablename + "/" + rowKey, data=json.dumps(jsonOutput), headers={"Content-Type" : "application/json", "Accept" : "application/json"})

	if issuccessful(request):
		print "Added messages for " + filename
	else:
		print "Errored out while loading data.  Status code was " + str(request.status_code) + "\n" + request.text
		quit()
