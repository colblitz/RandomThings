import platform
import time
from selenium import webdriver
from random import randint

system = platform.system()
chromepath = ""
if system == "Linux":
	chromepath = 'chromedrivers/chromedriver_linux64'
elif system == "Darwin":
	chromepath = 'chromedrivers/chromedriver_mac64'
elif system == "Windows":
	chromepath = 'chromedrivers/chromedriver.exe'

print chromepath

timeToWait = 5

def vote():
	try:
		global timeToWait
		chrome_options = webdriver.ChromeOptions()
		chrome_options.add_argument("--incognito")
		chrome_options.add_argument("--headless")

		browser = webdriver.Chrome(chromepath, chrome_options=chrome_options)
		browser.get("https://www.10best.com/awards/travel/best-escape-room/boxaroo-boston/")
		button = browser.find_element_by_css_selector('#awardVoteErrors a')
		button.click()

		time.sleep(timeToWait)

		if browser.current_url != "https://www.10best.com/awards/travel/best-escape-room/boxaroo-boston/share/":
			timeToWait = timeToWait - 0.1
		elif timeToWait < 5.0:
			timeToWait = timeToWait + 0.1

		browser.quit();
	except Exception as e:
	    print("Error: " + str(e))

while True:
	print "starting batch"
	for x in xrange(randint(0, 100)):
		print x
		vote()
		s = randint(0, 200 - x)
		print "sleeping ", s
		time.sleep(s)
