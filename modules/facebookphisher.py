from __future__ import print_function
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from pyvirtualdisplay import Display
from time import sleep
import sys
import json
import os
import markovify
from bs4 import BeautifulSoup
import traceback
import re
import requests
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys



class Facebookphisher(object):

	timeout = 10

	def __init__(self,showbrowser):
		display = Display(visible=0, size=(1600, 1024))
		display.start()
		if not showbrowser:
			os.environ['MOZ_HEADLESS'] = '1'
		firefoxprofile = webdriver.FirefoxProfile()
		firefoxprofile.set_preference("permissions.default.desktop-notification", 1)
		firefoxprofile.set_preference("dom.webnotifications.enabled", 1)
		firefoxprofile.set_preference("dom.push.enabled", 1)
		self.driver = webdriver.Firefox(firefox_profile=firefoxprofile)
		self.driver.implicitly_wait(15)
		#self.driver.delete_all_cookies()

	def doLogin(self,username,password):

		self.driver.get("https://www.facebook.com/login")
		self.driver.execute_script('localStorage.clear();')

		if(self.driver.title.encode('ascii','replace').endswith(bytes("Facebook", 'utf-8'))):
			print("\n[+] Facebook Login Page loaded successfully [+]")
			try:
				fbUsername = self.driver.find_element_by_id("email")
			except:
				print("Facebook Login Page username field seems to have changed, please make an issue on: https://github.com/Greenwolf/social_attacker")
			fbUsername.send_keys(username)
			try:
				fbPassword = self.driver.find_element_by_id("pass")
			except:
				print("Facebook Login Page password field seems to have changed, please make an issue on: https://github.com/Greenwolf/social_attacker")
			fbPassword.send_keys(password)
			try:
				fbLoginButton =  self.driver.find_element_by_id("loginbutton")
			except:
				print("Facebook Login Page login button field seems to have changed, please make an issue on: https://github.com/Greenwolf/social_attacker")				
			fbLoginButton.click()
			sleep(5)
			# checks if a notification is in place, which changes the title
			if (self.driver.title.encode('utf8','replace')[0] == "("):
				if(str(self.driver.title.encode('utf8','replace').split()[1]) == bytes("Facebook", 'utf-8')):
					print("[+] Facebook Login Success [+]\n")
				else:
					print("[-] Facebook Login Failed [-]\n")
			else:
				if(self.driver.title.encode('utf8','replace').startswith(bytes("Facebook", 'utf-8')) == True):
					print("[+] Facebook Login Success [+]\n")
				else:
					print("[-] Facebook Login Failed [-]\n")
		else:
			print("Facebook Login Page title field seems to have changed, please make an issue on: https://github.com/Greenwolf/social_attacker")


	def addFacebookProfile(self,facebookprofile,username,password):
		self.driver.get(facebookprofile)
		if(self.driver.title.encode('utf8','replace').startswith(bytes("Page not found", 'utf-8')) == True):
			print("\nFacebook session has expired attempting to reestablish...")
			self.doLogin(username,password)
			self.driver.get(facebookprofile)
			sleep(3)
			if(self.driver.title.encode('utf8','replace').startswith(bytes("Page not found", 'utf-8')) == True):
				print("Facebook Timeout Error, session has expired and attempts to reestablish have failed")
			else:
				print("New Facebook Session created, resuming adding process")
		try:
			#print("DEBUG: Clicking Add")


			#Extract "token" from facebookprofile get response, this is csrf token for request
			#Extract facebook id ("entity_id") for friend request
			
			#change user agent to firefox user agent 

			csrf_token = ""
			target_facebook_id = ""
			soup = BeautifulSoup(self.driver.page_source, 'html.parser')
			scripts = soup.find_all('script')
			for script in scripts:
				token = re.search('"token":"(.*)"},258', str(script))
				fb_id = re.search('"entity_id":"(.*)","', str(script))
				if token:
					csrf_token = token.group(1)
				if fb_id :
					target_facebook_id = fb_id.group(1)
			#print(csrf_token)
			#print(target_facebook_id)

			#Extract cookies from 
			all_cookies = self.driver.get_cookies()
			cookies = {}
			for s_cookie in all_cookies:
				cookies[s_cookie["name"]]=s_cookie["value"]

			sleep(5)
			#Use token + facebook ID + sessions cookies to make a request which adds a friend
			s = requests.Session()
			#Adding through button on profile method - UPDATE: doesnt work 100% of the time, changed to search which bypasses this
			#data = {"to_friend":target_facebook_id, "action":"add_friend", "how_found":"profile_button","__a":"1","fb_dtsg":csrf_token}
			#url = "https://www.facebook.com/ajax/add_friend/action.php"
			#referer_string = "facebookprofile" + "?epa=SEARCH_BOX"

			#adding through search method
			# to_friend: facebook ID of person to add
			# action: action to perform, add_friend
			# how_found: where in the application the request came from, we want browse to it looks like it came from a seach, not profile_button which is from the button on their profile page, this is locked down and causes errors on occasion
			# fb_dtsg: this is the csrf token for post requests, it can be extracted from the HTLM
			data = {"to_friend":target_facebook_id, "action":"add_friend", "how_found":"browse","fb_dtsg":csrf_token}
			url = "https://www.facebook.com/ajax/add_friend/action.php"
			referer_string = "https://www.facebook.com/search/top/?q=X&epa=SEARCH_BOX"
			headers = { 
				'User-Agent': 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:67.0) Gecko/20100101 Firefox/67.0',
				'Referer': referer_string,
				'Content-Type': 'application/x-www-form-urlencoded',
				'Accept': '*/*',
				'Accept-Language': 'en-US,en;q=0.5',
				'Accept-Encoding': 'gzip, deflate'
			}
			r = s.post(url, data=data, cookies=cookies, headers=headers)
			#view response, if they ever encode, might need r.content
			#print(r.text)


			#print(self.driver.find_elements_by_class_name("FriendRequestAdd"))
			#self.driver.find_elements_by_class_name("FriendRequestAdd")[0].click()
			#sleep(3)
			#print(self.driver.find_elements_by_class_name("layerCancel"))
			#self.driver.find_element_by_class_name("layerCancel").click()
			#sleep(3)
			#self.driver.find_elements_by_class_name("FriendRequestAdd")[0].click()
			#print("DEBUG: After friend request")
			sleep(3)
		except:
			print("Error Adding Friend: %s" % (facebookprofile))
			traceback.print_exc()


	def checkFacebookProfile(self,facebookprofile,username,password):
		self.driver.get(facebookprofile)

		if(self.driver.title.encode('utf8','replace').startswith(bytes("Page not found", 'utf-8')) == True):
			print("\nFacebook session has expired attempting to reestablish...")
			self.doLogin(username,password)
			self.driver.get(facebookprofile)
			sleep(3)
			if(self.driver.title.encode('utf8','replace').startswith(bytes("Page not found", 'utf-8')) == True):
				print("Facebook Timeout Error, session has expired and attempts to reestablish have failed")
			else:
				print("New Facebook Session created, resuming checking process")
		
		# This is rough code, not sure if len=0 will return correctly, or if it will crash?
		# This code relies on facebook profile page and looking at friend status button ontop of the cover photo
		try:

			if len(self.driver.find_elements_by_class_name("enableFriendListFlyout")) >= 2: # Target Accepted add request
				return "Accepted"
			elif len(self.driver.find_elements_by_class_name("FriendRequestOutgoing")) == 1: # Target Accepted add request
				return "Pending"
			elif len(self.driver.find_elements_by_class_name("FriendRequestAdd")) == 3: # Target has been been added yet, so theres 3 add buttons o page
				print("This Facebook profile has not been 'friended' yet, are you running this in the correct order?")
				return "NotAdded"
			elif len(self.driver.find_elements_by_class_name("FriendRequestAdd")) == 0: # Rejected, so no add buttons of page
				return "Rejected"
			else:
				print("Error Identifying Connection Request Status for:" + facebookprofile)
				return "Unknown"
		except: 
			traceback.print_exc()
			return "Error"

	def checkThenPhishFacebookProfile(self,facebookprofile,message,username,password):
		self.driver.get(facebookprofile)

		if(self.driver.title.encode('utf8','replace').startswith(bytes("Page not found", 'utf-8')) == True):
			print("\nFacebook session has expired attempting to reestablish...")
			self.doLogin(username,password)
			self.driver.get(facebookprofile)
			sleep(3)
			if(self.driver.title.encode('utf8','replace').startswith(bytes("Page not found", 'utf-8')) == True):
				print("Facebook Timeout Error, session has expired and attempts to reestablish have failed")
			else:
				print("New Facebook Session created, resuming phishing process")

		try:
			#if len(self.driver.find_elements_by_class_name("FriendRequestFriends")) == 1: # Target Accepted add request
			if len(self.driver.find_elements_by_class_name("enableFriendListFlyout")) >= 2: # Target Accepted add request
				# Does this XPath find manage to click on the message button?
				try:
					#self.driver.find_elements_by_xpath("//div[@class='_42ft _4jy0 _4jy4 _517h _51sy']")[0].click()
					self.driver.find_elements_by_xpath("//a[@class='_42ft _4jy0 _4jy4 _517h _51sy']")[0].click()
					sleep(2)
					#This should click in message box
					messagingbox = self.driver.find_elements_by_xpath("//div[@class='_1mf _1mj']")[1]
					messagingbox.click()

					# This should send keys
					#messagingbox.send_keys(message)
					#messagingbox.send_keys(Keys.ENTER)

					#Use current click position with ActionChains, as you can't send keyboard input to the messaging box location
					actions = ActionChains(self.driver)
					sleep(2)
					actions.send_keys(message)
					sleep(2)
					actions.send_keys(Keys.ENTER)
					sleep(2)
					actions.perform()

					# This should close window by clicking on the x
					self.driver.find_element_by_xpath("//div[@class='close']").click()
					return "Sent"
				except:
					traceback.print_exc()
					print("Connection has accepted, but message sending failed, possible code issue")
					return "Error"
			#elif len(self.driver.find_elements_by_class_name("FriendRequestOutgoing")) == 1: # Target hasn't interacted yet
			elif len(self.driver.find_elements_by_class_name("FriendRequestOutgoing")) == 1: # Target hasn't interacted yet
				return "Pending"
			elif len(self.driver.find_elements_by_class_name("FriendRequestAdd")) == 3: # Target has been been added yet
				print("This Facebook profile has not been 'friended' yet, are you running this in the correct order?")
				return "NotAdded"
			elif len(self.driver.find_elements_by_class_name("FriendRequestAdd")) == 0: # Rejected, Unable to Add Again
				return "Rejected"
			else:
				print("Error Identifying Connection Request Status for:" + facebookprofile)
				return "Unknown"
		except: 
			traceback.print_exc()
			return "Error"

	def generateMarkovMessageForFacebookProfile(self,facebookprofile,markovlength,username,password):
		self.driver.get(facebookprofile)

		if(self.driver.title.encode('utf8','replace').startswith(bytes("Page not found", 'utf-8')) == True):
			print("\nFacebook session has expired attempting to reestablish...")
			self.doLogin(username,password)
			self.driver.get(facebookprofile)
			sleep(3)
			if(self.driver.title.encode('utf8','replace').startswith(bytes("Page not found", 'utf-8')) == True):
				print("Facebook Timeout Error, session has expired and attempts to reestablish have failed")
			else:
				print("New Facebook Session created, resuming phishing process")
		# This is rough code, not sure if len=0 will return correctly, or if it will crash?
		try:
			# Code here to fill array of timeline post strings
			# Code to scroll down the page, either to bottom or 50 times height of screen
			SCROLL_PAUSE_TIME = 0.5
			# Get scroll height
			last_height = self.driver.execute_script("return document.body.scrollHeight")
			breakoutcount = 0
			while True:
				# Scroll down to bottom
				self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

				# Wait to load page
				sleep(SCROLL_PAUSE_TIME)

				# Calculate new scroll height and compare with last scroll height
				new_height = self.driver.execute_script("return document.body.scrollHeight")
				if (new_height == last_height or breakoutcount > 100):
					sleep(SCROLL_PAUSE_TIME*4)
					self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
					sleep(SCROLL_PAUSE_TIME)
					new_height = self.driver.execute_script("return document.body.scrollHeight")
					if (new_height == last_height or breakoutcount > 100):
						break
				last_height = new_height
				breakoutcount = breakoutcount + 1

			#print("DEBUG TEST: Markov Facebook Creation33")
			timeline_text = [] # create empty array to hold timeline post strings for processing

			# Code to extract all posts, this pulls out all posts on timeline
			#self.driver.find_elements_by_xpath("//div[@class='_5pcb _4b0l _2q8l']").click()
			# Extract page source from selenium, then use beautifulsoup to extract data
			searchresponse = self.driver.page_source.encode('utf-8')
			soupParser = BeautifulSoup(searchresponse, 'html.parser')

			# Extract target persons full facebook name from the top of the page
			targetfacebookname = soupParser.find('a', {'class': '_2nlw _2nlv'}).contents[0]
			# scrape out all posts from the source code
			for postelement in soupParser.find_all('div', {'class': '_5pcb _4b0l _2q8l'}):
				try: # Try to pull out all of the user written posts with their paragraphs
					# Pull out 3rd href element, this is the posters name on a post
					postername = postelement.find_all('a', href=True)[2].contents[0]

					# If postername matches targets name, this is their post, and add it to the array
					if (postername == targetfacebookname):
						postcontent = postelement.find('div', {'class': '_5pbx userContent _3576'}).find_all('p')
						posttext = ""
						# for each line/paragraph in the post
						for paragraph in postcontent:
							# for each section, a href, normal content, spans break up the content section into parts
							for section in paragraph.contents:
								try:
									try:
										# pull out normal test
										posttext = posttext + section
									except:
										try:
											# try to pull out span contents which are # hashtags like: #LovingIt 
											spancontents = section.contents[0].contents[1].contents[0]
											posttext = posttext + "#" + spancontents
										except:
											continue
											#try:
											#	# FRIEND NAMES LOOK BAD, Commenting this part out: try to pull out atag and get contents, usually a name
											#atagcontents = section.contents[0]
											#	posttext = posttext + atagcontents
											#except:
											#	continue
								except:
									continue
							posttext = posttext + "."
						#print(postername)
						#print(posttext)
						# Add post to the array
						timeline_text.append(posttext)
				except:
					pass
				try: # Code to try and pull out all news headlines from a facebook page
					#code to pull out all new post headlines
					#mbs _6m6 _2cnj _5s6c
					# Pull out 3rd href element, this is the posters name on a post
					postername = postelement.find_all('a', href=True)[2].contents[0]

					# If postername matches targets name, this is their post, and add it to the array
					if (postername == targetfacebookname):
						posttext = ""
						# Pull out news item class and href
						postcontent = postelement.find('div', {'class': 'mbs _6m6 _2cnj _5s6c'}).find('a')
						posttext = postcontent.contents
						timeline_text.append(posttext)
				except:
					pass
				try: # Code to try and pull out all link headlines from a facebook page
					postername = postelement.find_all('a', href=True)[2].contents[0]
					if (postername == targetfacebookname):
						posttext = ""
						postcontent = postelement.find('div', {'class': 'mtm _5pco'}).find('p')
						posttext = postcontent.contents[0]
						if "<span" not in str(posttext):
							timeline_text.append(posttext)
				except:
					continue

			#print("----------------------------")
			#print(timeline_text)
			#print("----------------------------")
			processed_timeline_text = []
			# Do some processing on timeline posts, 'a href' has already been removed by not including.
			for post in timeline_text:
				# Strip out urls that have http/https
				processedpost = re.sub(r'^https?:\/\/.*[\r\n]*', '', str(post), flags=re.MULTILINE)
				if processedpost != "":
					processed_timeline_text.append(processedpost)
			# Load markov models with processed timeline posts to create a message
			try:
				text_model = markovify.text.NewlineText("\n".join(processed_timeline_text))
				markovmessage = text_model.make_short_sentence(markovlength)
			except:
				markovmessage = "Error-MarkovifyCrash"
			if markovmessage is None:
				markovmessage = "Error-MarkovNoData"
			#print("Debug: Markov Message: " + str(markovmessage))
			return markovmessage
		except:
			traceback.print_exc()
			return "Error-MarkovGeneralCrash"

	def getCookies(self):
		all_cookies = self.driver.get_cookies()
		cookies = {}
		for s_cookie in all_cookies:
			cookies[s_cookie["name"]]=s_cookie["value"]
		return cookies

	def testdeletecookies(self):

		self.driver.delete_all_cookies()


	def kill(self):
		self.driver.quit()

