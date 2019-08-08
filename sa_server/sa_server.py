import time
import datetime
import argparse
import sys
import os
from os import curdir, sep
from http.server import HTTPServer, BaseHTTPRequestHandler,SimpleHTTPRequestHandler
from http.cookies import SimpleCookie
import ssl
from io import BytesIO
import socket
import requests
import urllib
import time
from datetime import datetime
import traceback
import mimetypes

# Written by Jacob Wilkin (Greenwolf)

#SSL Certificate Generation https://www.sslforfree.com
#Follow Instructions to get certificates
#Combine certificates private.key,certificate.crt,ca_bundle.crt in that order in new file called cert.pem
#Place in same folder as server.py, only web/ will be served so this isn't made public. 

# Using the server to server a macro word document
# server.py -f macro.doc

# Logging Format
# IP - datetime timezone - User Agent - Command Path

#class MyServer(SocketServer.TCPServer):
#
#    def handle_error(self, request, client_address):
#        pass

class SocialAttackHTTPRequestHandler(BaseHTTPRequestHandler):

	#Supress logging messages
	def log_message(self, format, *args):
		return

	# Blank Get
	def do_GET(self):

		#Overwrite 'Server: BaseHTTP/0.6 Python/3.7.2+' response header
		self.server_version = "Microsoft-IIS/7.0"
		self.sys_version = ""

		# extract IP
		client_address = self.client_address[0]

		# Extract datetime
		# [17/Jun/2019 23:30:25]
		datetime_stamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

		# Extract timezone
		tzname = time.tzname

		# Extract Command 
		command = self.command

		# Extract Path
		path = self.path

		# Extract User Agent
		user_agent = ""
		for header in str(self.headers).split("\n"):
			if "User-Agent:" in header:
				user_agent = header

		#Log info
		log_file = open("../social_attacker_server.log", "a")
		log_file.write(str(client_address) + " - "  + str(datetime_stamp) + " " + str(tzname[0]) + " - " + str(user_agent) + " - " + str(command) + " " + str(path) + "\n")
		log_file.close()

		if args.vv == True:
			print(str(client_address) + " - "  + str(datetime_stamp) + " " + str(tzname[0]) + " - " + str(user_agent) + " - " + str(command) + " " + str(path))

		global file
		# If file not specified, find file
		try:
			if file == "":
				f = open(curdir + sep + self.path.split("?")[0], 'rb')
				#print(curdir + sep + file)
				self.send_response(200)
				self.send_header('Content-type',str(mimetypes.guess_type(curdir + sep + self.path)[0]))
				self.end_headers()
				self.wfile.write(f.read())
				f.close()
			# If file is provided, always redirect to file
			else:
				f = open(curdir + sep + file, 'rb')
				#print(curdir + sep + file)
				self.send_response(200)
				self.send_header('Content-type',str(mimetypes.guess_type(curdir + sep + file)[0]))
				self.send_header('Content-disposition',"attachment; filename=\"" + file + "\"")
				self.end_headers()
				self.wfile.write(f.read())
				f.close()
		except:
			#traceback.print_exc()
			self.send_response(404)
			self.end_headers()
			self.wfile.write(b'Error')
		time.sleep(0.5)
	
parser = argparse.ArgumentParser(
		formatter_class=argparse.RawDescriptionHelpFormatter,
		description='Social Attacker server.py by Jacob Wilkin(Greenwolf)',
		usage='%(prog)s -p <port>')

parser.add_argument('-v', '--version', action='version',version='%(prog)s 0.1.0 : Social Attacker server.py by Greenwolf (https://github.com/Greenwolf/social_attacker)')
parser.add_argument('-vv', '--verbose', action='store_true',dest='vv',help='Verbose Mode')
parser.add_argument('-p', '--port',action='store', dest='port',required=False,help='Port server is listening on, default is 443/tcp')
parser.add_argument('-f', '--file',action='store', dest='file',required=False,help='File to serve in web directory, example: macro.doc. This is useful if you use a tracking ID without a path such as https://mysite.com/[TRACKING_ID]')
args = parser.parse_args()

port = 443
if args.port:
	port = int(args.port)

print('Saving log output to: social_attacker_server.log')
cwd = os.getcwd()
certlocation = cwd + "/cert.pem"
#print(certlocation)
web_dir = os.path.join(os.path.dirname(__file__), 'web')
os.chdir(web_dir)
print('Serving content in: ' + cwd + "/" + web_dir)

# If file is provided set up global variable for it, else set to empty string
global file 
if args.file:
	file = args.file
else:
	file = ""

try:
	httpd = HTTPServer(("",port), SocialAttackHTTPRequestHandler)
	#httpd = MyServer.TCPServer(("",port), SocialAttackHTTPRequestHandler)
	httpd.socket = ssl.wrap_socket (httpd.socket, 
			keyfile=certlocation, 
			certfile=certlocation, server_side=True)
	print('Server started...')
	httpd.serve_forever()
except KeyboardInterrupt:
	print('Shutting down server')
	httpd.socket.close()
