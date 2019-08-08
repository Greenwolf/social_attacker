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




class Vkontaktephisher(object):

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

		self.driver.get("https://www.vk.com/login")
		self.driver.execute_script('localStorage.clear();')

		#agent = self.driver.execute_script("return navigator.userAgent")
		#print("User Agent: " + agent)
		
		if(self.driver.title.encode('ascii','replace').startswith(bytes("Log in", 'utf-8'))):
			print("\n[+] Vkontakte Login Page loaded successfully [+]")
			try:
				vkUsername = self.driver.find_element_by_id("email")
			except:
				print("Vkontakte Login Page username field seems to have changed, please make an issue on: https://github.com/Greenwolf/social_attacker")
			vkUsername.send_keys(username)
			try:
				vkPassword = self.driver.find_element_by_id("pass")
			except:
				print("Vkontakte Login Page password field seems to have changed, please make an issue on: https://github.com/Greenwolf/social_attacker")
			vkPassword.send_keys(password)

			try:
				self.driver.find_element_by_id("login_button").click()
			except:
				print("Vkontakte Login Page login button seems to have changed, please make an issue on: https://github.com/Greenwolf/social_attacker")
			sleep(5)

			if(self.driver.title.encode('ascii','replace').startswith(bytes("Log in", 'utf-8'))):
				print("[-] Vkontakte Login Failed [-]\n")
			else:
				print("[+] Vkontakte Login Success [+]\n")
		else:
			print("Vkontakte Login Page title field seems to have changed, please make an issue on: https://github.com/Greenwolf/social_attacker")

	def addVkontakteProfile(self,vkontakteprofile,username,password):
		self.driver.get(vkontakteprofile)
		#print("DEBUG: after navigate")
		sleep(3)
		if "login" in self.driver.current_url:
			self.doLogin(username,password)
			self.driver.get(url)
			sleep(3)
			if "login" in self.driver.current_url: 
				print("Vkontakte Timeout Error, session has expired and attempts to reestablish have failed")
			else:
				print("New Vkontakte Session created, resuming activity")
		try:
			#print("DEBUG: Clicking Add")
			response = self.driver.page_source.encode('utf-8')
			soup = BeautifulSoup(response, 'html.parser')
			#If not added person, add them
			#print("----")
			#print("[" + soup.find_all('div', {'class': 'page_action_left fl_l'})[0].get_text() + "]")
			#print("----")
			if "Add to Friends" in soup.find_all('div', {'class': 'page_action_left fl_l'})[0].get_text():
				#Locate connection button in page, click it
				connect_button = self.driver.find_elements_by_xpath("//button[@class='flat_button button_wide']")[0]
				connect_button.click()
			else:
				print("Already Added: " + vkontakteprofile)

			#print("DEBUG: After friend request")
			sleep(3)
		except:
			print("Error Adding Friend: %s" % (vkontakteprofile))
			traceback.print_exc()


	def checkVkontakteProfile(self,vkontakteprofile,username,password):
		self.driver.get(vkontakteprofile)
		sleep(3)
		if "login" in self.driver.current_url: 
			self.doLogin(username,password)
			self.driver.get(url)
			sleep(3)
			if "login" in self.driver.current_url: 
				print("Vkontakte Timeout Error, session has expired and attempts to reestablish have failed")
			else:
				print("New Vkontakte Session created, resuming activity")
		try:
			#All of these are xpaths for the connect/messagelock/message button on the profile page, it uses the button classes to identify the stats of the request, 
			#there are 3 states, unconnected, request sent, and connected. It's not possible to know if a request is waiting to be accepted or has been rejected. 
			response = self.driver.page_source.encode('utf-8')
			soup = BeautifulSoup(response, 'html.parser')
			if "In your friend list" in soup.find_all('div', {'class': 'page_action_left fl_l'})[0].get_text():
				return "Accepted"
			elif "Request sent" in soup.find_all('div', {'class': 'page_action_left fl_l'})[0].get_text():
				return "Pending"
			elif "Following" in soup.find_all('div', {'class': 'page_action_left fl_l'})[0].get_text():
				return "Following"
			elif "Add to Friends" in soup.find_all('div', {'class': 'page_action_left fl_l'})[0].get_text():
				print("This Vkontakte profile has not been connected to yet, are you running this in the correct order?")
				return "NotAdded"
			else:
				#This should never be reached, if it is it means the Vkontakte profile page code has changed. 
				print("Error Identifying Connection Request Status for:" + vkontakteprofile)
				print("This could be due to a code change in Vkontakte, please make an issue on the github page.")
				return "Unknown"
		except: 
			traceback.print_exc()
			return "Error"

	def checkThenPhishVkontakteProfile(self,vkontakteprofile,message,username,password):
		self.driver.get(vkontakteprofile)
		sleep(3)
		if "login" in self.driver.current_url: 
			self.doLogin(username,password)
			self.driver.get(url)
			sleep(3)
			if "login" in self.driver.current_url: 
				print("Vkontakte Timeout Error, session has expired and attempts to reestablish have failed")
			else:
				print("New Vkontakte Session created, resuming activity")

		try:
			#self.driver.find_elements_by_xpath("//div[@class='_42ft _4jy0 _4jy4 _517h _51sy']")[0].click()
			write_message_button = self.driver.find_element_by_xpath("//a[@class='button_link cut_left']")
			write_message_button.click()
			sleep(3)

			#Use current click position with ActionChains, as you can't send keyboard input to the messaging box location
			actions = ActionChains(self.driver)
			actions.send_keys(message)
			sleep(1)
			actions.perform()
			sleep(1)

			send_button = self.driver.find_element_by_xpath("//button[@class='flat_button fl_r mail_box_send_btn']")
			send_button.click()
			sleep(2)
			return "Sent"
		except: 
			traceback.print_exc()
			return "Error"
		# Commented out status checking code, as it seems like you can direct message anyone on VK, regardless of friend status
		'''		
		try:
			#All of these are xpaths for the connect/messagelock/message button on the profile page, it uses the button classes to identify the stats of the request, 
			#there are 3 states, unconnected, request sent, and connected. It's not possible to know if a request is waiting to be accepted or has been rejected. 
			response = self.driver.page_source.encode('utf-8')
			soup = BeautifulSoup(response, 'html.parser')
			if soup.find_all('div', {'class': 'page_action_left fl_l'})[0].get_text() == "In your friend list":

			elif soup.find_all('div', {'class': 'page_action_left fl_l'})[0].get_text() == "Request sent":
				return "Pending"
			elif soup.find_all('div', {'class': 'page_action_left fl_l'})[0].get_text() == "Following":
				return "Following"
			elif soup.find_all('div', {'class': 'page_action_left fl_l'})[0].get_text() == "Add to Friends":
				print("This Vkontakte profile has not been connected to yet, are you running this in the correct order?")
				return "NotAdded"
			else:
				#This should never be reached, if it is it means the Vkontakte profile page code has changed. 
				print("Error Identifying Connection Request Status for:" + vkontakteprofile)
				print("This could be due to a code change in Vkontakte, please make an issue on the github page.")
				return "Unknown"
		except: 
			traceback.print_exc()
			return "Error"
		'''

	def generateMarkovMessageForVkontakteProfile(self,vkontakteprofile,markovlength,username,password):
		self.driver.get(vkontakteprofile)
		sleep(3)

		if "login" in self.driver.current_url: 
			self.doLogin(username,password)
			self.driver.get(url)
			sleep(3)
			if "login" in self.driver.current_url: 
				print("Vkontakte Timeout Error, session has expired and attempts to reestablish have failed")
			else:
				print("New Vkontakte Session created, resuming activity")
		# This is rough code, not sure if len=0 will return correctly, or if it will crash?
		try:
			# Code here to fill array of timeline post strings
			# Code to scroll down the page, either to bottom or 50 times height of screen
			SCROLL_PAUSE_TIME = 1
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

			#print("DEBUG TEST: Markov Vkontakte Creation33")
			timeline_text = [] # create empty array to hold timeline post strings for processing

			# Code to extract all posts, this pulls out all posts on timeline
			#self.driver.find_elements_by_xpath("//div[@class='_5pcb _4b0l _2q8l']").click()
			# Extract page source from selenium, then use beautifulsoup to extract data
			searchresponse = self.driver.page_source.encode('utf-8')
			soupParser = BeautifulSoup(searchresponse, 'html.parser')
			# scrape out all posts from the source code
			for postelement in soupParser.find_all('div', {'class': 'wall_post_text'}):
				try: # Try to pull out all of the user written posts with their paragraphs
					# Pull out 3rd href element, this is the posters name on a post
					postcontent = postelement.get_text(" ")
					timeline_text.append(postcontent)
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
				processed_post = post.replace("hashtag#","#")
				processed_timeline_text.append(processed_post)
			# Load markov models with processed timeline posts to create a message
			try:
				text_model = markovify.text.NewlineText("\n".join(processed_timeline_text))
				markovmessage = text_model.make_short_sentence(markovlength)
				#print(markovmessage)
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

