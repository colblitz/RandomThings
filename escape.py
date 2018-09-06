import platform
from selenium import webdriver

system = platform.system()
chromepath = ""
if system == "Linux":
	chromepath = 'chromedrivers/chromedriver_linux64'
elif system == "Darwin":
	chromepath = 'chromedrivers/chromedriver_mac64'
elif system == "Windows":
	chromepath = 'chromedrivers/chromedriver.exe'

print chromepath

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--headless")

browser = webdriver.Chrome(chromepath, chrome_options=chrome_options)
browser.get("https://www.10best.com/awards/travel/best-escape-room/boxaroo-boston/")
button = browser.find_element_by_css_selector('#awardVoteErrors a')
button.click()

import time
time.sleep(5)

print browser.current_url
# print dir(browser)
browser.quit();