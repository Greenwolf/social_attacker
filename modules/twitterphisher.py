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




class Twitterphisher(object):

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
		self.driver.delete_all_cookies()


	def doLogin(self,username,password):

		self.driver.get("https://twitter.com/login")
		self.driver.execute_script('localStorage.clear();')

		#agent = self.driver.execute_script("return navigator.userAgent")
		#print("User Agent: " + agent)
		
		if(self.driver.title.encode('ascii','replace').startswith(bytes("Login on", 'utf-8'))):
			print("\n[+] Twitter Login Page loaded successfully [+]")
			try:
				twUsername = self.driver.find_element_by_class_name("js-username-field")
				#print("debug username")
			except:
				print("Twitter Login Page username field seems to have changed, please make an issue on: https://github.com/Greenwolf/social_attacker")
				sys.exit()
			twUsername.send_keys(username)
			sleep(2)

			try:
				#twPassword = self.driver.find_element_by_xpath("//input[@class='js-password-field']")

				twPassword = self.driver.find_element_by_class_name("js-password-field")
				#print("debug password")
			except:
				print("Twitter Login Page password field seems to have changed, please make an issue on: https://github.com/Greenwolf/social_attacker")
				sys.exit()
			twPassword.send_keys(password)
			sleep(2)

			try:
				twLoginButton = self.driver.find_element_by_xpath("//button[@class='submit EdgeButton EdgeButton--primary EdgeButtom--medium']")
				#print("debug loginbutton")
			except:
				print("Twitter Login Page login button name seems to have changed, please make an issue on: https://github.com/Greenwolf/social_attacker")
				traceback.print_exc()
				sys.exit()
			twLoginButton.click()
			sleep(5)

			if(self.driver.title.encode('ascii','replace').startswith(bytes("Login on", 'utf-8'))):
				print("[-] Twitter Login Failed [-]\n")
			else:
				print("[+] Twitter Login Success [+]\n")
		else:
			print("Twitter Login Page title field seems to have changed, please make an issue on: https://github.com/Greenwolf/social_attacker")

	def addTwitterProfile(self,twitterprofile,username,password):
		self.driver.get(twitterprofile)
		#print("DEBUG: after navigate")
		sleep(3)
		if "login" in self.driver.current_url: 
			self.doLogin(username,password)
			self.driver.get(url)
			sleep(3)
			if "login" in self.driver.current_url: 
				print("Twitter Timeout Error, session has expired and attempts to reestablish have failed")
			else:
				print("New Twitter Session created, resuming activity")
		try:
			#print("DEBUG: Clicking Add")
			#Locate follow button in page, click it
			#follow_button = self.driver.find_element_by_xpath("//button[@class='EdgeButton EdgeButton--secondary EdgeButton--medium button-text follow-text']")
			if len(self.driver.find_elements_by_xpath("//div[@class='user-actions btn-group following not-muting including ']")) == 1 or len(self.driver.find_elements_by_xpath("//div[@class='user-actions btn-group following not-muting can-dm including ']")):
				print("Already following: " + twitterprofile)
			else:
				follow_button = self.driver.find_elements_by_class_name("user-actions-follow-button")[0]
				follow_button.click()
				sleep(3)
		except:
			print("Error Adding Friend: %s" % (twitterprofile))
			traceback.print_exc()


	def checkTwitterProfile(self,twitterprofile,username,password):
		self.driver.get(twitterprofile)
		sleep(3)
		if "login" in self.driver.current_url: 
			self.doLogin(username,password)
			self.driver.get(url)
			sleep(3)
			if "login" in self.driver.current_url: 
				print("Twitter Timeout Error, session has expired and attempts to reestablish have failed")
			else:
				print("New Twitter Session created, resuming activity")
		try:
			#All of these are xpaths for the connect/messagelock/message button on the profile page, it uses the button classes to identify the stats of the request, 
			#there are 3 states, unconnected, request sent, and connected. It's not possible to know if a request is waiting to be accepted or has been rejected. 
			if len(self.driver.find_elements_by_xpath("//div[@class='user-actions btn-group following not-muting including ']")) == 1 or len(self.driver.find_elements_by_xpath("//div[@class='user-actions btn-group following not-muting can-dm including ']")): # Target Accepted add request
				return "Following"
			elif len(self.driver.find_elements_by_xpath("//div[@class='user-actions btn-group not-following not-muting ']")) == 1 or len(self.driver.find_elements_by_xpath("//div[@class='user-actions btn-group not-following not-muting can-dm ']")): # Target has been been added yet, so theres 3 add buttons o page
				print("This Twitter profile has not been followed to yet, are you running this in the correct order?")
				return "NotFollowing"
			else:
				#This should never be reached, if it is it means the Twitter profile page code has changed. 
				print("Error Identifying Connection Request Status for:" + twitterprofile)
				print("This could be due to a code change in Twitter, please make an issue on the github page.")
				return "Unknown"
		except: 
			traceback.print_exc()
			return "Error"

	def checkThenPhishTwitterProfile(self,twitterprofile,message,username,password):
		self.driver.get(twitterprofile)
		sleep(5)
		if "login" in self.driver.current_url: 
			self.doLogin(username,password)
			self.driver.get(url)
			sleep(3)
			if "login" in self.driver.current_url: 
				print("Twitter Timeout Error, session has expired and attempts to reestablish have failed")
			else:
				print("New Twitter Session created, resuming activity")
		try:
			#All of these are xpaths for the connect/messagelock/message button on the profile page, it uses the button classes to identify the stats of the request, 
			#there are 3 states, unconnected, request sent, and connected. It's not possible to know if a request is waiting to be accepted or has been rejected. 
			if len(self.driver.find_elements_by_xpath("//div[@class='user-actions btn-group following not-muting including ']")) == 1 or len(self.driver.find_elements_by_xpath("//div[@class='user-actions btn-group following not-muting can-dm including ']")): # Target Accepted add request
				try:
					#self.driver.find_elements_by_xpath("//div[@class='_42ft _4jy0 _4jy4 _517h _51sy']")[0].click()
					tweet_to_button = self.driver.find_element_by_xpath("//button[@class='NewTweetButton u-sizeFull js-tooltip EdgeButton EdgeButton--primary  u-textTruncate']")
					tweet_to_button.click()
					sleep(5)

					#Use current click position with ActionChains, as it auto focuses the cursor
					actions = ActionChains(self.driver)
					actions.send_keys(message)
					sleep(2)
					actions.perform()
					sleep(2)

					#This should click the tweet button
					tweet_send_button = self.driver.find_element_by_xpath("//button[@class='tweet-action EdgeButton EdgeButton--primary js-tweet-btn']")
					tweet_send_button.click()

					sleep(2)
					return "Sent"
				except:
					traceback.print_exc()
					print("Connection has accepted, but message sending failed, possible code issue")
					return "Error"
			elif len(self.driver.find_elements_by_xpath("//div[@class='user-actions btn-group not-following not-muting ']")) == 1 or len(self.driver.find_elements_by_xpath("//div[@class='user-actions btn-group not-following not-muting can-dm ']")): # Target has been been added yet, so theres 3 add buttons o page
				print("This Twitter profile has not been followed to yet, are you running this in the correct order?")
				return "NotFollowing"
			else:
				#This should never be reached, if it is it means the Twitter profile page code has changed. 
				print("Error Identifying Connection Request Status for:" + twitterprofile)
				print("This could be due to a code change in Twitter, please make an issue on the github page.")
				return "Unknown"
		except: 
			traceback.print_exc()
			return "Error"

	def generateMarkovMessageForTwitterProfile(self,twitterprofile,markovlength,username,password):
		self.driver.get(twitterprofile)
		sleep(3)

		if "login" in self.driver.current_url: 
			self.doLogin(username,password)
			self.driver.get(url)
			sleep(3)
			if "login" in self.driver.current_url: 
				print("Twitter Timeout Error, session has expired and attempts to reestablish have failed")
			else:
				print("New Twitter Session created, resuming activity")
		# This is rough code, not sure if len=0 will return correctly, or if it will crash?
		try:
			# Code here to fill array of timeline post strings
			# Code to scroll down the page, either to bottom or 50 times height of screen
			SCROLL_PAUSE_TIME = 2
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

			#print("DEBUG TEST: Markov Twitter Creation33")
			timeline_text = [] # create empty array to hold timeline post strings for processing

			# Code to extract all posts, this pulls out all posts on timeline
			#self.driver.find_elements_by_xpath("//div[@class='_5pcb _4b0l _2q8l']").click()
			# Extract page source from selenium, then use beautifulsoup to extract data
			searchresponse = self.driver.page_source.encode('utf-8')
			soupParser = BeautifulSoup(searchresponse, 'html.parser')
			# scrape out all posts from the source code
			for postelement in soupParser.find_all('div', {'class': 'js-tweet-text-container'}):
				try: # Try to pull out all of the user written posts with their paragraphs
					# Pull out 3rd href element, this is the posters name on a post

					postcontents = postelement.find_all('p')
					for paragraph in postcontents:
						timeline_text.append(paragraph.get_text())
							#print(paragraph)
				except:
					traceback.print_exc()
					pass

			#print("----------------------------")
			#print(timeline_text)
			#print("----------------------------")
			processed_timeline_text = []
			# Do some processing on timeline posts, 'a href' has already been removed by not including.
			for post in timeline_text:
				# Strip out urls that have http/https
				#processed_post = post.replace("hashtag#","#")
				processed_post = post
				processed_timeline_text.append(processed_post)
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

