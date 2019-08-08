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




class Linkedinphisher(object):

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

		self.driver.get("https://www.linkedin.com/uas/login")
		self.driver.execute_script('localStorage.clear();')

		#agent = self.driver.execute_script("return navigator.userAgent")
		#print("User Agent: " + agent)
		
		if(self.driver.title.encode('ascii','replace').startswith(bytes("LinkedIn Login", 'utf-8'))):
			print("\n[+] LinkedIn Login Page loaded successfully [+]")
			try:
				lnkUsername = self.driver.find_element_by_id("session_key-login")
			except:
				try:
					lnkUsername = self.driver.find_element_by_id("username")
				except:
					print("LinkedIn Login Page username field seems to have changed, please make an issue on: https://github.com/Greenwolf/social_attacker")
			lnkUsername.send_keys(username)
			try:
				lnkPassword = self.driver.find_element_by_id("session_password-login")
			except:
				try:
					lnkPassword = self.driver.find_element_by_id("password")
				except:
					print("LinkedIn Login Page password field seems to have changed, please make an issue on: https://github.com/Greenwolf/social_attacker")
			lnkPassword.send_keys(password)
			try:
				self.driver.find_element_by_id("btn-primary").click()
			except:
				try:
					self.driver.find_element_by_class_name("btn__primary--large").click()
				except:
					print("LinkedIn Login Page login button seems to have changed, please make an issue on: https://github.com/Greenwolf/social_attacker")
			sleep(5)
			if(self.driver.title.encode('utf8','replace') == "Sign In to LinkedIn"):
				print("[-] LinkedIn Login Failed [-]\n")
			else:
				print("[+] LinkedIn Login Success [+]\n")
		else:
			print("LinkedIn Login Page title field seems to have changed, please make an issue on: https://github.com/Greenwolf/social_attacker")

	def addLinkedinProfile(self,linkedinprofile,username,password):
		self.driver.get(linkedinprofile)
		#print("DEBUG: after navigate")
		sleep(3)
		if "login" in self.driver.current_url: 
			self.doLogin(username,password)
			self.driver.get(url)
			sleep(3)
			if "login" in self.driver.current_url: 
				print("LinkedIn Timeout Error, session has expired and attempts to reestablish have failed")
			else:
				print("New Linkedin Session created, resuming activity")
		try:
			#print("DEBUG: Clicking Add")

			#Check if already connected to target
			if len(self.driver.find_elements_by_xpath("//button[@class='pv-s-profile-actions pv-s-profile-actions--message ml2 artdeco-button artdeco-button--2 artdeco-button--primary ember-view']")) == 1: # Target Accepted add request
				print("Already connected to: %s" % (linkedinprofile))
			else:
				#Locate connection button in page, click it
				connect_button = self.driver.find_element_by_class_name("pv-s-profile-actions--connect")
				connect_button.click()

				sleep(3)

				sendnow_button = self.driver.find_element_by_class_name("ml1")
				sendnow_button.click()

				#print("DEBUG: After friend request")
				sleep(3)
		except:
			print("Error Adding Friend: %s" % (linkedinprofile))
			traceback.print_exc()


	def checkLinkedinProfile(self,linkedinprofile,username,password):
		self.driver.get(linkedinprofile)
		sleep(3)
		if "login" in self.driver.current_url: 
			self.doLogin(username,password)
			self.driver.get(url)
			sleep(3)
			if "login" in self.driver.current_url: 
				print("LinkedIn Timeout Error, session has expired and attempts to reestablish have failed")
			else:
				print("New Linkedin Session created, resuming activity")
		try:
			#All of these are xpaths for the connect/messagelock/message button on the profile page, it uses the button classes to identify the stats of the request, 
			#there are 3 states, unconnected, request sent, and connected. It's not possible to know if a request is waiting to be accepted or has been rejected. 
			if len(self.driver.find_elements_by_xpath("//button[@class='pv-s-profile-actions pv-s-profile-actions--message ml2 artdeco-button artdeco-button--2 artdeco-button--primary ember-view']")) == 1: # Target Accepted add request
				return "Accepted"
			elif len(self.driver.find_elements_by_xpath("//button[@class='pv-s-profile-actions pv-s-profile-actions--send-in-mail ml2 artdeco-button artdeco-button--2 artdeco-button--primary ember-view']")) == 1:
				return "Pending or Ignored"
			elif len(self.driver.find_elements_by_xpath("//button[@class='pv-s-profile-actions pv-s-profile-actions--connect ml2 artdeco-button artdeco-button--2 artdeco-button--primary ember-view']")) == 1: # Target has been been added yet, so theres 3 add buttons o page
				print("This Linkedin profile has not been connected to yet, are you running this in the correct order?")
				return "NotAdded"
			else:
				#This should never be reached, if it is it means the LinkedIn profile page code has changed. 
				print("Error Identifying Connection Request Status for:" + linkedinprofile)
				print("This could be due to a code change in LinkedIn, please make an issue on the github page.")
				return "Unknown"
		except: 
			traceback.print_exc()
			return "Error"

	def checkThenPhishLinkedinProfile(self,linkedinprofile,message,username,password):
		self.driver.get(linkedinprofile)
		sleep(3)
		if "login" in self.driver.current_url: 
			self.doLogin(username,password)
			self.driver.get(url)
			sleep(3)
			if "login" in self.driver.current_url: 
				print("LinkedIn Timeout Error, session has expired and attempts to reestablish have failed")
			else:
				print("New Linkedin Session created, resuming activity")
		try:
			#All of these are xpaths for the connect/messagelock/message button on the profile page, it uses the button classes to identify the stats of the request, 
			#there are 3 states, unconnected, request sent, and connected. It's not possible to know if a request is waiting to be accepted or has been rejected. 
			if len(self.driver.find_elements_by_xpath("//button[@class='pv-s-profile-actions pv-s-profile-actions--message ml2 artdeco-button artdeco-button--2 artdeco-button--primary ember-view']")) == 1: # Target Accepted add request
				try:
					#self.driver.find_elements_by_xpath("//div[@class='_42ft _4jy0 _4jy4 _517h _51sy']")[0].click()
					message_button = self.driver.find_element_by_xpath("//button[@class='pv-s-profile-actions pv-s-profile-actions--message ml2 artdeco-button artdeco-button--2 artdeco-button--primary ember-view']")
					message_button.click()
					sleep(5)
					#This should type message in the box
					#print("DEBUG: Before message box click")
					messaging_box = self.driver.find_element_by_xpath("//div[@class='msg-form__contenteditable t-14 t-black--light t-normal flex-grow-1']")
					messaging_box.send_keys(message)
					sleep(2)
					#This should click the send button
					send_button = self.driver.find_element_by_xpath("//button[@class='msg-form__send-button artdeco-button artdeco-button--1']")
					send_button.click()
					sleep(2)
					#This should close the message box
					close_box = self.driver.find_element_by_xpath("//button[@class='msg-overlay-bubble-header__control js-msg-close artdeco-button artdeco-button--circle artdeco-button--inverse artdeco-button--1 artdeco-button--tertiary ember-view']")
					close_box.click()
					return "Sent"
				except:
					traceback.print_exc()
					print("Connection has accepted, but message sending failed, possible code issue")
					return "Error"
			elif len(self.driver.find_elements_by_xpath("//button[@class='pv-s-profile-actions pv-s-profile-actions--send-in-mail ml2 artdeco-button artdeco-button--2 artdeco-button--primary ember-view']")) == 1:
				return "Pending or Ignored"
			elif len(self.driver.find_elements_by_xpath("//button[@class='pv-s-profile-actions pv-s-profile-actions--connect ml2 artdeco-button artdeco-button--2 artdeco-button--primary ember-view']")) == 1: # Target has been been added yet, so theres 3 add buttons o page
				print("This Linkedin profile has not been connected to yet, are you running this in the correct order?")
				return "NotAdded"
			else:
				#This should never be reached, if it is it means the LinkedIn profile page code has changed. 
				print("Error Identifying Connection Request Status for:" + linkedinprofile)
				print("This could be due to a code change in LinkedIn, please make an issue on the github page.")
				return "Unknown"
		except: 
			traceback.print_exc()
			return "Error"

	def generateMarkovMessageForLinkedinProfile(self,linkedinprofile,markovlength,username,password):
		recent_activity = linkedinprofile + "detail/recent-activity/"
		self.driver.get(recent_activity)
		sleep(3)

		if "login" in self.driver.current_url: 
			self.doLogin(username,password)
			self.driver.get(url)
			sleep(3)
			if "login" in self.driver.current_url: 
				print("LinkedIn Timeout Error, session has expired and attempts to reestablish have failed")
			else:
				print("New Linkedin Session created, resuming activity")
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

			#print("DEBUG TEST: Markov Linkedin Creation33")
			timeline_text = [] # create empty array to hold timeline post strings for processing

			# Code to extract all posts, this pulls out all posts on timeline
			#self.driver.find_elements_by_xpath("//div[@class='_5pcb _4b0l _2q8l']").click()
			# Extract page source from selenium, then use beautifulsoup to extract data
			searchresponse = self.driver.page_source.encode('utf-8')
			soupParser = BeautifulSoup(searchresponse, 'html.parser')
			# scrape out all posts from the source code
			for postelement in soupParser.find_all('div', {'class': 'feed-shared-update-v2__description'}):
				try: # Try to pull out all of the user written posts with their paragraphs
					# Pull out 3rd href element, this is the posters name on a post

					postcontent = postelement.find_all('span')[0].get_text()
					for paragraph in postcontent.split("\n"):
						if paragraph != '':
							timeline_text.append(paragraph)
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
				processed_post = post.replace("hashtag#","#")
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

	def prepareLinkedinProfile(self,company_url,username,password):
		self.driver.get(company_url)
		#print("DEBUG: after navigate")
		sleep(3)
		if "login" in self.driver.current_url: 
			self.doLogin(username,password)
			self.driver.get(url)
			sleep(3)
			if "login" in self.driver.current_url: 
				print("LinkedIn Timeout Error, session has expired and attempts to reestablish have failed")
			else:
				print("New Linkedin Session created, resuming activity")
		connection_list = []
		try:
			#navigate 
			show_all_employees_link = self.driver.find_elements_by_xpath("//a[@class='link-without-visited-state inline-block ember-view']")[0].get_attribute("href")
			self.driver.get(show_all_employees_link)
			sleep(5)
		except:
			print("LinkedIn See All Employees field seems to have changed, please make an issue on: https://github.com/Greenwolf/social_attacker")
			traceback.print_exc()

		try:
			for number in range(1,100,1):
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
					if (new_height == last_height or breakoutcount > 5):
					    break
					last_height = new_height
					breakoutcount = breakoutcount + 1
				sleep(1)

				profiles = self.driver.find_elements_by_xpath("//div[@class='search-result__wrapper']")
				for profile in profiles:
					try:
						#info = profile.find_element_by_xpath("//div[@class='search-result__info pt3 pb4 ph0']")
						#print(profile.get_attribute('innerHTML'))
						full_name = profile.find_element_by_class_name("actor-name-with-distance").text.split("\n")[0]
						#print(full_name)
						profile_link = profile.find_elements_by_class_name("search-result__result-link")[0].get_attribute("href")
						#print(profile_link)
						connect_button = profile.find_element_by_class_name("search-result__action-button")
						connect_button.click()
						status = "Connection Request Sent"
						sleep(2)
						send_button = self.driver.find_elements_by_xpath("//button[@class='artdeco-button artdeco-button--3 ml1']")[0]
						send_button.click()
						sleep(2)
						print("Connecting to: " + full_name + " : " + profile_link)
						connection_list.append([full_name,profile_link,status])
					except:
						#If error move to next user 
						continue
				#Try clicking next button, if it doesnt work assume end of employees and return
				try:
					next_button = self.driver.find_element_by_xpath("//button[@class='artdeco-pagination__button artdeco-pagination__button--next artdeco-button artdeco-button--muted artdeco-button--icon-right artdeco-button--1 artdeco-button--tertiary ember-view']")
					next_button.click()
					sleep(2)	
				except:
					return connection_list
		except:
			traceback.print_exc()
			pass

		return connection_list

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

