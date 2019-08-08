# Social Attacker
![alt text](https://img.shields.io/badge/Python-3_only-blue.svg "Python 3 only")
![alt text](https://img.shields.io/travis/Greenwolf/social_attacker.svg "Travis build status")

A Social Media Phishing Tool by Jacob Wilkin ([Greenwolf](https://github.com/Greenwolf)).

Social Attacker is the first Open Source, Multi-Site, automated Social Media Phishing Framework. It allows you to automate the phishing of Social Media users on a mass scale by handling the connecting to, and messaging of targets. 

You provide Social Attacker with a phishing message and a list of target profiles (collected either by hand or with [Social Mapper](https://github.com/Greenwolf/social_mapper)). Then over a timeframe you set, it attempts to connect to the targets and, if they accept, sends them phishing message. Alternativly it can scrape a targets public profile history and use rudimentary message generation to craft a personal message specific to that person, as an alternative to sending the same phish to all targets.

Social Attacker supports the following social media platforms:

* LinkedIn
* Facebook
* Twitter
* VKontakte

Additional Features Include:

* An organisation's name, searching via LinkedIn
* A folder full of named images
* A CSV file with names and URL’s to images online

Social Attackers usage is similar to [Social Mapper](https://github.com/Greenwolf/social_mapper), so if you are familar with this tool, this should be easy to use.

## Usecases (Why you want to run this)

Social Attacker is primarily aimed at Penetration Testers and Red Teamers, who will use it to perform phishing on targets social media profiles. What you send and do is only limited by your imagination, but here are a few ideas to get started:

* Create a detailed HTML report, showing a breakdown of how your organisations employees react to a random account adding them and sending them a link to click on various social media platforms.
* 'Friend' and Connect to your targets so you can direct message them links to implants or macro documents. Recent statistics show social media users are more than twice as likely to click on links and open documents compared to those delivered via email.
* Create custom phishing campaigns for each social media site. Redirect them to a credential harvesting page with an offical looking login form, or a site under your control hosting an exploitkit or Metasploits browser autopwn.
* Trick users into disclosing their emails and phone numbers with fake vouchers and offers to make the pivot into email phishing, vishing or smishing.

## Getting Started

These instructions will show you the requirements for and how to use Social Attacker.

### Prerequisites

As this is a Python based tool, it should theoretically run on Linux, ChromeOS ([Developer Mode](https://www.chromium.org/chromium-os/developer-information-for-chrome-os-devices/generic)) and macOS. The main requirements are Firefox, Selenium and Geckodriver. To install the tool and set it up follow these 4 steps:

1) Install the latest version of Mozilla Firefox for macOS here:

```
https://www.mozilla.org/en-GB/firefox/new/
```

Or for Debian/Kali (but not required for Ubuntu) get the non-ESR version of Firefox with:
```
sudo add-apt-repository ppa:mozillateam/firefox-next && sudo apt update && sudo apt upgrade
```

Make sure the new version of Firefox is in the path. If not manually add it.

2) Install the Geckodriver for your operating system and make sure it's in your path, on Mac you can place it in `/usr/local/bin`, on ChromeOS you can place it in `/usr/local/bin`, and on Linux you can place it in `/usr/bin`.

Download the latest version of Geckodriver here:

```
https://github.com/mozilla/geckodriver/releases
```

3) Install the required libraries:

On Linux & macOS finish the install with:

```
git clone https://github.com/Greenwolf/social_attacker
cd social_attacker/setup
python -m pip install --no-cache-dir -r requirements.txt
```

On Mac look through the [setup/setup-mac.txt](setup/setup-mac.txt) file to view some additional xquartz installation instructions.

4) Provide Social Attacker with credentials to log into social media services:

```
Open social_attacker.py and enter social media credentials into global variables at the top of the file
```

5) For Facebook, make sure the language of the account which you have provided credentials for is set to 'English (US)' for the duration of the run. Additionally make sure all of your accounts are working, and can be logged into without requiring 2 factor authentication.

## Using Social Attacker

Social Attacker is run from the command-line using a mix of required and optional parameters. You can specify options such as enabling custom phishing message generation (-mm), setting the wait time before phishing after adding, and specifying which sites to target.

### Required Parameters

To start up the tool 4 parameters must be provided, an input format, the input file or folder and the basic running mode:
    
```
-f, --format	: Specify the function to perform 'prepare'(gather LinkedIn connection degrees for a company), 'add'(everyone on list),'check'(who has accepted the request),'generate'(unique phish messages),'phish'(all that have accepted),'addphish'(Add & Phish everyone on list) or 'checkclicks'(to see who has clicked the links)
-i, --input	: The name of the csv file containing links to profiles, must include columns with header titled "Full Name","LinkedIn","Facebook","Twitter","Vkontakte" or the social attacker csv with tracking IDs if using the checklicks option
```

Additionally at least one social media site to check must be selected by including one or more of the following:

```
-a, --all			: Selects all of the options below and phishes on every site that Social Attacker has credentials for
-fb, --facebook		: Perform defined function on Facebook
-tw, --twitter		: Perform defined function on Twitter
-li, --linkedin		: Perform defined function on LinkedIn
-vk, --vkontakte	: Perform defined function on VKontakte
```

### Optional Parameters

Additional optional parameters can also be set to add additional customisation to the way Social Mapper runs:

```
-m, --message		: Sets the default message to send to each user as a phish.
-mm, --markovmessage: The phishing link to be appended to the end of a custom message generation attempt
-ml, --markovlength	: The max length of custom message generation, best to keep short and snappy (default 140 chars)
-w, --wait			: Set the time in hours between adding targets and sending them a phishing message when using the 'addphish' function. For example you may want to wait 24 or 48 hours to give targets time to accept connection requests.
-wl, --weblogs		: The web logs generated by sa_server.py (social_attacker_server.log), which can be parsed to extract clicks and user agents. This is needed to generate a final HTML report.
```

### Example Runs

Here are a couple of example runs to get started for differing use cases:

```
Prepare your linkedin account for connecting to a company to help alleviate 3rd degree requirements
python3 social_attacker.py -f prepare -i "https://www.linkedin.com/company/example-company/" -li

Adding/Connecting to Facebook & LinkedIn users
python3 social_attacker.py -f add -i social_mapper_results.csv -fb -li

Checking which Facebook & LinkedIn user have accepted the connection and can be phished
python3 social_attacker.py -f check -i social_mapper_results.csv -fb -li

Phish users with set message. The string [TRACKING_ID] is overwritten for each phish with a unique 5 character HEX string to tracking purposes.
python3 social_attacker.py -f phish -i social_mapper_results.csv -fb -li -m "Hey come download this file https://greenwolf.com/macro.doc?t=[TRACKING_ID]"

Perform adding and phishing in one go, with delay between in hours(48h in this case for 2 days).
python3 social_attacker.py -f addphish -i social_mapper_results.csv -fb -li -w 48 -m "Hey come download this file https://greenwolf.com/macro.doc?t=[TRACKING_ID]"

Generate unique custom markov messages for each user based on timeline/post history (only for users who have accepted add requests). This is output to a csv file for review/editing, Where Markov cant be generated it is displayed with "-", these will be replaced with the set standard message (-m) when phishing later.
python3 social_attacker.py -f generate -i social_mapper_results.csv -fb -li

Same as above but set the max custom message length to 100 characters instead the default 140.
python3 social_attacker.py -f generate -i social_mapper_results.csv -fb -li -ml 100

Phish users by feeding in the csv output from the 'generate' command. Needs a -mm field with the link to be appended to the end of the message, or overwrite another link mid message. Also needs a default message to fall back to.
python3 social_attacker.py -f phish -i social_attacker_markov_results.csv -fb -li -mm "https://greenwolf.com/macro.doc?t=[TRACKING_ID]" -m "Hey come download this file https://greenwolf.com/macro.doc?t=[TRACKING_ID]"

Perform adding and phish in one go with custom markov messages enabled, no review process here though, enjoyed the twitterese & chaos! 
python3 social_attacker.py -f addphish -i social_mapper_results.csv -fb -li -w 48 -mm "https://greenwolf.com/macro.doc?t=[TRACKING_ID]" -m "Hey come download this file https://greenwolf.com/macro.doc?t=[TRACKING_ID]"

Generate a final phishing html report. This displays has clicked on your links if you instructed social_attacker.py to include a [TRACKING_ID] in your phishing messages. It requires a specfic log output from sa_server.py, so make sure you are writing logs in the same format if you use IIS or Apache etc. Feed in your phishing results and this log file to generate your report. This function has features to discount automated crawlers which will poison your logs.
python3 social_attacker.py -f checkclicks -i social_attacker_phish_results.csv -wl apache-logs.txt

```

### Hosting with sa_server.py

Included with Social Attacker is a lightweight python HTTPS web server, that can be set up with an SSL certificate (see get-a-ssl-certificate.txt). This server is easy to use for a number of reasons, for example; you can place your ssl certificate in the same directory as sa_server.py, and it will over serve items in the web folder. 

You can also force a file to be served using the --file parameter. This is useful if you want to provide your tracking links are part of the path. For example '--file macro.doc' will force clicks from both of these addresses to the macro.doc link. 
https://greenwolf.com/ABCD1 
https://greenwolf.com/ABCD2

```
Server all items in the web folder on port 443
python3 sa_server.py -p 443

Force all visitors to download macro.doc
python3 sa_server.py -p 443 --file macro.doc
```

If you wish to use another server type, but also generate the HTML report, the logs need to be in the following format:
```
IP - datetime timezone - User Agent - Command Path

head -n 5 social_attacker_server.log
10.10.10.10 - 2019-06-18 01:46:29 GMT - User-Agent: curl/7.54.0 - GET /macro.doc
11.11.11.11 - 2019-06-18 02:09:32 GMT - User-Agent: Mozilla/5.0 (Linux; Android 6.0; HTC One M9 Build/MRA58K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.98 Mobile Safari/537.3 - GET /macro.doc
12.12.12.12 - 2019-06-18 02:09:32 GMT - User-Agent: Mozilla/5.0 (Linux; Android 6.0.1; SM-G920V Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.98 Mobile Safari/537.36 - GET /
12.12.12.12 - 2019-06-18 02:09:32 GMT - User-Agent: Mozilla/5.0 (Linux; Android 6.0.1; SM-G920V Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.98 Mobile Safari/537.36 - GET /robots.txt
10.10.10.10 - 2019-06-18 02:09:32 GMT - User-Agent: curl/7.54.0 - GET /macro.doc
```

### Troubleshooting

Social Media sites often change their page formats and class names, if Social Attacker isn't working for you on a specific site, check out the [docs](docs/TroubleShooting_Social_Attacker) section for troubleshooting advice on how to fix it. Please feel free to submit a pull request with your fixes.

## Authors

* [**Jacob Wilkin**](https://github.com/Greenwolf) - *Research and Development* - [Greenwolf Security](https://github.com/Greenwolf)

## Donation
If this tool has been useful for you, feel free to thank me by buying me a coffee :)

[![Coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/Greenwolf)

## Acknowledgments

* Thanks to `[Your Name Could Be Here, Come Help Out!]` for contributions to the project.

![Social Attacker Logo](docs/logo.png?raw=true "Social Attacker Logo")

## Youtube Trailer:

[![Social Attacker Trailer](https://i.imgur.com/s6rPhgK.jpg)](https://youtu.be/-93fTjuW7YI "Social Attacker Trailer")
