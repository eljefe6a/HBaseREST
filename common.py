#!/usr/bin/env python
import struct
import base64

baseurl = "http://localhost:8070"

tablename = "messagestable"
cfname = "messages"
messagecolumn = "message"

usernamecolumn = "username"
linenumbercolumn = "line"
username = "shakespeare"

linenumbercolumnencoded = base64.b64encode(cfname + ":" + linenumbercolumn)
usernamecolumnencoded = base64.b64encode(cfname + ":" + usernamecolumn)
messagecolumnencoded = base64.b64encode(cfname + ":" + messagecolumn)

# Method for encoding ints with base64 encoding
def encode(n):
	data = struct.pack("i", n)
	s = base64.b64encode(data)
	return s

# Method for decoding ints with base64 encoding 
def decode(s):
	data = base64.b64decode(s)
	n = struct.unpack("i", data)
	return n[0]

# Checks the request object to see if the call was successful
def issuccessful(request):
	if 200 <= request.status_code and request.status_code <= 299:
		return True
	else:
		return False