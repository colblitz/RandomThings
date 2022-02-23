import os
import time
import urllib
import shutil
import traceback

from bs4 import BeautifulSoup
from urllib.request import urlopen

SERIES_NAME = "silent-war"

def getRequest(url):
	return urllib.request.Request(
		url, 
		data=None, 
		headers={
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'
		}
	)

def urlRead(url):
	return urlopen(getRequest(url)).read()

def urlDownload(url, filepath):
	if os.path.isfile(filepath):
		print("file exists, skipping")
		return 
	with urllib.request.urlopen(getRequest(url)) as response, open(filepath, 'wb') as out_file:
		shutil.copyfileobj(response, out_file)

# Work
if not os.path.exists(SERIES_NAME):
	print(f"Making series directory: {SERIES_NAME}")
	os.mkdir(SERIES_NAME)

INDEX_URL = "https://adultwebtoon.com/adult-webtoon/my-kingdom-silent-war/"

# https://adultwebtoon.com/adult-webtoon/my-kingdom-silent-war/149/
CHAP_LENGTH = len(INDEX_URL)


def CHAPTER_FIND(soup):
	return [cli.find('a').get("href") for cli in soup.find_all("li", {"class": "wp-manga-chapter"})]


from selenium import webdriver
from selenium.webdriver.firefox.options import Options

def downloadSeries(indexUrl):

	print(f"Starting download of series from index {indexUrl}")
	options = Options()
	options.headless = True
	# firefoxOptions = webdriver.FirefoxOptions()
	# firefoxOptions.set_headless()
	browser = webdriver.Firefox(options = options)
	print("Browser started")
	browser.get(indexUrl)
	print("After get")
	browser.implicitly_wait(10)
	time.sleep(10)
	print("After wait")

	html = browser.page_source

	soup = BeautifulSoup(html, "html.parser")
	#print(html)

	chapterList = []
	try:
		chapterList = CHAPTER_FIND(soup)
	except Exception as e:
		print("Error finding chapters")
		traceback.print_exc()

	print(f"Found {len(chapterList)} chapters")

	for chapterUrl in chapterList:
		print(chapterUrl)
		try:
			downloadChapter(chapterUrl)
		except Exception as e:
			print(f"Error downloading chapter {chapterUrl}")
			traceback.print_exc()


def IMG_NUM(imgid):
	return int(imgid.split("-")[1]) + 1

def IMG_FIND(soup):
	images = []
	for img in soup.find("div", {"class": "reading-content"}).find_all("img"):
		imgsrc = img["src"].strip()
		imgid = img["id"].strip()
		images.append((imgsrc, IMG_NUM(imgid)))
	return images

# https://adultwebtoon.com/adult-webtoon/my-kingdom-silent-war/150/

def CHAPTER_NUM(chapterUrl):
	end = chapterUrl[CHAP_LENGTH:-1]
	try:
		if "-" in end:
			return end
		if len(end) > 3:
			if end[0] == "0":
				return "{:03d}".format(int(end[0]))
			return "{:03d}".format(int(end[:3]))
		return "{:03d}".format(int(end))
	except:
		return end

def downloadChapter(chapterUrl, chapterNum = None):
	print("------------------------------------------------------------")
	print(f"Downloading chapter {chapterUrl}")
	chapterNum = chapterNum if chapterNum else CHAPTER_NUM(chapterUrl)
	print(f"ChapterNum: {chapterNum}")
	if chapterNum < "145":
		return

	chapterDir = SERIES_NAME + "/" + chapterNum
	if not os.path.exists(chapterDir):
		print(f"Making chapter dir: {chapterDir}")
		os.mkdir(chapterDir)

	soup = BeautifulSoup(urlRead(chapterUrl), "html.parser")
	imgList = []
	try:
		imgList = IMG_FIND(soup)
		print(f"Got {len(imgList)} image urls")
	except Exception as e:
		print("Error finding images")
		traceback.print_exc()
	imgIndex = 0
	for (imageUrl, imageNum) in imgList:
		imgIndex += 1
		downloadImage(imageUrl, chapterNum, imgIndex)

IMAGE_TEMPLATE = SERIES_NAME + "/" + SERIES_NAME + "-{}-{:03d}.jpg"

def downloadImage(imageUrl, chapterNum, imgIndex):
	imageNum = imgIndex if imgIndex != None else IMG_NUM(imageUrl)
	imageFilepath = IMAGE_TEMPLATE.format(chapterNum, imageNum)
	if os.path.exists(imageFilepath):
		print(f"Skipped {imageFilepath}")
		return
	urlDownload(imageUrl, imageFilepath)
	print(f"Saved {imageUrl} to {imageFilepath}")
	time.sleep(0.05)




# import urllib
# import urllib2
# from bs4 import BeautifulSoup
# import os
# import time

# urllib.URLopener.version = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
# imageOpener = urllib.URLopener()
# opener = urllib2.build_opener()
# opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36')]

# ### Constants to fill in
# SERIES_NAME = "kuroha-to-nijisuke"

# IMAGE_TEMPLATE = SERIES_NAME + "/" + SERIES_NAME + "-{}-{:03d}.jpg"

# if not os.path.exists(SERIES_NAME):
# 	print "Making series dir"
# 	os.mkdir(SERIES_NAME)

# INDEX_URL = "https://m.mangabat.com/read-js387959"
# CHAP_LENGTH = len(INDEX_URL) + 8


# def CHAPTER_FIND(soup):
# 	return [cli.find('a').get("href") for cli in soup.find_all("li", {"class": "a-h"})]

# def IMG_FIND(soup):
# 	images = []
# 	for img in soup.find("div", {"class": "container-chapter-reader"}).find_all("img"):
# 		imgsrc = img["src"]
# 		images.append((imgsrc, IMG_NUM(imgsrc)))
# 	return images
# 		#print img
# 		#print img["src"]
# 	#return [(img.get("src").strip(), (int(img.get("id")[6:])) + 1) for img in soup.find("div", {"class": "container-chapter-reader"}).find_all("img")]
# 	#return [(img.get("data-src").strip(), (int(img.get("id")[6:])) + 1) for img in soup.find_all("img", {"class": "wp-manga-chapter-img"})]

# #############################
# def CHAPTER_NUM(chapterUrl):
# 	end = chapterUrl[CHAP_LENGTH:]
# 	try:
# 		if len(end) > 3:
# 			if end[0] == "0":
# 				return "{:03d}".format(int(end[0]))
# 			return "{:03d}".format(int(end[:3]))
# 		return "{:03d}".format(int(end))
# 	except:
# 		return end

# def IMG_NUM(imageUrl):
# 	return int(imageUrl.split("/")[-1].split(".")[0])


# ###
# def downloadImage(imageUrl, chapterNum, imageNum = None):
# 	imageNum = imageNum if imageNum else IMG_NUM(imageUrl)
# 	imageFilename = IMAGE_TEMPLATE.format(chapterNum, imageNum)
# 	if os.path.exists(imageFilename):
# 		print "Skipped " + imageFilename
# 		return
# 	imageOpener.retrieve(imageUrl, imageFilename)
# 	print "Saved " + imageUrl + " to " + imageFilename
# 	time.sleep(0.1)

# def downloadChapter(chapterUrl, chapterNum = None):
# 	print "Downloading chapter " + chapterUrl
# 	chapterNum = chapterNum if chapterNum else CHAPTER_NUM(chapterUrl)

# 	if not os.path.exists(SERIES_NAME + "/" + chapterNum):
# 		print "Making chapter dir: " + SERIES_NAME + "/" + chapterNum
# 		os.mkdir(SERIES_NAME + "/" + chapterNum)

# 	print chapterNum, chapterUrl
# 	soup = BeautifulSoup(opener.open(chapterUrl), "html.parser")
# 	imgList = []
# 	try:
# 		imgList = IMG_FIND(soup)
# 	except Exception as e:
# 		print "error finding images"
# 		print e
# 	for (imageUrl, imageNum) in imgList:
# 		downloadImage(imageUrl, chapterNum, imageNum)

# def downloadSeries(indexUrl):
# 	soup = BeautifulSoup(opener.open(indexUrl), "html.parser")

# 	chapterList = []
# 	try:
# 		chapterList = CHAPTER_FIND(soup)
# 	except Exception as e:
# 		print "error finding chapters"
# 		print e

# 	for chapterUrl in chapterList:
# 		#print chapterUrl
# 		downloadChapter(chapterUrl)



downloadSeries(INDEX_URL)
