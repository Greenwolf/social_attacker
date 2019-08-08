from modules import facebookphisher
from modules import linkedinphisher
from modules import twitterphisher
from modules import vkontaktephisher
import pandas
import numpy
import argparse
import time
import sys
import random
import mmap
import re
import traceback
from datetime import datetime
from time import sleep

# Markov Documentation: 
# Facebook: Pulls out user written timeline posts, news article headlines and link descriptions 
# LinkedIn: Pulls out recent activity thats been posted or liked
# Twitter: Pulls out all tweets
# VKontakte: Pulls out all timeline posts
#

# Usernames & Passwords for the accounts you wish to phish with

global facebook_username
global facebook_password
facebook_username = ""
facebook_password = ""
global linkedin_username
global linkedin_password
linkedin_username = ""
linkedin_password = ""
global twitter_username
global twitter_password
twitter_username = ""
twitter_password = ""
global vkontakte_username
global vkontakte_password
vkontakte_username = "" # Can be mobile or email
vkontakte_password = ""

#Generate initial 5 character hex tracking code
global tracking_id
tracking_id = ''.join(random.choice('0123456789ABCDEF') for i in range(5))

startTime = datetime.now()

# person class to hold data
class Person(object):
    first_name = ""
    last_name = ""
    full_name = ""

    #profile link
    facebook = ""
    # connected request status: connected/rejected/pending/error/unknown etc
    facebookstatus = ""
    # Phish status: sent/error
    facebookphish = ""
    # 5 character hex tracking code
    facebooktrackingcode = ""
    # markov message that was generated
    facebookmarkovmessage = ""
    # final phishing message sent: default message or markov + phishing link
    facebookfinalphishingmessage = ""
    # log check: did user click?
    facebookclicked = ""
    # log check: what IP did user click from
    facebookclickedip = ""
    # log check: what time did user click
    facebookclickedtime = ""
    # log check: what was user agent from click
    facebookclickeduseragent = ""

    linkedin = ""
    linkedinstatus = ""
    linkedinphish = ""
    linkedintrackingcode = ""
    linkedinmarkovmessage = ""
    linkedinfinalphishingmessage = ""
    linkedinclicked = ""
    linkedinclickedip = ""
    linkedinclickedtime = ""
    linkedinclickeduseragent = ""

    twitter = ""
    twitterstatus = ""
    twitterphish = ""
    twittertrackingcode = ""
    twittermarkovmessage = ""
    twitterfinalphishingmessage = ""
    twitterclicked = ""
    twitterclickedip = ""
    twitterclickedtime = ""
    twitterclickeduseragent = ""

    vkontakte = ""
    vkontaktestatus = ""
    vkontaktephish = ""
    vkontaktetrackingcode = ""
    vkontaktemarkovmessage = ""
    vkontaktefinalphishingmessage = ""
    vkontakteclicked = ""
    vkontakteclickedip = ""
    vkontakteclickedtime = ""
    vkontakteclickeduseragent = ""

    def __init__(self, first_name, last_name, full_name):
        self.first_name = first_name
        self.last_name = last_name
        self.full_name = full_name

def prepare_linkedin(company_url):
    LinkedinphisherObject = linkedinphisher.Linkedinphisher(showbrowser)
    LinkedinphisherObject.doLogin(linkedin_username,linkedin_password)
    connection_list = LinkedinphisherObject.prepareLinkedinProfile(company_url,linkedin_username,linkedin_password)
    try:
        LinkedinphisherObject.kill()
    except:
        print("Error Killing LinkedIn Selenium instance")
    return connection_list

# TODO Code to friend all Facebook targets
def add_facebook(peoplelist):
    FacebookphisherObject = facebookphisher.Facebookphisher(showbrowser)
    FacebookphisherObject.doLogin(facebook_username,facebook_password)

    count=1
    ammount=len(peoplelist)                      
    for person in peoplelist:
        #Testcode to mimic a session timeout
        #if count == 3: print "triggered delete"
        #    FacebookphisherObject.testdeletecookies()
        if person.facebook:
            if args.vv == True:
                print("Adding Facebook Friend %i/%i : %s" % (count,ammount,person.full_name))
            else:
                sys.stdout.write("\rAdding Facebook Friend %i/%i : %s                                " % (count,ammount,person.full_name))
                sys.stdout.flush()
            count = count + 1    
            try:
                FacebookphisherObject.addFacebookProfile(person.facebook,facebook_username,facebook_password)
            except:
                continue
        else:
            continue
    try:
        FacebookphisherObject.kill()
    except:
        print("Error Killing Facebook Selenium instance")

# TODO Code to connect to all LinkedIn targets
def add_linkedin(peoplelist):
    LinkedinphisherObject = linkedinphisher.Linkedinphisher(showbrowser)
    LinkedinphisherObject.doLogin(linkedin_username,linkedin_password)

    count=1
    ammount=len(peoplelist)                      
    for person in peoplelist:
        #Testcode to mimic a session timeout
        #if count == 3: print "triggered delete"
        #    LinkedinphisherObject.testdeletecookies()
        if person.linkedin:
            if args.vv == True:
                print("Adding LinkedIn Connection %i/%i : %s" % (count,ammount,person.full_name))
            else:
                sys.stdout.write("\rAdding LinkedIn Connection %i/%i : %s                                " % (count,ammount,person.full_name))
                sys.stdout.flush()
            count = count + 1            
            try:
                LinkedinphisherObject.addLinkedinProfile(person.linkedin,linkedin_username,linkedin_password)
            except:
                continue
        else:
            continue
    try:
        LinkedinphisherObject.kill()
    except:
        print("Error Killing LinkedIn Selenium instance")

#Follow on twitter
def add_twitter(peoplelist):
    TwitterphisherObject = twitterphisher.Twitterphisher(showbrowser)
    TwitterphisherObject.doLogin(twitter_username,twitter_password)

    count=1
    ammount=len(peoplelist)                      
    for person in peoplelist:
        
        #Testcode to mimic a session timeout
        #if count == 3: print "triggered delete"
        #    TwitterphisherObject.testdeletecookies()
        if person.twitter:
            if args.vv == True:
                print("Following Twitter target %i/%i : %s" % (count,ammount,person.full_name))
            else:
                sys.stdout.write("\rFollowing Twitter target %i/%i : %s                                " % (count,ammount,person.full_name))
                sys.stdout.flush()
            count = count + 1    
            try:
                TwitterphisherObject.addTwitterProfile(person.twitter,twitter_username,twitter_password)
            except:
                continue
        else:
            continue
    try:
        TwitterphisherObject.kill()
    except:
        print("Error Killing Twitter Selenium instance")

def add_vkontakte(peoplelist):
    VkontaktephisherObject = vkontaktephisher.Vkontaktephisher(showbrowser)
    VkontaktephisherObject.doLogin(vkontakte_username,vkontakte_password)

    count=1
    ammount=len(peoplelist)                      
    for person in peoplelist:
        #Testcode to mimic a session timeout
        #if count == 3: print "triggered delete"
        #    VkontaktephisherObject.testdeletecookies()
        if person.vkontakte:
            if args.vv == True:
                print("Adding Vkontakte Connection %i/%i : %s" % (count,ammount,person.full_name))
            else:
                sys.stdout.write("\rAdding Vkontakte Connection %i/%i : %s                                " % (count,ammount,person.full_name))
                sys.stdout.flush()
            count = count + 1            
            try:
                VkontaktephisherObject.addVkontakteProfile(person.vkontakte,vkontakte_username,vkontakte_password)
            except:
                continue
        else:
            continue
    try:
        VkontaktephisherObject.kill()
    except:
        print("Error Killing VKontakte Selenium instance")

# [MORE_SOCIAL_MEDIA_SITES_TAG]

# TODO Code to check if Facebook Target has accepted friend request
def check_facebook(peoplelist):
    FacebookphisherObject = facebookphisher.Facebookphisher(showbrowser)
    FacebookphisherObject.doLogin(facebook_username,facebook_password)

    count=1
    ammount=len(peoplelist)
    for person in peoplelist:
       
        #Testcode to mimic a session timeout
        #if count == 3: print "triggered delete"
        #    FacebookphisherObject.testdeletecookies()
        if person.facebook:
            if args.vv == True:
                print("Checking Facebook for Friend Request Status %i/%i : %s" % (count,ammount,person.full_name))
            else:
                sys.stdout.write("\rChecking Facebook for Friend Request Status %i/%i : %s                                " % (count,ammount,person.full_name))
                sys.stdout.flush()
            count = count + 1     
            try:
                person.facebookstatus = FacebookphisherObject.checkFacebookProfile(person.facebook,facebook_username,facebook_password)
                if args.vv == True:
                    print(person.facebook + " : " + person.facebookstatus)
                sleep(3)
            except:
                continue
        else:
            continue
    try:
        FacebookphisherObject.kill()
    except:
        print("Error Killing Facebook Selenium instance")
    return peoplelist
    # If connected, set person.facebookstatus to Yes
    # Output connected targets to csv + console

# TODO Code to check if LinkedIn Target has accepted connection request
def check_linkedin(peoplelist):
    LinkedinphisherObject = linkedinphisher.Linkedinphisher(showbrowser)
    LinkedinphisherObject.doLogin(linkedin_username,linkedin_password)

    count=1
    ammount=len(peoplelist)
    for person in peoplelist:
          
        #Testcode to mimic a session timeout
        #if count == 3: print "triggered delete"
        #    LinkedinphisherObject.testdeletecookies()
        if person.linkedin:
            if args.vv == True:
                print("Checking LinkedIn for Connection Status %i/%i : %s" % (count,ammount,person.full_name))
            else:
                sys.stdout.write("\rChecking LinkedIn for Connection Status %i/%i : %s                                " % (count,ammount,person.full_name))
                sys.stdout.flush()
            count = count + 1  
            try:
                person.linkedinstatus = LinkedinphisherObject.checkLinkedinProfile(person.linkedin,linkedin_username,linkedin_password)
                if args.vv == True:
                    print(person.linkedin + " : " + person.linkedinstatus)
                sleep(3)
            except:
                continue
        else:
            continue
    try:
        LinkedinphisherObject.kill()
    except:
        print("Error Killing LinkedIn Selenium instance")
    return peoplelist
    # If connected, set person.linkedinstatus to Yes
    # Output connected targets to csv + console

def check_twitter(peoplelist):
    TwitterphisherObject = twitterphisher.Twitterphisher(showbrowser)
    TwitterphisherObject.doLogin(twitter_username,twitter_password)

    count=1
    ammount=len(peoplelist)
    for person in peoplelist:
      
        #Testcode to mimic a session timeout
        #if count == 3: print "triggered delete"
        #    TwitterphisherObject.testdeletecookies()
        if person.twitter:
            if args.vv == True:
                print("Checking Twitter for Following Status %i/%i : %s" % (count,ammount,person.full_name))
            else:
                sys.stdout.write("\rChecking Twitter for Following Status %i/%i : %s                                " % (count,ammount,person.full_name))
                sys.stdout.flush()
            count = count + 1      
            try:
                person.twitterstatus = TwitterphisherObject.checkTwitterProfile(person.twitter,twitter_username,twitter_password)
                if args.vv == True:
                    print(person.twitter + " : " + person.twitterstatus)
                sleep(3)
            except:
                continue
        else:
            continue
    try:
        TwitterphisherObject.kill()
    except:
        print("Error Killing Twitter Selenium instance")
    return peoplelist
    # If connected, set person.linkedinstatus to Yes
    # Output connected targets to csv + console

# TODO Code to check if LinkedIn Target has accepted connection request
def check_vkontakte(peoplelist):
    VkontaktephisherObject = vkontaktephisher.Vkontaktephisher(showbrowser)
    VkontaktephisherObject.doLogin(vkontakte_username,vkontakte_password)

    count=1
    ammount=len(peoplelist)
    for person in peoplelist:
        
        #Testcode to mimic a session timeout
        #if count == 3: print "triggered delete"
        #    VkontaktephisherObject.testdeletecookies()
        if person.vkontakte:
            if args.vv == True:
                print("Checking Vkontakte for Connection Status %i/%i : %s" % (count,ammount,person.full_name))
            else:
                sys.stdout.write("\rChecking Vkontakte for Connection Status %i/%i : %s                                " % (count,ammount,person.full_name))
                sys.stdout.flush()
            count = count + 1    
            try:
                person.vkontaktestatus = VkontaktephisherObject.checkVkontakteProfile(person.vkontakte,vkontakte_username,vkontakte_password)
                if args.vv == True:
                    print(person.vkontakte + " : " + person.vkontaktestatus)
                sleep(3)
            except:
                continue
        else:
            continue
    try:
        VkontaktephisherObject.kill()
    except:
        print("Error Killing VKontakte Selenium instance")
    return peoplelist
    # If connected, set person.vkontaktestatus to Yes
    # Output connected targets to csv + console

# [MORE_SOCIAL_MEDIA_SITES_TAG]

def generate_markov_facebook(peoplelist):
    FacebookphisherObject = facebookphisher.Facebookphisher(showbrowser)
    FacebookphisherObject.doLogin(facebook_username,facebook_password)

    count=1
    ammount=len(peoplelist)

    for person in peoplelist:         
        #Testcode to mimic a session timeout
        #if count == 3: print "triggered delete"
        #    FacebookphisherObject.testdeletecookies()
        if person.facebook:
            if args.vv == True:
                print("Generating Facebook Markov Message Phish %i/%i : %s" % (count,ammount,person.full_name))
            else:
                sys.stdout.write("\rGenerating Facebook Markov Message Phish %i/%i : %s                                " % (count,ammount,person.full_name))
                sys.stdout.flush()
            count = count + 1   
            try:
                if args.markovlength:
                    person.facebookmarkovmessage = FacebookphisherObject.generateMarkovMessageForFacebookProfile(person.facebook,args.markovlength,facebook_username,facebook_password)
                else:
                    person.facebookmarkovmessage = FacebookphisherObject.generateMarkovMessageForFacebookProfile(person.facebook,140,facebook_username,facebook_password)
                sleep(3)
            except:
                continue
        else:
            traceback.print_exc()
            continue
    try:
        FacebookphisherObject.kill()
    except:
        print("Error Killing Facebook Selenium instance")
    return peoplelist

def generate_markov_linkedin(peoplelist):
    LinkedinphisherObject = linkedinphisher.Linkedinphisher(showbrowser)
    LinkedinphisherObject.doLogin(linkedin_username,linkedin_password)

    count=1
    ammount=len(peoplelist)

    for person in peoplelist:
     
        #Testcode to mimic a session timeout
        #if count == 3: print "triggered delete"
        #    LinkedinphisherObject.testdeletecookies()
        if person.linkedin:
            if args.vv == True:
                print("Generating Linkedin Markov Message Phish %i/%i : %s" % (count,ammount,person.full_name))
            else:
                sys.stdout.write("\rGenerating Linkedin Markov Message Phish %i/%i : %s                                " % (count,ammount,person.full_name))
                sys.stdout.flush()
            count = count + 1
            try:
                if args.markovlength:
                    person.linkedinmarkovmessage = LinkedinphisherObject.generateMarkovMessageForLinkedinProfile(person.linkedin,args.markovlength,linkedin_username,linkedin_password)
                else:
                    person.linkedinmarkovmessage = LinkedinphisherObject.generateMarkovMessageForLinkedinProfile(person.linkedin,140,linkedin_username,linkedin_password)
                sleep(3)
            except:
                continue
        else:
            traceback.print_exc()
            continue
    try:
        LinkedinphisherObject.kill()
    except:
        print("Error Killing Linkedin Selenium instance")
    return peoplelist

def generate_markov_twitter(peoplelist):
    #Works by scraping posts in recent activity
    #https://www.twitter.com/in/user-id/detail/recent-activity/
    TwitterphisherObject = twitterphisher.Twitterphisher(showbrowser)
    TwitterphisherObject.doLogin(twitter_username,twitter_password)

    count=1
    ammount=len(peoplelist)

    for person in peoplelist:
        
        #Testcode to mimic a session timeout
        #if count == 3: print "triggered delete"
        #    FacebookphisherObject.testdeletecookies()
        if person.twitter:
            if args.vv == True:
                print("Generating Twitter Markov Message Phish %i/%i : %s" % (count,ammount,person.full_name))
            else:
                sys.stdout.write("\rGenerating Twitter Markov Message Phish %i/%i : %s                                " % (count,ammount,person.full_name))
                sys.stdout.flush()
            count = count + 1    
            try:
                if args.markovlength:
                    person.twittermarkovmessage = TwitterphisherObject.generateMarkovMessageForTwitterProfile(person.twitter,args.markovlength,twitter_username,twitter_password)
                else:
                    person.twittermarkovmessage = TwitterphisherObject.generateMarkovMessageForTwitterProfile(person.twitter,140,twitter_username,twitter_password)
                sleep(3)
            except:
                continue
        else:
            traceback.print_exc()
            continue
    try:
        TwitterphisherObject.kill()
    except:
        print("Error Killing Twitter Selenium instance")
    return peoplelist

def generate_markov_vkontakte(peoplelist):
    #Works by scraping posts in recent activity
    #https://www.vkontakte.com/in/user-id/detail/recent-activity/
    VkontaktephisherObject = vkontaktephisher.Vkontaktephisher(showbrowser)
    VkontaktephisherObject.doLogin(vkontakte_username,vkontakte_password)

    count=1
    ammount=len(peoplelist)

    for person in peoplelist:          
        #Testcode to mimic a session timeout
        #if count == 3: print "triggered delete"
        #    FacebookphisherObject.testdeletecookies()
        if person.vkontakte:
            if args.vv == True:
                print("Generating Vkontakte Markov Message Phish %i/%i : %s" % (count,ammount,person.full_name))
            else:
                sys.stdout.write("\rGenerating Vkontakte Markov Message Phish %i/%i : %s                                " % (count,ammount,person.full_name))
                sys.stdout.flush()
            count = count + 1  
            try:
                if args.markovlength:
                    person.vkontaktemarkovmessage = VkontaktephisherObject.generateMarkovMessageForVkontakteProfile(person.vkontakte,args.markovlength,vkontakte_username,vkontakte_password)
                else:
                    person.vkontaktemarkovmessage = VkontaktephisherObject.generateMarkovMessageForVkontakteProfile(person.vkontakte,140,vkontakte_username,vkontakte_password)
                sleep(3)
            except:
                continue
        else:
            traceback.print_exc()
            continue
    try:
        VkontaktephisherObject.kill()
    except:
        print("Error Killing VKontakte Selenium instance")
    return peoplelist

# [MORE_SOCIAL_MEDIA_SITES_TAG]

# TODO Code to check & phish if Facebook Target has accepted friend request
def checkphish_facebook(peoplelist):
    FacebookphisherObject = facebookphisher.Facebookphisher(showbrowser)
    FacebookphisherObject.doLogin(facebook_username,facebook_password)

    count=1
    ammount=len(peoplelist)

    for person in peoplelist:

        #Testcode to mimic a session timeout
        #if count == 3: print "triggered delete"
        #    FacebookphisherObject.testdeletecookies()

        if person.facebook:
            if args.vv == True:
                print("Sending Facebook Phish %i/%i : %s" % (count,ammount,person.full_name))
            else:
                sys.stdout.write("\rSending Facebook Phish %i/%i : %s                                " % (count,ammount,person.full_name))
                sys.stdout.flush()
            count = count + 1
            try:
                #Set unique tracking id, increment global tracking_id value
                global tracking_id
                person.facebooktrackingcode = tracking_id
                tracking_id = numpy.base_repr((int(tracking_id, 36) + 1), 36).zfill(5)

                # Need to sepparate these out, so that there is another function to generate markov messages 
                if args.markovmessage: # If markov message, check if blank message "Error-MarkovNone" or "Error", if so send message, else send markov message
                    if person.facebookmarkovmessage == "Error-MarkovGeneralCrash" or person.facebookmarkovmessage == "Error-MarkovNoData" or person.facebookmarkovmessage == "Error-MarkovifyCrash":
                        person.facebookfinalphishingmessage = args.message.replace('[TRACKING_ID]',person.facebooktrackingcode).replace('[FULL_NAME]',person.full_name).replace('[LAST_NAME]',person.last_name).replace('[FIRST_NAME]',person.first_name)
                        person.facebookphish = FacebookphisherObject.checkThenPhishFacebookProfile(person.facebook,person.facebookfinalphishingmessage,facebook_username,facebook_password)
                    else:
                        phishingurl = args.markovmessage.replace('[TRACKING_ID]',person.facebooktrackingcode).replace('[FULL_NAME]',person.full_name).replace('[LAST_NAME]',person.last_name).replace('[FIRST_NAME]',person.first_name)
                        # if markov message contains no links, add the end, else replace links with phishing link
                        if "http" not in person.facebookmarkovmessage and "https" not in person.facebookmarkovmessage:
                            person.facebookfinalphishingmessage = person.facebookmarkovmessage + " " + phishingurl
                        else:
                            final_message_array = person.facebookmarkovmessage.split()
                            temp_message = ""
                            for word in final_message_array:
                                if "http" not in word and "https" not in word:
                                    temp_message = temp_message + word + " "
                                else:
                                    temp_message = temp_message + phishingurl + " "
                            person.facebookfinalphishingmessage = temp_message[:-1]
                        person.facebookphish = FacebookphisherObject.checkThenPhishFacebookProfile(person.facebook,person.facebookfinalphishingmessage,facebook_username,facebook_password)
                elif args.message: # If just message, replace variables then send
                    person.facebookfinalphishingmessage = args.message.replace('[TRACKING_ID]',person.facebooktrackingcode).replace('[FULL_NAME]',person.full_name).replace('[LAST_NAME]',person.last_name).replace('[FIRST_NAME]',person.first_name)
                    person.facebookphish = FacebookphisherObject.checkThenPhishFacebookProfile(person.facebook,person.facebookfinalphishingmessage,facebook_username,facebook_password)
                else:
                    print("Error, No Phishing Message Provided")
                    sys.exit(0)
                sleep(3)
            except:
                traceback.print_exc()
                continue
        else:
            continue
    try:
        FacebookphisherObject.kill()
    except:
        print("Error Killing Facebook Selenium instance")
    return peoplelist
    # If connected, send phishing message(-m), or generate custom one with markov chains(-mm)
    # Generate unique tracking codes before phishing
    # Output phished users + profiles + tracking codes to csv + console

# TODO Code to check & phish if LinkedIn Target has accepted connection request
def checkphish_linkedin(peoplelist):
    # If connected, send phishing message(-m), or generate custom one with markov chains(-mm)
    # Generate unique tracking codes before phishing
    # Output phished users + profiles + tracking codes to csv + console
    LinkedinphisherObject = linkedinphisher.Linkedinphisher(showbrowser)
    LinkedinphisherObject.doLogin(linkedin_username,linkedin_password)

    count=1
    ammount=len(peoplelist)

    for person in peoplelist:

        #Testcode to mimic a session timeout
        #if count == 3: print "triggered delete"
        #    LinkedinphisherObject.testdeletecookies()

        if person.linkedin:
            if args.vv == True:
                print("Sending LinkedIn Phish %i/%i : %s" % (count,ammount,person.full_name))
            else:
                sys.stdout.write("\rSending LinkedIn Phish %i/%i : %s                                " % (count,ammount,person.full_name))
                sys.stdout.flush()
            count = count + 1
            try:
                #Set unique tracking id, increment global tracking_id value
                global tracking_id
                person.linkedintrackingcode = tracking_id
                tracking_id = numpy.base_repr((int(tracking_id, 36) + 1), 36).zfill(5)

                # Need to sepparate these out, so that there is another function to generate markov messages 
                if args.markovmessage: # If markov message, check if blank message "Error-MarkovNone" or "Error", if so send message, else send markov message
                    if person.linkedinmarkovmessage == "Error-MarkovGeneralCrash" or person.linkedinmarkovmessage == "Error-MarkovNoData" or person.linkedinmarkovmessage == "Error-MarkovifyCrash":
                        person.linkedinfinalphishingmessage = args.message.replace('[TRACKING_ID]',person.linkedintrackingcode).replace('[FULL_NAME]',person.full_name).replace('[LAST_NAME]',person.last_name).replace('[FIRST_NAME]',person.first_name)
                        person.linkedinphish = LinkedinphisherObject.checkThenPhishLinkedinProfile(person.linkedin,person.linkedinfinalphishingmessage,linkedin_username,linkedin_password)
                    else:
                        phishingurl = args.markovmessage.replace('[TRACKING_ID]',person.linkedintrackingcode).replace('[FULL_NAME]',person.full_name).replace('[LAST_NAME]',person.last_name).replace('[FIRST_NAME]',person.first_name)
                        # if markov message contains no links, add the end, else replace links with phishing link
                        if "http" not in person.linkedinmarkovmessage and "https" not in person.linkedinmarkovmessage:
                            person.linkedinfinalphishingmessage = person.linkedinmarkovmessage + " " + phishingurl
                        else:
                            final_message_array = person.linkedinmarkovmessage.split()
                            temp_message = ""
                            for word in final_message_array:
                                if "http" not in word and "https" not in word:
                                    temp_message = temp_message + word + " "
                                else:
                                    temp_message = temp_message + phishingurl + " "
                            person.linkedinfinalphishingmessage = temp_message[:-1]
                        person.linkedinphish = LinkedinphisherObject.checkThenPhishLinkedinProfile(person.linkedin,person.linkedinfinalphishingmessage,linkedin_username,linkedin_password)
                elif args.message: # If just message, replace variables then send
                    person.linkedinfinalphishingmessage = args.message.replace('[TRACKING_ID]',person.linkedintrackingcode).replace('[FULL_NAME]',person.full_name).replace('[LAST_NAME]',person.last_name).replace('[FIRST_NAME]',person.first_name)
                    person.linkedinphish = LinkedinphisherObject.checkThenPhishLinkedinProfile(person.linkedin,person.linkedinfinalphishingmessage,linkedin_username,linkedin_password)
                else:
                    print("Error, No Phishing Message Provided")
                    sys.exit(0)
                sleep(3)
            except:
                traceback.print_exc()
                continue
        else:
            continue
    try:
        LinkedinphisherObject.kill()
    except:
        print("Error Killing LinkedIn Selenium instance")
    return peoplelist
    # If connected, send phishing message(-m), or generate custom one with markov chains(-mm)
    # Generate unique tracking codes before phishing
    # Output phished users + profiles + tracking codes to csv + console

# TODO Code to check & phish if LinkedIn Target has accepted connection request
def checkphish_twitter(peoplelist):
    # If connected, send phishing message(-m), or generate custom one with markov chains(-mm)
    # Generate unique tracking codes before phishing
    # Output phished users + profiles + tracking codes to csv + console
    TwitterphisherObject = twitterphisher.Twitterphisher(showbrowser)
    TwitterphisherObject.doLogin(twitter_username,twitter_password)

    count=1
    ammount=len(peoplelist)

    for person in peoplelist:

        #Testcode to mimic a session timeout
        #if count == 3: print "triggered delete"
        #    TwitterphisherObject.testdeletecookies()

        if person.twitter:
            if args.vv == True:
                print("Sending Twitter Phish %i/%i : %s" % (count,ammount,person.full_name))
            else:
                sys.stdout.write("\rSending Twitter Phish %i/%i : %s                                " % (count,ammount,person.full_name))
                sys.stdout.flush()
            count = count + 1
            try:
                #Set unique tracking id, increment global tracking_id value
                global tracking_id
                person.twittertrackingcode = tracking_id
                tracking_id = numpy.base_repr((int(tracking_id, 36) + 1), 36).zfill(5)

                # Need to sepparate these out, so that there is another function to generate markov messages 
                if args.markovmessage: # If markov message, check if blank message "Error-MarkovNone" or "Error", if so send message, else send markov message
                    if person.twittermarkovmessage == "Error-MarkovGeneralCrash" or person.twittermarkovmessage == "Error-MarkovNoData" or person.twittermarkovmessage == "Error-MarkovifyCrash":
                        person.twitterfinalphishingmessage = args.message.replace('[TRACKING_ID]',person.twittertrackingcode).replace('[FULL_NAME]',person.full_name).replace('[LAST_NAME]',person.last_name).replace('[FIRST_NAME]',person.first_name)
                        person.twitterphish = TwitterphisherObject.checkThenPhishTwitterProfile(person.twitter,person.twitterfinalphishingmessage,twitter_username,twitter_password)
                    else:
                        phishingurl = args.markovmessage.replace('[TRACKING_ID]',person.twittertrackingcode).replace('[FULL_NAME]',person.full_name).replace('[LAST_NAME]',person.last_name).replace('[FIRST_NAME]',person.first_name)
                        # if markov message contains no links, add the end, else replace links with phishing link
                        if "http" not in person.twittermarkovmessage and "https" not in person.twittermarkovmessage:
                            person.twitterfinalphishingmessage = person.twittermarkovmessage + " " + phishingurl
                        else:
                            final_message_array = person.twittermarkovmessage.split()
                            temp_message = ""
                            for word in final_message_array:
                                if "http" not in word and "https" not in word:
                                    temp_message = temp_message + word + " "
                                else:
                                    temp_message = temp_message + phishingurl + " "
                            person.twitterfinalphishingmessage = temp_message[:-1]
                        person.twitterphish = TwitterphisherObject.checkThenPhishTwitterProfile(person.twitter,person.twitterfinalphishingmessage,twitter_username,twitter_password)
                elif args.message: # If just message, replace variables then send
                    person.twitterfinalphishingmessage = args.message.replace('[TRACKING_ID]',person.twittertrackingcode).replace('[FULL_NAME]',person.full_name).replace('[LAST_NAME]',person.last_name).replace('[FIRST_NAME]',person.first_name)
                    person.twitterphish = TwitterphisherObject.checkThenPhishTwitterProfile(person.twitter,person.twitterfinalphishingmessage,twitter_username,twitter_password)
                else:
                    print("Error, No Phishing Message Provided")
                    sys.exit(0)
                sleep(3)
            except:
                traceback.print_exc()
                continue
        else:
            continue
    try:
        TwitterphisherObject.kill()
    except:
        print("Error Killing Twitter Selenium instance")
    return peoplelist
    # If connected, send phishing message(-m), or generate custom one with markov chains(-mm)
    # Generate unique tracking codes before phishing
    # Output phished users + profiles + tracking codes to csv + console

# TODO Code to check & phish if LinkedIn Target has accepted connection request
def checkphish_vkontakte(peoplelist):
    # If connected, send phishing message(-m), or generate custom one with markov chains(-mm)
    # Generate unique tracking codes before phishing
    # Output phished users + profiles + tracking codes to csv + console
    VkontaktephisherObject = vkontaktephisher.Vkontaktephisher(showbrowser)
    VkontaktephisherObject.doLogin(vkontakte_username,vkontakte_password)

    count=1
    ammount=len(peoplelist)

    for person in peoplelist:

        #Testcode to mimic a session timeout
        #if count == 3: print "triggered delete"
        #    VkontaktephisherObject.testdeletecookies()

        if person.vkontakte:
            if args.vv == True:
                print("Sending Vkontakte Phish %i/%i : %s" % (count,ammount,person.full_name))
            else:
                sys.stdout.write("\rSending Vkontakte Phish %i/%i : %s                                " % (count,ammount,person.full_name))
                sys.stdout.flush()
            count = count + 1
            try:
                #Set unique tracking id, increment global tracking_id value
                global tracking_id
                person.vkontaktetrackingcode = tracking_id
                tracking_id = numpy.base_repr((int(tracking_id, 36) + 1), 36).zfill(5)

                # Need to sepparate these out, so that there is another function to generate markov messages 
                if args.markovmessage: # If markov message, check if blank message "Error-MarkovNone" or "Error", if so send message, else send markov message
                    if person.vkontaktemarkovmessage == "Error-MarkovGeneralCrash" or person.vkontaktemarkovmessage == "Error-MarkovNoData" or person.vkontaktemarkovmessage == "Error-MarkovifyCrash":
                        person.vkontaktefinalphishingmessage = args.message.replace('[TRACKING_ID]',person.vkontaktetrackingcode).replace('[FULL_NAME]',person.full_name).replace('[LAST_NAME]',person.last_name).replace('[FIRST_NAME]',person.first_name)
                        person.vkontaktephish = VkontaktephisherObject.checkThenPhishVkontakteProfile(person.vkontakte,person.vkontaktefinalphishingmessage,vkontakte_username,vkontakte_password)
                    else:
                        phishingurl = args.markovmessage.replace('[TRACKING_ID]',person.vkontaktetrackingcode).replace('[FULL_NAME]',person.full_name).replace('[LAST_NAME]',person.last_name).replace('[FIRST_NAME]',person.first_name)
                        # if markov message contains no links, add the end, else replace links with phishing link
                        if "http" not in person.vkontaktemarkovmessage and "https" not in person.vkontaktemarkovmessage:
                            person.vkontaktefinalphishingmessage = person.vkontaktemarkovmessage + " " + phishingurl
                        else:
                            final_message_array = person.vkontaktemarkovmessage.split()
                            temp_message = ""
                            #If word in sentance is a link, replace it with phishing link
                            for word in final_message_array:
                                if "http" not in word and "https" not in word:
                                    temp_message = temp_message + word + " "
                                else:
                                    temp_message = temp_message + phishingurl + " "
                            person.vkontaktefinalphishingmessage = temp_message[:-1]
                        person.vkontaktephish = VkontaktephisherObject.checkThenPhishVkontakteProfile(person.vkontakte,person.vkontaktefinalphishingmessage,vkontakte_username,vkontakte_password)
                elif args.message: # If just message, replace variables then send
                    person.vkontaktefinalphishingmessage = args.message.replace('[TRACKING_ID]',person.vkontaktetrackingcode).replace('[FULL_NAME]',person.full_name).replace('[LAST_NAME]',person.last_name).replace('[FIRST_NAME]',person.first_name)
                    person.vkontaktephish = VkontaktephisherObject.checkThenPhishVkontakteProfile(person.vkontakte,person.vkontaktefinalphishingmessage,vkontakte_username,vkontakte_password)
                else:
                    print("Error, No Phishing Message Provided")
                    sys.exit(0)
                sleep(3)
            except:
                traceback.print_exc()
                continue
        else:
            continue
    try:
        VkontaktephisherObject.kill()
    except:
        print("Error Killing VKontakte Selenium instance")
    return peoplelist
    # If connected, send phishing message(-m), or generate custom one with markov chains(-mm)
    # Generate unique tracking codes before phishing
    # Output phished users + profiles + tracking codes to csv + console

# [MORE_SOCIAL_MEDIA_SITES_TAG]

# Code to check if each person has clicked by comparing unique tracking codes across web logs. 
# Loops through the logs looking up each persons code, is "smart" and ignores the sites automated crawlers which poison the logs
def checkclicks(peoplelist,weblogs):

    #linkedinclicked = ""
    #linkedinclickedip = ""
    #linkedinclickedtime = ""
    #linkedinclickeduseragent = ""

    file = open(weblogs, "r")
    for person in peoplelist:
        if person.facebookphish != "Sent":
            person.facebookclicked = "Message Not Sent"
            person.facebookclickedip =  person.facebookphish
        else:
            person.facebookclicked = "Not Clicked"
        if person.linkedinphish != "Sent":
            person.linkedinclicked = "Message Not Sent"
            person.linkedinclickedip =  person.linkedinphish
        else:
            person.linkedinclicked = "Not Clicked"
        if person.twitterphish != "Sent":
            person.twitterclicked = "Message Not Sent"
            person.twitterclickedip =  person.twitterphish
        else:
            person.twitterclicked = "Not Clicked"
        if person.vkontaktephish != "Sent":
            person.vkontakteclicked = "Message Not Sent"
            person.vkontakteclickedip =  person.vkontaktephish
        else:
            person.vkontakteclicked = "Not Clicked"
        for line in file:
            if person.facebooktrackingcode != "":
                if re.search(person.facebooktrackingcode, line):
                    # Only get first click by breaking after detection. 
                    # Also disregard facebook cralwer user agents:
                    # Facebook crawler agents:
                    # User-Agent: facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)
                    if "facebookexternalhit" not in line and "+http://www.facebook.com/externalhit_uatext.php" not in line:
                        person.facebookclicked = "Link Clicked"
                        person.facebookclickedip = line.split(" - ")[0]
                        person.facebookclickedtime = line.split(" - ")[1]
                        person.facebookclickeduseragent = line.split(" - ")[2].replace(">","&gt;").replace("<","&lt;")
                        break
            else:
                person.facebookclicked = "Message Not Sent"
                break
        # After looping through the file, need to use .seek(0) to reset it to the start
        file.seek(0)
        for line in file:  
            if person.linkedintrackingcode != "":
                if re.search(person.linkedintrackingcode, line):
                    # LinkedIn crawler agents:
                    # User-Agent: LinkedInBot/1.0 (compatible; Mozilla/5.0; Apache-HttpClient +http://www.linkedin.com)
                    if "LinkedInBot" not in line and "+http://www.linkedin.com" not in line:
                        person.linkedinclicked = "Link Clicked"
                        person.linkedinclickedip = line.split(" - ")[0]
                        person.linkedinclickedtime = line.split(" - ")[1]
                        person.linkedinclickeduseragent = line.split(" - ")[2].replace(">","&gt;").replace("<","&lt;")
                        break
            else:
                person.linkedinclicked = "Message Not Sent"
                break
        file.seek(0)
        for line in file:
            if person.twittertrackingcode != "":
                if re.search(person.twittertrackingcode, line):
                    # Twitter crawler agents:
                    # User-Agent: Twitterbot/1.0
                    # User-Agent: Mozilla/5.0 (compatible; AhrefsBot/6.1; +http://ahrefs.com/robot/)
                    # User-Agent: Mozilla/5.0 (compatible; TrendsmapResolver/0.1)
                    if "Twitterbot" not in line and "AhrefsBot" not in line and "TrendsmapResolver" not in line and "Python-urllib" not in line and "+http://www.alexa.com" not in line:
                        if line.split(" - ")[2] != "":
                            person.twitterclicked = "Link Clicked"
                            person.twitterclickedip = line.split(" - ")[0]
                            person.twitterclickedtime = line.split(" - ")[1]
                            person.twitterclickeduseragent = line.split(" - ")[2].replace(">","&gt;").replace("<","&lt;")
                            break
            else:
                person.twitterclicked = "Message Not Sent"
                break
        file.seek(0)
        for line in file:  
            if person.vkontaktetrackingcode != "":
                if re.search(person.vkontaktetrackingcode, line):
                    # VKontakte crawler agents:
                    # User-Agent: Mozilla/5.0 (compatible; vkShare; +http://vk.com/dev/Share)
                    if "vkShare" not in line and "+http://vk.com/dev/Share" not in line:
                        person.vkontakteclicked = "Link Clicked"
                        person.vkontakteclickedip = line.split(" - ")[0]
                        person.vkontakteclickedtime = line.split(" - ")[1]
                        person.vkontakteclickeduseragent = line.split(" - ")[2].replace(">","&gt;").replace("<","&lt;")
                        break
            else:
                person.vkontakteclicked = "Message Not Sent"
                break
        file.seek(0)
        # Non memory effiencent way, but better for HUGE log files
        #if person.facebooktrackingcode in open(weblogs).read():
        #    person.facebookclicked = "Y"
        #else:
        #    person.facebookclicked = "N"
    return peoplelist

# Parse arguments, select which sites to use, then have: 
# 3 options, either add and wait with given time (friendphish 2d) or just (add) or just (phish) or (check)
# this should mean you can 
#   1) (add) everyone to friends/contacts
#   2) (check) and see who has accepted the request
#   3) (phish) send a message to everyone who has accepted
#   4) (addphish [X hours]) add everyone, wait X hours and then phish them
# option to add tracking code to links based off string in phishing message like [TRACKING_ID]
#   5) (checkclicks) takes the tracking ID csv + web server logs (Apache+IIS+pythonsimpleserver) and gives info on who has clicked the link

parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='Social Attacker by Jacob Wilkin(Greenwolf)',
        usage='%(prog)s -f <function> -i <inputCSV> <options>')
parser.add_argument('-v', '--version', action='version',
    version='%(prog)s 0.1.0 : Social Attacker by Jacob Wilkin(Greenwolf)')
parser.add_argument('-vv', '--verbose', action='store_true',dest='vv',help='Verbose Mode')
parser.add_argument('-f', '--function',action='store', dest='function',required=True,choices=set(("prepare","add","check","generate","phish","addphish","checkclicks")),
    help='Specify the function to perform \'add\'(everyone on list),\'check\'(who has accepted the request),\'generate\'(unique phish messages),\'phish\'(all that have accepted),\'addphish\'(Add & Phish everyone on list) or \'checkclicks\'(to see who has clicked the links)')
parser.add_argument('-i', '--input',action='store', dest='input',required=True,
    help='The name of the csv file containing links to profiles, must include columns with header titled "Full Name","LinkedIn","Facebook","Twitter","Vkontakte" or the social attacker csv with tracking IDs if using the checklicks option')

parser.add_argument('-w', '--wait',action='store', dest='wait',required=False,
    help='The number of hours to wait after adding targets on the list, before sending the phishing messages')
parser.add_argument('-m', '--message',action='store', dest='message',required=False,
    help='The message that is sent to the targets: "[FULL_NAME]","[FIRST_NAME]","[LAST_NAME]" will be replaced with the targets name. "[TRACKING_ID]" will be replaced with a unique 6 character alphanumeric that will allow web logs to be loaded into social attacker to track clicks for each user. Example: "Hello [FIRSTNAME], Please click this link https://phishingdomain.com/macro_document.docx?t=[TRACKING_ID]".')
parser.add_argument('-mm', '--markovmessage',action='store', dest='markovmessage',required=False,
    help='Use Markov Chains based on target history to generate a custom message. A link must be provided to add to the end of the message. "[TRACKING_ID]" will be replaced with a unique 6 character alphanumeric that will allow web logs to be loaded into social attacker to track clicks for each user. Example: "https://phishingdomain.com/macro_document.docx?t=[TRACKING_ID]". Note: If using this option you must also specify a backup message to use with -m or --message incase Markov generation fails.')
parser.add_argument('-ml', '--markovlength',action='store', dest='markovlength',required=False,
    help='Set the max length in chars of the generated Markov Message, default is 140 if unset.')

parser.add_argument('-wl', '--weblogs',action='store', dest='weblogs',required=False,
    help='A weblog containing requests to the site, to pull out tracking IDs and check for clicks')

parser.add_argument('-s', '--showbrowser',action='store_true',dest='showbrowser',help='If flag is set then browser will be visible')

parser.add_argument('-a', '--all',action='store_true',dest='a',help='Flag to check all supported social media sites')
parser.add_argument('-fb', '--facebook',action='store_true',dest='fb',help='Flag to check Facebook')
parser.add_argument('-li', '--linkedin',action='store_true',dest='li',help='Flag to check LinkedIn')
parser.add_argument('-tw', '--twitter',action='store_true',dest='tw',help='Flag to check Twitter')
parser.add_argument('-vk', '--vkontakte',action='store_true',dest='vk',help='Flag to check Vkontakte')
# [MORE_SOCIAL_MEDIA_SITES_TAG] 

args = parser.parse_args()

if args.showbrowser:
    showbrowser=True
else:
    showbrowser=False

# A site needs to be specified
if not (args.a or args.fb or args.li or args.tw or args.vk) and args.function != "checkclicks":
    parser.error('No sites specified, add -a for all, or a combination of the sites you want to check using a mix of -fb -li -tw -vk')
# adding and phishing at the same need needs a wait time
if args.function == "addphish" and not args.wait:
    parser.error('Please supply a wait time for the \'addphish\' option with -w')
# tracking needs a weblog
if args.function == "checkclicks" and not args.weblogs:
    parser.error('To use the \'checkclicks\' option, please provide an apache,iis or python simple server log file so tracking IDs can be extracted using -wl')
# A phish needs a message:
if ((args.function == "phish" or args.function == "addphish") and not args.message):
    parser.error('If you wish to send a phishing message, please provide a message with -m, if you wish to use custom message generation with markov chains use -mm and provide a phishing link. Note you must always provide a -m message as a backup for if Markov generation fails. For more details see -h for help')
if (args.function == "prepare" and not args.li):
    parser.error("The 'prepare' function only works if you specify LinkedIn (-li) and a company url as the input")

if (args.function == "add" or args.function == "check" or args.function == "generate" or args.function == "phish" or args.function == "addphish"): 
    # import social media profiles + names from social mapper CSV into person class from social mapper
    # read csv into data using pandas, split up columns into a name,facebook and linkedin column
    data = pandas.read_csv(args.input)
    data.replace(numpy.nan,'', inplace=True)
    try:
        name_column = data['Full Name']
    except:
        print("No column called \"Full Name\" found in %s" % args.input)
        sys.exit()
    if (args.a or args.fb):
        try:
            facebook_column = data['Facebook']
            if (args.function == "phish" and args.markovmessage):
                try:
                    facebook_markovmessage_column = data['Facebook Markov Message']
                except:
                    print("No column called \"Facebook Markov Message\" found in %s" % args.input)
                    sys.exit()
        except:
            print("No column called \"Facebook\" found in %s" % args.input)
            sys.exit()
    if (args.a or args.li):
        try:
            linkedin_column = data['LinkedIn']
            if (args.function == "phish" and args.markovmessage):
                try:
                    linkedin_markovmessage_column = data['LinkedIn Markov Message']
                except:
                    print("No column called \"LinkedIn Markov Message\" found in %s" % args.input)
                    sys.exit()
        except:
            print("No column called \"LinkedIn\" found in %s" % args.input)
            sys.exit()
    if (args.a or args.tw):
        try:
            twitter_column = data['Twitter']
            if (args.function == "phish" and args.markovmessage):
                try:
                    twitter_markovmessage_column = data['Twitter Markov Message']
                except:
                    print("No column called \"Twitter Markov Message\" found in %s" % args.input)
                    sys.exit()
        except:
            print("No column called \"Twitter\" found in %s" % args.input)
            sys.exit()
    if (args.a or args.vk):
        try:
            vkontakte_column = data['Vkontakte']
            if (args.function == "phish" and args.markovmessage):
                try:
                    vkontakte_markovmessage_column = data['Vkontakte Markov Message']
                except:
                    print("No column called \"Vkontakte Markov Message\" found in %s" % args.input)
                    sys.exit()
        except:
            print("No column called \"Vkontakte\" found in %s" % args.input)
            sys.exit()
    # [MORE_SOCIAL_MEDIA_SITES_TAG]

    # interate through the name column, adding the relevant facebook/linkedin profiles to create a target list. If linkedin and facebook are both blank, skip person
    line=0
    peoplelist = []
    for full_name in name_column:
        first_name = full_name.split(" ")[0]
        last_name = full_name.split(" ",1)[1]
        person = Person(first_name, last_name, full_name)
        if (args.a or args.fb):
            person.facebook = facebook_column[line]
        if (args.a or args.li):
            person.linkedin = linkedin_column[line]
        if (args.a or args.tw):
            person.twitter = twitter_column[line]
        if (args.a or args.vk):
            person.vkontakte = vkontakte_column[line]            
        if (args.function == "phish" and args.markovmessage):
            if (args.a or args.fb):
                person.facebookmarkovmessage = facebook_markovmessage_column[line]
            if (args.a or args.li):    
                person.linkedinmarkovmessage = linkedin_markovmessage_column[line]
            if (args.a or args.tw):    
                person.twittermarkovmessage = twitter_markovmessage_column[line]
            if (args.a or args.vk):    
                person.vkontaktemarkovmessage = vkontakte_markovmessage_column[line]
        # Skip person if no linkedin or facebook profile
        if (person.linkedin == "" and person.facebook == "" and person.twitter == "" and person.vkontakte == ""):
            if args.vv:
                print("Removed %s: no profiles found" % person.full_name)
                print(person.full_name)
        # [MORE_SOCIAL_MEDIA_SITES_TAG]
        else:
            peoplelist.append(person)
        line += 1
elif args.function == "checkclicks":
    # Code here to parse out the social attacker csv, names, links, tracking codes
    # Data read in format:
    # Full Name   Facebook Profile  Facebook Status    Facebook Tracking ID    LinkedIn Profile  LinkedIn Status  LinkedIn Tracking ID  Twitter Profile  Twitter Status  Twitter Tracking ID   Vkontakte Profile  Vkontakte Status  Vkontakte Tracking ID
    data = pandas.read_csv(args.input)
    data.replace(numpy.nan,'', inplace=True)
    try:
        name_column = data['Full Name']
    except:
        print("No column called \"Full Name\" found in %s" % args.input)
        sys.exit()
    try:
        facebook_column = data['Facebook']
    except:
        print("No column called \"Facebook\" found in %s" % args.input)
        sys.exit()
    try:
        facebookstatus_column = data['Facebook Status']
    except:
        print("No column called \"Facebook Status\" found in %s" % args.input)
        sys.exit()
    try:
        facebooktrackingid_column = data['Facebook Tracking ID']
    except:
        print("No column called \"Facebook Tracking ID\" found in %s" % args.input)
        sys.exit()
    try:
        facebookmessage_column = data['Facebook Message']
    except:
        print("No column called \"Facebook Message\" found in %s" % args.input)
        sys.exit()
    try:
        linkedin_column = data['LinkedIn']
    except:
        print("No column called \"LinkedIn\" found in %s" % args.input)
        sys.exit()
    try:
        linkedinstatus_column = data['LinkedIn Status']
    except:
        print("No column called \"LinkedIn Status\" found in %s" % args.input)
        sys.exit()
    try:
        linkedintrackingid_column = data['LinkedIn Tracking ID']
    except:
        print("No column called \"LinkedIn Tracking ID\" found in %s" % args.input)
        sys.exit()
    try:
        linkedinmessage_column = data['LinkedIn Message']
    except:
        print("No column called \"LinkedIn Message\" found in %s" % args.input)
        sys.exit()
    try:
        twitter_column = data['Twitter']
    except:
        print("No column called \"Twitter\" found in %s" % args.input)
        sys.exit()
    try:
        twitterstatus_column = data['Twitter Status']
    except:
        print("No column called \"Twitter Status\" found in %s" % args.input)
        sys.exit()
    try:
        twittertrackingid_column = data['Twitter Tracking ID']
    except:
        print("No column called \"Twitter Tracking ID\" found in %s" % args.input)
        sys.exit()
    try:
        twittermessage_column = data['Twitter Message']
    except:
        print("No column called \"Twitter Message\" found in %s" % args.input)
        sys.exit()
    try:
        vkontakte_column = data['Vkontakte']
    except:
        print("No column called \"Vkontakte\" found in %s" % args.input)
        sys.exit()
    try:
        vkontaktestatus_column = data['Vkontakte Status']
    except:
        print("No column called \"Vkontakte Status\" found in %s" % args.input)
        sys.exit()
    try:
        vkontaktetrackingid_column = data['Vkontakte Tracking ID']
    except:
        print("No column called \"Vkontakte Tracking ID\" found in %s" % args.input)
        sys.exit()
    try:
        vkontaktemessage_column = data['Vkontakte Message']
    except:
        print("No column called \"Vkontakte Message\" found in %s" % args.input)
        sys.exit()

    line=0
    peoplelist = []
    for full_name in name_column:
        first_name = full_name.split(" ")[0]
        last_name = full_name.split(" ",1)[1]
        person = Person(first_name, last_name, full_name)
        person.facebook = facebook_column[line]
        person.facebookphish = facebookstatus_column[line]
        person.facebooktrackingcode = facebooktrackingid_column[line]
        person.facebookfinalphishingmessage = facebookmessage_column[line]
        person.linkedin = linkedin_column[line]
        person.linkedinphish = linkedinstatus_column[line]
        person.linkedintrackingcode = linkedintrackingid_column[line]
        person.linkedinfinalphishingmessage = linkedinmessage_column[line]
        person.twitter = twitter_column[line]
        person.twitterphish = twitterstatus_column[line]
        person.twittertrackingcode = twittertrackingid_column[line]  
        person.twitterfinalphishingmessage = twittermessage_column[line]
        person.vkontakte = vkontakte_column[line]
        person.vkontaktephish = vkontaktestatus_column[line]
        person.vkontaktetrackingcode = vkontaktetrackingid_column[line]
        person.vkontaktefinalphishingmessage = vkontaktemessage_column[line]
        peoplelist.append(person)
        line += 1
        # TODO all the loading in of the tracking IDs + Status here
        # filewriter.write("Full Name,Facebook,Facebook Status,Facebook Tracking ID,LinkedIn,LinkedIn Status,LinkedIn Tracking ID" + "\n")

# code to confirm csv data has been stored into data structures correctly correctly
#for person in peoplelist:
#    print(person.full_name)
#    print(person.first_name)
#    print(person.last_name)
#    print(person.facebook)
#    print(person.linkedin)
#    print(person.twitter)
#    print(person.vkontakte)
#    print("\n")

# Code to prepare a linkedin account for running social attacker against a specific company
if args.function == "prepare" and args.li:
    if not (linkedin_username == "" or linkedin_password == ""):
        connection_list = prepare_linkedin(args.input)
    else:
        print("Please provide LinkedIn Login Credentials in the social_attacker.py file, for now skipping LinkedIn Preparation")
    
    #connection_list.append([full_name,profile_link,status])

    # Write csv file to give update on status
    outputfilename = "Results/" + args.input.replace("\"","").replace("/","-") + "-social-attacker-LinkedIn-Preparation.csv"
    filewriter = open(outputfilename.format(outputfilename), 'w')
    filewriter.write("Full Name,Profile,Status" + "\n")
    t = PrettyTable(['Full Name','Profile','Status'])
    for connection in connection_list:
        filewriter.write("\"" + connection[0] + "\"" + "," + "\"" + connection[1] + "\"" + "," + "\"" + connection[2] + "\"" + "\n")
        t.add_row([connection[0],connection[1],connection[2]])
        # [MORE_SOCIAL_MEDIA_SITES_TAG]
    filewriter.close()
    print(t)
    print("\n")
    print("LinkedIn Preparation Results can also be found in: " + outputfilename)

# function to add facebook targets
# function to add Linkedin targets
# [OPTIONAL] function to follow twitter
# [OPTIONAL] function to add VK
if (args.function == "add" or args.function == "addphish"): 
    if args.a == True or args.fb == True:
        if not (facebook_username == "" or facebook_password == ""):
            add_facebook(peoplelist)
        else:
            print("Please provide Facebook Login Credentials in the social_attacker.py file, for now skipping Facebook Friending")
    if args.a == True or args.li == True:
        if not (linkedin_username == "" or linkedin_password == ""):
            add_linkedin(peoplelist)
        else:
            print("Please provide LinkedIn Login Credentials in the social_attacker.py file, for now skipping LinkedIn Connecting")
    if args.a == True or args.tw == True:
        if not (twitter_username == "" or twitter_password == ""):
            add_twitter(peoplelist)
        else:
            print("Please provide Twitter Login Credentials in the social_attacker.py file, for now skipping Twitter Following/Connecting")
    if args.a == True or args.vk == True:
        if not (vkontakte_username == "" or vkontakte_password == ""):
            add_vkontakte(peoplelist)
        else:
            print("Please provide Vkontakte Login Credentials in the social_attacker.py file, for now skipping Vkontakte Connecting")
    # [MORE_SOCIAL_MEDIA_SITES_TAG] 

# If addphishing, wait the set delay before checking & phishing
if args.function == "addphish":
    seconds = args.wait*3600
    seconds = 360
    print("\nSleeping for %s hours to allow time for connections to be accepted" % args.wait)
    time.sleep(seconds)

# function to check if accepted facebook (if just checking, report results)
# function to check if accepted linkedin (if just checking, report results)
# This is just to check
if (args.function == "check"): 
    if args.a == True or args.fb == True:
        if not (facebook_username == "" or facebook_password == ""):
            peoplelist = check_facebook(peoplelist)
        else:
            print("Please provide Facebook Login Credentials in the social_attacker.py file, for now skipping Facebook Checking")
    if args.a == True or args.li == True:
        if not (linkedin_username == "" or linkedin_password == ""):
            peoplelist = check_linkedin(peoplelist)
        else:
            print("Please provide LinkedIn Login Credentials in the social_attacker.py file, for now skipping LinkedIn Checking")
    if args.a == True or args.tw == True:
        if not (twitter_username == "" or twitter_password == ""):
            peoplelist = check_twitter(peoplelist)
        else:
            print("Please provide Twitter Login Credentials in the social_attacker.py file, for now skipping Twitter Checking")
    if args.a == True or args.vk== True:
        if not (vkontakte_username == "" or vkontakte_password == ""):
            peoplelist = check_vkontakte(peoplelist)
        else:
            print("Please provide Vkontakte Login Credentials in the social_attacker.py file, for now skipping Vkontakte Checking")
    # [MORE_SOCIAL_MEDIA_SITES_TAG]

    # Write csv file to give update on status
    outputfilename = "Results/" + args.input.replace("\"","").replace("/","-") + "-social-attacker-status.csv"
    filewriter = open(outputfilename.format(outputfilename), 'w')
    filewriter.write("Full Name,Facebook Status,LinkedIn Status,Twitter Status,Vkontakte Status" + "\n")
    #t = PrettyTable(['Full Name','Facebook Status','LinkedIn Status','Twitter Status','Vkontakte Status'])
    for person in peoplelist:
        filewriter.write("\"" + person.full_name + "\"" + "," + "\"" + person.facebookstatus + "\"" + "," + "\"" + person.linkedinstatus + "\"" + "," + "\"" + person.twitterstatus + "\"" + "," + "\"" + person.vkontaktestatus + "\"" + "\n")
        #t.add_row([person.full_name,person.facebookstatus,person.linkedinstatus,person.twitterstatus,person.vkontaktestatus])
        print(person.full_name)
        if person.facebook != "":
            print("\tFacebook: " + person.facebookstatus)
            #print("\t\t" + person.facebookclicked)
        if person.linkedin != "":
            print("\tLinkedIn: " + person.linkedinstatus)
            #print("\t\t" + person.linkedinclicked)
        if person.twitter != "":
            print("\tTwitter: " + person.twitterstatus)
            #print("\t\t" + person.twitterclicked)
        if person.vkontakte != "":
            print("\tVKontakte: " + person.vkontaktestatus)
            #print("\t\t" + person.vkontakteclicked)       
        print("")

        # [MORE_SOCIAL_MEDIA_SITES_TAG]
    filewriter.close()
    #print(t)
    print("\n")
    print("Status of connection requests can also be found in: " + outputfilename)

# Function to generate unique markov messages for each user
# These should output a csv with the persons name and profiles and unique messages
# Full Name   Facebook    Facebook Markov Message    LinkedIn    LinkedIn Markov Message
if (args.function == "generate" or (args.function == "addphish" and args.markovmessage)):
    # Call functions to generate the markov messages here
    if args.a == True or args.fb == True:
        if not (facebook_username == "" or facebook_password == ""):
            peoplelist = generate_markov_facebook(peoplelist)
        else:
            print("Please provide Facebook Login Credentials in the social_attacker.py file, for now skipping Facebook Markov Generation")
    if args.a == True or args.li == True:
        if not (linkedin_username == "" or linkedin_password == ""):
            peoplelist = generate_markov_linkedin(peoplelist)
        else:
            print("Please provide LinkedIn Login Credentials in the social_attacker.py file, for now skipping LinkedIn Markov Generation")
    if args.a == True or args.tw == True:
        if not (twitter_username == "" or twitter_password == ""):
            peoplelist = generate_markov_twitter(peoplelist)
        else:
            print("Please provide Twitter Login Credentials in the social_attacker.py file, for now skipping Twitter Markov Generation")
    if args.a == True or args.vk == True:
        if not (vkontakte_username == "" or vkontakte_password == ""):
            peoplelist = generate_markov_vkontakte(peoplelist)
        else:
            print("Please provide Vkontakte Login Credentials in the social_attacker.py file, for now skipping Vkontakte Markov Generation")


    if args.function == "generate":
        # Generate CSV file here
        outputfilename = "Results/" + args.input.replace("\"","").replace("/","-") + "-social-attacker-markov-results.csv"
        filewriter = open(outputfilename.format(outputfilename), 'w')
        filewriter.write("Full Name,Facebook,Facebook Markov Message,LinkedIn,LinkedIn Markov Message,Twitter,Twitter Markov Message,Vkontakte,Vkontakte Markov Message" + "\n")
        #t = PrettyTable(['Full Name','Facebook','Facebook Markov Message','LinkedIn','LinkedIn Markov Message','Twitter','Twitter Markov Message','Vkontakte','Vkontakte Markov Message'])
        print("")
        for person in peoplelist:
            filewriter.write("\"" + person.full_name + "\"" + "," + "\"" + person.facebook + "\"" + "," + "\"" + person.facebookmarkovmessage + "\"" + "," + "\"" + person.linkedin + "\"" + "," + "\"" + person.linkedinmarkovmessage + "\"" + "," + "\"" + person.twitter + "\"" + "," + "\"" + person.twittermarkovmessage + "\"" +"," + "\"" + person.vkontakte + "\"" + "," + "\"" + person.vkontaktemarkovmessage + "\"" + "\n")
            #t.add_row([person.full_name,person.facebook,person.facebookmarkovmessage,person.linkedin,person.linkedinmarkovmessage,person.twitter,person.twittermarkovmessage,person.vkontakte,person.vkontaktemarkovmessage])
        
            print(person.full_name)
            if person.facebook != "":
                print("\tFacebook: " + person.facebookmarkovmessage)
                #print("\t\t" + person.facebookclicked)
            if person.linkedin != "":
                print("\tLinkedIn: " + person.linkedinmarkovmessage)
                #print("\t\t" + person.linkedinclicked)
            if person.twitter != "":
                print("\tTwitter: " + person.twittermarkovmessage)
                #print("\t\t" + person.twitterclicked)
            if person.vkontakte != "":
                print("\tVKontakte: " + person.vkontaktemarkovmessage)
                #print("\t\t" + person.vkontakteclicked)       
            print("")

            # [MORE_SOCIAL_MEDIA_SITES_TAG]
        filewriter.close()
        #print(t)
        print("\n")
        print("Unique History based Markov Messages can also be found in: " + outputfilename)


# function to send phishing message of facebook to results of successful checked (accepted)
# function to send phishing message of linkedin to results of successful checked (accepted)
# These should output a csv with the persons name and profiles with their unique tracking ID
# Full Name   Facebook Profile    Facebook Tracking ID    LinkedIn Profile    LinkedIn Tracking ID
# This function needs to check & phish in one go 
if (args.function == "phish" or args.function == "addphish"): 
    if args.a == True or args.fb == True:
        if not (facebook_username == "" or facebook_password == ""):
            peoplelist = checkphish_facebook(peoplelist)
        else:
            print("Please provide Facebook Login Credentials in the social_attacker.py file, for now skipping Facebook Phishing")
    if args.a == True or args.li == True:
        if not (linkedin_username == "" or linkedin_password == ""):
            peoplelist = checkphish_linkedin(peoplelist)
        else:
            print("Please provide LinkedIn Login Credentials in the social_attacker.py file, for now skipping LinkedIn Phishing")
    if args.a == True or args.tw == True:
        if not (twitter_username == "" or twitter_password == ""):
            peoplelist = checkphish_twitter(peoplelist)
        else:
            print("Please provide Twitter Login Credentials in the social_attacker.py file, for now skipping Twitter Phishing")
    if args.a == True or args.vk == True:
        if not (vkontakte_username == "" or vkontakte_password == ""):
            peoplelist = checkphish_vkontakte(peoplelist)
        else:
            print("Please provide Vkontakte Login Credentials in the social_attacker.py file, for now skipping Vkontakte Phishing")
    # [MORE_SOCIAL_MEDIA_SITES_TAG]
    outputfilename = "Results/" + args.input.replace("\"","").replace("/","-") + "-social-attacker-phishing-results.csv"
    filewriter = open(outputfilename.format(outputfilename), 'w')
    filewriter.write("Full Name,Facebook,Facebook Status,Facebook Tracking ID,Facebook Message,LinkedIn,LinkedIn Status,LinkedIn Tracking ID,LinkedIn Message,Twitter,Twitter Status,Twitter Tracking ID,Twitter Message,Vkontakte,Vkontakte Status,Vkontakte Tracking ID,Vkontakte Message" + "\n")
    #t = PrettyTable(['Full Name','Facebook','Facebook Status','Facebook Tracking ID','Facebook Message','LinkedIn','LinkedIn Status','LinkedIn Tracking ID','LinkedIn Message','Twitter','Twitter Status','Twitter Tracking ID','Twitter Message','Vkontakte','Vkontakte Status','Vkontakte Tracking ID','Vkontakte Message'])
    print("")
    for person in peoplelist:
        #filewriter.write("\"" + person.full_name + "\"" + "," + "\"" + person.facebook + "\"" + "," + "\"" + person.facebookphish + "\"" + "," + "\"" + person.facebooktrackingcode + "\"" + ',"' + "\"" + person.facebookfinalphishingmessage + "\"" + '",' + "\"" + person.linkedin + "\"" + "," + "\"" + person.linkedinphish + "\"" + "," + "\"" + person.linkedintrackingcode + "\"" + ',"' + "\"" + person.linkedinfinalphishingmessage + "\"" + '",' + "\"" + person.twitter + "\"" + "," + "\"" + person.twitterphish + "\"" + "," + "\"" + person.twittertrackingcode + "\"" + ',"' + "\"" + person.twitterfinalphishingmessage + "\"" + '",' + "\"" + person.vkontakte + "\"" + "," + "\"" + person.vkontaktephish + "\"" + "," + "\"" + person.vkontaktetrackingcode + "\"" + ',"' + "\"" + person.vkontaktefinalphishingmessage + "\"" + '",' + "\"" + "\n")
        filewriter.write("\"" + person.full_name + "\"" + "," + "\"" + person.facebook + "\"" + "," + "\"" + person.facebookphish + "\"" + "," + "\"" + person.facebooktrackingcode + "\"" + ',"' + person.facebookfinalphishingmessage + '",' + "\"" + person.linkedin + "\"" + "," + "\"" + person.linkedinphish + "\"" + "," + "\"" + person.linkedintrackingcode + "\"" + ',"' + person.linkedinfinalphishingmessage + '",' + "\"" + person.twitter + "\"" + "," + "\"" + person.twitterphish + "\"" + "," + "\"" + person.twittertrackingcode + "\"" + ',"' + person.twitterfinalphishingmessage + '",' + "\"" + person.vkontakte + "\"" + "," + "\"" + person.vkontaktephish + "\"" + "," + "\"" + person.vkontaktetrackingcode + "\"" + ',"' + person.vkontaktefinalphishingmessage + '"' + "\n")

        print(person.full_name)
        if person.facebook != "":
            print("\tFacebook: " + person.facebookphish)
            #print("\t\t" + person.facebookclicked)
        if person.linkedin != "":
            print("\tLinkedIn: " + person.linkedinphish)
            #print("\t\t" + person.linkedinclicked)
        if person.twitter != "":
            print("\tTwitter: " + person.twitterphish)
            #print("\t\t" + person.twitterclicked)
        if person.vkontakte != "":
            print("\tVKontakte: " + person.vkontaktephish)
            #print("\t\t" + person.vkontakteclicked)       
        print("")

        #t.add_row([person.full_name,person.facebook,person.facebookphish,person.facebooktrackingcode,person.facebookfinalphishingmessage,person.linkedin,person.linkedinphish,person.linkedintrackingcode,person.linkedinfinalphishingmessage,person.twitter,person.twitterphish,person.twittertrackingcode,person.twitterfinalphishingmessage,person.vkontakte,person.vkontaktephish,person.vkontaktetrackingcode,person.vkontaktefinalphishingmessage])
        # [MORE_SOCIAL_MEDIA_SITES_TAG]
    filewriter.close()
    #print(t)
    print("\n")
    print("Full Phishing Results and Tracking Codes can also be found in: " + outputfilename)    

# function to parse the social attacker tracking ID csv
# check it against web logs to create campaign results csv
# Log format:
# []
if (args.function == "checkclicks"): 
    if args.weblogs:
        peoplelist = checkclicks(peoplelist,args.weblogs)
    else:
        print("Web Logs not provided, exiting")
        sys.exit()
    print("")
    outputfilename = "Results/" + args.input.replace("\"","").replace("/","-") + "-social-attacker-whoclicked-results.csv"
    filewriter = open(outputfilename.format(outputfilename), 'w')
    filewriter.write("Full Name,Facebook,Facebook Message,Facebook Clicked,Facebook IP,Facebook DateTime,Facebook User Agent,LinkedIn,LinkedIn Message,LinkedIn Clicked,LinkedIn IP,LinkedIn DateTime,LinkedIn User Agent,Twitter,Twitter Message,Twitter Clicked,Twitter IP,Twitter DateTime,Twitter User Agent,Vkontakte,Vkontakte Message,Vkontakte Clicked,Vkontakte IP,Vkontakte DateTime,Vkontakte User Agent" + "\n")

    # HTML Generation here
    outputhtmlfilename = "Results/" + args.input.replace("\"","").replace("/","-") + "-social-attacker-whoclicked-results.html"
    filewriterhtml = open(outputhtmlfilename.format(outputhtmlfilename), 'w')
    # write head here

    css = """
    <style type="text/css">
.people  {width:100%;border-collapse:collapse;border-spacing:0;}
.people td{font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:black;}
.people th{background-color: #12db00;color: white;font-family:Arial, sans-serif;font-size:14px;font-weight:normal;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:black;}

.people .name{width:200px;text-align:center;vertical-align:middle}

.people .profileshead{width:120px;text-align:center;vertical-align:middle}
.people .messagehead{width:30%;text-align:center;vertical-align:middle}
.people .clickstatushead{width:15%;text-align:center;vertical-align:middle}
.people .useragenthead{text-align:center;vertical-align:middle}

.people .profiles{width:120px;text-align:center;vertical-align:middle}
.people .message{width:35%;text-align:center;vertical-align:middle}
.people .clickstatus{width:10%;text-align:center;vertical-align:middle}
.people .useragent{text-align:center;vertical-align:middle}

.people tr:nth-child(even){background-color: #f2f2f2;}

.people tbody:hover td[rowspan], .people tr:hover {background-color: #aaa;}


.people .profiles span {
   visibility: hidden;
   background-color: black;
   color: #fff;
   text-align: center;
   border-radius: 6px;
   padding: 5px 0;
   /* Position the tooltip */
   position: absolute;
   left:25%;
   z-index: 1;
   }

.people .profiles:hover span{visibility: visible;}

</style>
    """

    tablehead = """
<table class="people">
  <tr>
    <th class="name">Name</th>
    <th class="profileshead">Profiles</th>
    <th class="messagehead">Message</th>
    <th class="clickstatushead">Click Status<br>Datatime<br>IP Address</th>
    <th class="useragenthead">User Agent</th>
  </tr>
    """

    filewriterhtml.write(css)
    filewriterhtml.write(tablehead)

    for person in peoplelist:
        filewriter.write("\"" + person.full_name + "\"" + "," + "\"" + person.facebook + "\"" + "," + "\"" + person.facebookfinalphishingmessage + "\"" + "," + "\"" + person.facebookclicked + "\"" + "," + "\""  + person.facebookclickedip + "\"" + "," + "\"" + person.facebookclickedtime + "\"" + "," + "\"" + person.facebookclickeduseragent + "\"" + "," + "\"" + person.linkedin + "\"" + "," + "\"" + person.linkedinfinalphishingmessage + "\"" + "," + "\"" + person.linkedinclicked + "\"" + "," + "\""  + person.linkedinclickedip + "\"" + "," + "\"" + person.linkedinclickedtime + "\"" + "," + "\"" + person.linkedinclickeduseragent + "\"" + "," + "\"" + person.twitter + "\"" + "," + "\"" + person.twitterfinalphishingmessage + "\"" + "," + "\"" + person.twitterclicked + "\"" + "," + "\""  + person.twitterclickedip + "\"" + "," + "\"" + person.twitterclickedtime + "\"" + "," + "\"" + person.twitterclickeduseragent + "\"" + "," + "\"" + person.vkontakte + "\"" + "," + "\"" + person.vkontaktefinalphishingmessage + "\"" + "," + "\"" + person.vkontakteclicked + "\"" + "," + "\""  + person.vkontakteclickedip + "\"" + "," + "\"" + person.vkontakteclickedtime + "\"" + "," + "\"" + person.vkontakteclickeduseragent + "\"" + "\n")
        #t = PrettyTable(['Full Name','Facebook','Facebook Message','Facebook Clicked','Facebook IP','Facebook DateTime','Facebook User Agent','LinkedIn','LinkedIn Message','LinkedIn Clicked','LinkedIn IP','LinkedIn DateTime','LinkedIn User Agent','Twitter','Twitter Message','Twitter Clicked','Twitter IP','Twitter DateTime','Twitter User Agent','Vkontakte','Vkontakte Message','Vkontakte Clicked','Vkontakte IP','Vkontakte DateTime','Vkontakte User Agent'])
        #t.add_row([person.full_name,person.facebook,person.facebookfinalphishingmessage,person.facebookclicked,person.facebookclickedip,person.facebookclickedtime,person.facebookclickeduseragent,person.linkedin,person.linkedinfinalphishingmessage,person.linkedinclicked,person.linkedinclickedip,person.linkedinclickedtime,person.linkedinclickeduseragent,person.twitter,person.twitterfinalphishingmessage,person.twitterclicked,person.twitterclickedip,person.twitterclickedtime,person.twitterclickeduseragent,person.vkontakte,person.vkontaktefinalphishingmessage,person.vkontakteclicked,person.vkontakteclickedip,person.vkontakteclickedtime,person.vkontakteclickeduseragent])

        print(person.full_name)
        if person.facebook != "":
            print("\tFacebook: " + person.facebookclicked)
            #print("\t\t" + person.facebookclicked)
        if person.linkedin != "":
            print("\tLinkedIn: " + person.linkedinclicked)
            #print("\t\t" + person.linkedinclicked)
        if person.twitter != "":
            print("\tTwitter: " + person.twitterclicked)
            #print("\t\t" + person.twitterclicked)
        if person.vkontakte != "":
            print("\tVKontakte: " + person.vkontakteclicked)
            #print("\t\t" + person.vkontakteclicked)       
        print("")


        # Add rows for html report here in the body
        html = """
<tbody>
  <tr>
    <td class="name" rowspan="4">%s</td>
    <td class="profiles">
      <a href="%s">
      <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAOEAAADhCAMAAAAJbSJIAAAAb1BMVEU6VZ////82Up4zUJ1UbKx4ibswTpyMmsQ5V6EtTJupss8nSJnN0+WVosgqSpo4U56eqcyDksDj5vBwgbb3+PxFXqNabqt9jb3S2OhidbC9xdy3v9l0hLjZ3etLY6bq7fTEyt4dQpdJYqekrs2uttK97JEgAAADFUlEQVR4nO3c2XLiMBBAUUZmM3IsFsNgSIAk/P83TsLzjCNbI3c3de9rqlw+BV7VZDIhIiIiIiIiIiIiIiIiIlJeCM4VxbzsrJDey8G50s/3h91ss3jp7LdJYii8262rbfPr545eem/753y9qWJwjypzwqJuT7E6i0JX7459fOaEvn3r5zMmLPy5r8+W0L9Gn15MCkO9GuAzJHSh9xFoS1hcrsOAVoTzdsghaEhYTAcDbQjdfjjQhDAshx6DRoShrhKAFoR+nQI0ICzaJKABYZlyEFoQ1p9pQPVCd0m4UJgQ+lsiULvQXVKB2oW+1ysZg8KwTAYqF5ZpF3sDQr99cqFLvJ3RL0y+2usXDnw1Y0YYUh58TQiL3X8Aql57Kvschs3xdF/9pftC8fphj3vSalZ6X5tbA/axJ5rtzhdBem+HVEeeaKq55s+po1DHAW/vJj+/yfdifdxX1OYX9LuwjxIejH5Fv3LTGOBJ8eXup+KEH056P4cXJby+S+9mQlHCUy29mwlFCddz6d1MKEq4sXsmjRTOEGoOIUL9IUSoP4QI9YcQof4QItQfQoT6Q4hQR27+78qYucRX37GFR7Jrb65ddBQz1Hbv2sCjpSixvEcgEitlhcN+cNenRnZxagThm+wK6ghC4TXiEYSr8tmFwstvIwhb2XX+EYR72St+fmEj6htDuBW+a8svPArPauQXnp9e+CI8jZJfKP38mF8ofDnML2wuwsOn2YVX6ena7MKt9PRpduHt6YUr6eHM7MKF9HBmduGr9OvU7MKp9BR4bmEjDcwulJ9zzy2U/+1hbqH0s1N+4afsq8QRhPKT/LmFB+kb7+xC6Tua7ELhdacRhOLPTtmFCv7ZQOY14LP4xWISlh2FqFkM17UF8VPpF7Hjb3HTJl2nSwXAzp5jnqYrhAj1hxCh/hAi1B9ChPpDiFB/CBHqDyFC/SFEqD+ECPWHEKH+ECLUH0KE+kOIUH8IEeoPIUL9IUSoP4QI9YcQof4QItQfQoT6Q4hQfwgR6g8hQv0hRKg/hAj1hxCh/hAi1B9ChD36A+1ASVvVoq0WAAAAAElFTkSuQmCC" width=auto height=auto style="max-width:100px; max-height:100px;">
      <span>%s</span>
    </td>
    <td class="message">%s</td>
    <td class="clickstatus"><b>%s</b><br>%s<br>%s</td>
    <td class="useragent">%s</td>
  </tr>
  <tr>
    <td class="profiles">
      <a href="%s">
      <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAOEAAADhCAMAAAAJbSJIAAAAhFBMVEUAe7X///8AcbDi6/MAd7N9rM4Ac7G70eStyN/I2ukAebQAdbIAcLDY6fLM4e5QmsXn8ve10+U5j7/0+vx2qc2Cs9Ntq88Af7idw9uly+EgiLxvpMpTnsg4k8JEk8Lq8/i92uqev9qNu9jR4+6uy+CZvNh4sNGvyuCIstJinceTuNUxir3eoYF2AAAEwklEQVR4nO2dbXfiKhRGARk6gjEvjho1tzq215lO////u1FrrTZQOwsP9dxnf+kHk7WyCxxIOICQB7K6mU8FC+ZNnb16iZe/ZaWcTv1k0dBOVeWJYZErm/qpImNVXhwNh4JP8R3RYngwHA64FeAeOxjuDQvBU7BVFMXOMOdYRffofGtYqtTPcUVU2RpWfIuwraeVFBnnImwLMRO1S/0QV8XVouFcSdtY04h56me4MnPBZLANAAAAAAAAAAAAAAAAAID/NVYbpQbKOKZpANboRT3sFVm5rgYM5yCtmc5e86pkb2K4laN1a3lCdm9SP1NU7D7b6IQNp3wAa7N3glKO+Sha974EtyzYZASYdaegHM25hJtpt6CUJZNoY2Y+Q8mjEK0deQ1rFoWon7yCsmARTl3tN5Qs0o/UKmCYc2iIqqu3P/CDQ5eoegHDbxwMzUPAkMWwxvm7QykrDu3Qjf2CI83B0FZ+wxWLHj8UTCccmmFoUFPwKMJAIbKIpFu0pyUyaYVb3KRLMOMQRw+YTYfglJOhMPnyTLDktgDOTU+GNsWCTxt8xYh1tn/bH62aAZcoeopT03zx46nSiqffDq21tcwaIADgK2CUn9Og6gJXns0aW9sGLWdecNsARqh0ivnV9zJ8eqvo/viv7P8+KlrrjHjOJ+P68a795a6crSf5szWp9um4/FubuQtc+eswCGpNmvVDcT5VMCr66/s0+QGRDL/vDbWqHv3zIEU9TZAgENPQmqp7svVI+Uw+4o1pqENzIAdq6o1XIhrqjwpwT1HRNsdohtaEZkBOmJDW1GiGpgz8fMaaUjGW4aC5XFDKMaFiNMOL6+iOhq4txjLMPyVImQURybD+RCvc8UCW5BnL0D+S8bChqqeRDC/rCt8yonrdiGT4F1Bl66QzpJp/TWcoNzQD1ISGGU01TWgo70kKMaUhTaxJaZiRdIkpDeUzRTRNakiS7JHUsKSopkkNSfqLpIaSYliT1vAfgoaY1nBM0BCjGy5Xs/pnPVsVl1w8I2iIcQ2z8Xy7RtM5YwbTzccvjSuC1QAxDZcL8zZ0OJV/9HmqGNyU4fuN0rX+6PPNTdXSzo3SB4/hmwi2W41muOxMhLMffEclyCSPZjjpDvyhLOuW5nYMe74WZUKLcijWrMQyXPv6bh2c0CDo8mMZ+r/ST88zOy/6x3w5w5G/YwuuyiHYYD3WN29/xxZYpNoO227GMLBm+Hw3g0vv+2KGjwHDb4H7CBYExM4Yeo8OGl5/6B03Y+jThkP2hg83U0v/1pDgwJHEhj0YwhCGMIQhDGEIQxjCEIYwhCEMYQhDGMIQhjCEIQxhCEMYwhCGMIQhDGEIQxjCEIYwhCEMYQhDGMIQhjBMYhhYb5Ha0PR7XpaLt8u13Hf/lb1//avs7GLpv69PsEw2tI/w6Xq00D7CoWWENnAfw/37AQAAAAAAAAAAAAAAAAAAAAAAgCPz1A9wZeaiYXz0u9juSiwItq1NiasFwVaLKVGZoNjlPB26kkKWnAvRlK2hzPnGGp3LrWEhuNZTK4qdYfcxDAywg+2hJ1vDjqM0OKDF7lSXnaEscsWtGLXJ92fziJfM1LJSjk9Baqeqw3ku4jX7NqsbLmPUeVMfTzr5D3pkWtnuvn/IAAAAAElFTkSuQmCC" width=auto height=auto style="max-width:100px; max-height:100px;">
      <span>%s</span>
    </td>
    <td class="message">%s</td>
    <td class="clickstatus"><b>%s</b><br>%s<br>%s</td>
    <td class="useragent">%s</td>
  </tr>
  <tr>
    <td class="profiles">
      <a href="%s">
      <img src="data:image/png;base64,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" width=auto height=auto style="max-width:100px; max-height:100px;">
      <span>%s</span>
    </td>
    <td class="message">%s</td>
    <td class="clickstatus"><b>%s</b><br>%s<br>%s</td>
    <td class="useragent">%s</td>
  </tr>
  <tr>
    <td class="profiles">
      <a href="%s">
      <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAOEAAADhCAMAAAAJbSJIAAAAdVBMVEVMdaP///9Jc6JEcKDv8/dBbp/3+fuKpMH7/P1Cb5/09/pPeKXo7fNlh67s8PVOd6XH0+FwjrJXfqmbsMpeg63e5u47ap3h6PBqirBzkbW0xNegtc3T3OeBnLyYrsiuv9PN2OXCz96Qp8Spu9CDn7+0wtV5l7mlsKRGAAAH0UlEQVR4nO2c65aiOhCFsUIUEbwg3lCkEdv3f8QDOrYtErKDgDNn1fdnZtYak2ySVCqVSiyLYRiGYRiGYRiGYRiGYRiGYRiGYRiGYRiGYRiGYRiGYRiGYRiGYRiG+R9BJMRYFoyFyP8u5c8/Pt20NhBShLvRcZ9EaTr/IU2j7+x4Xkzk+B9XKWej6LDxbHfoDEo4Q3fqrb72W/kPaxQU2cOyshehX+H4w+2kfCKpqfmhGLkaeTfcs4DaocNqOBhoEvrbK4tndgV+oGzdLHsZmQqmF23baBb6YRj6Lzyatg0ntR9cVXJwTg6ee2U4HDpOqdVeFE8UxS6xHixIdZ+f/OxrdWdT4BVMC2zbdvNWOdNDcpmYKwwS3URyk6CqebRdwQIHq129QgoPUDnTo+pzK4GmUlT15fKvPt+gCt1T/UwUc7CgjX68l4veN25fPnMWI7Rle1nbihid0Y7mU1WUfUTKTYOq3+a2TQQxNlaT2lasv0CBg8HRVCHFHlDsNFaWK0KodVHd/KGtjQp0R6YKrQAaZ98zZQOFjxiJyql8Z/yNDlKtyapALnW2tGCzUBcsj4Cxqh7nNyjErXJdOarifaj4ZU0RAVBCXcsEvrAO98aDNC8/QYbIqqaFMtKXUDdKsYlya8a2iVPjT5Gyz+qiRawf6DWWRpyhBhQ4USPPVEZI4YeaBS3Qm8JIaapoAtV/xTa3M9cqQsiS1YyPtX7F+VZXv0PWqxtprd+gZp0ipdd0otRPpETdhRks0K10kAEohMpXjxCZaH+cqWwgbeFZONg33kmvIWM2VxpqudQrVI0AQhzjG16DleJeyw6Zie5FVYM4aX+s9LwBK3XH3GF7KJxgnajaYYuz9rdLResk3oXprLHAwv9GOnGqCreIWPdTR6XQgt0Zr9lKcQdzK1RfkS66Xw4Vmx6JG9J9kxjNAzFC/G/VTp0WWoXVv6QQ7sK06UpxJ0iRauZhZTXk636o+DYCqrXAU5o5FHFCvqZzqlaoXVDtSjsoLuha2GhPUSKAtuqryk5sqhAbOAXzBlHEMlgn5vO9SmHQSCFYZY63fb8LLWsGRSzdyk5spJCg8McV7FRAhzgj5nSQrltTCC/2UcMtRRmJfdIKo6YfpRXOAi1Qf23Vjr7Cy4fq27wu+3pLU6EQ8xRz7JoomCFYXNZ53Qjp10PvJeA61nvrN4bHtvQVnQht9qcv41Tf+15c6gcKwKXQid51Zn7XSljEZF6uU++XvhyoyBQTODj4bZ6R0w6a/O6yVKl+91RWKE+Q4YbOVo0UzvThiGt7F8/jVH+8U1JIPngu5xxbznKgHVZz9BwfHmv3QF6pK1JMYL4Stp3Hga7Cz59WP6mebCnRHjyJOaxbT1RBPSn3aZyutQcXTz4NdqKXM23RjP4g9pgJODxF6bUG6ncUA/ZH3ZqThOZQAFYf/WryQr9HyB6NnaRYDU6mPrR8B9ABHziP+CByBPk4XVujxxRvxy0UEJoWYZ/uEiXg7W3ukbI1uqNYteeOliViMf7Cm75JpC1iOP54CWvUjNrt7AkrgYO07umWEgcNO3sn8v8boEPUUR4DtAIaH3KS7cwKltg+b3UJwhjOKpl3mnxLIzg1YhNlKRpssdMvPMBdHbZsDYOD9Y44d5yRSjF+ptcJaXdW5g8TbI/RFXaTjAszjDIr26cjZ+aJMZLn1BUNMy7MIOuDxmYedi+w8KbxHJC2qc3yaw+D4+e2+e5HoWXBpwptozilbB3yYc+mZdw+LE0BlALeCdE7WRcmTPDs65Z5I3PGCDBA3AWLfiSShW5XW8frS2KYfkhhvpvsR6K4fGzd70siHcETlH9YYvophS0kCWEKLfj2Vuuo0z3blRh8yp4Oai8ItIg8fU6ic+pDIVn4bYHWGS6Nb1Q2kYjdTusGd99DRCP33j4YtXH3fewWafTB6OJw34dC9Ny0G449PK9Ba+iCmxZn+Pq4xN8iEc7wqWOVXeJk00DjqI91kd43qGkohZCTyHxSD0fvJepjCrE06RoON7tPYmRumqd97PrJf0+ie89kJrqYh/E2ffiob0p83M8jWpj34qH705o3nRvnd+IB+eY7665SM54lzpqfZsyfUuFEaG5ukqbP0xhJtNKm62LJMxG++eHWqZenimTW7NjNKSePjM/GBQ1bTaZVQfLYKDi1eYnUk/kR5VcvRzZEcZMjm6/X05ZJZuzsdptk85DoR+Z+eMWrEXj60A9v3rLENc5GxuH+7wpDSOZZLWkP3tutbWgG5Q+Vt9VpYjrglRd125e4vpjtEaqv0hPyLMoTaV/nw/mCFmQmGhW31Y0lmr+E1RwS2wSOFivvcgvseZwfFBeKu9JIuwRsn+oud5GcZObsGr+E9a7GxRIyFq83ux5l+KmBwAYvYb0JURgDy+OhJr2CAoM4V7vXoDDyFWpyntcbHc1VbDwg299qUUJIeUlWtiqQZmeaYBmtT1PAMA8P217ctuo2kpTBZZ+uNp5XPFb5YOrNd/rbS9I6Hjz3j0rnyvDK9VHOohxvM48//pptrlIG/i4+j34Rh1i7BG1PSVo8QBxF30mSZFm2z1kej6ec0Xk3kR8aoWWoeBn6F7gnSfdHpK8PSefkf/wqp8tGMwzDMAzDMAzDMAzDMAzDMAzDMAzDMAzDMAzDMAzDMAzDMAzDMAzDMA34D2r1gCeezgwCAAAAAElFTkSuQmCC" width=auto height=auto style="max-width:100px; max-height:100px;">
      <span>%s</span>
    </td>
    <td class="message">%s</td>
    <td class="clickstatus"><b>%s</b><br>%s<br>%s</td>
    <td class="useragent">%s</td>
  </tr>
</tbody>
        """ % (person.full_name,person.facebook,person.facebook,person.facebookfinalphishingmessage,person.facebookclicked,person.facebookclickedip,person.facebookclickedtime,person.facebookclickeduseragent,person.linkedin,person.linkedin,person.linkedinfinalphishingmessage,person.linkedinclicked,person.linkedinclickedip,person.linkedinclickedtime,person.linkedinclickeduseragent,person.twitter,person.twitter,person.twitterfinalphishingmessage,person.twitterclicked,person.twitterclickedip,person.twitterclickedtime,person.twitterclickeduseragent,person.vkontakte,person.vkontakte,person.vkontaktefinalphishingmessage,person.vkontakteclicked,person.vkontakteclickedip,person.vkontakteclickedtime,person.vkontakteclickeduseragent)

        filewriterhtml.write(html)
        # [MORE_SOCIAL_MEDIA_SITES_TAG]
    # Add body close for html report here
    filewriterhtml.write("</table>")
    filewriter.close()
    filewriterhtml.close()
    #print(t)
    print("")
    print("Phishing Who Clicked Results can also be found in: " + outputfilename)
    print("")
    print("A HTML report is also available: " + outputhtmlfilename)
    print("")

print("Task Duration: " + str(datetime.now() - startTime))
