import urllib
import urllib2
from bs4 import BeautifulSoup
import os
import time

urllib.URLopener.version = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
imageOpener = urllib.URLopener()
opener = urllib2.build_opener()
opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36')]

### Constants to fill in
SERIES_NAME = "kuroha-to-nijisuke"

IMAGE_TEMPLATE = SERIES_NAME + "/" + SERIES_NAME + "-{}-{:03d}.jpg"

if not os.path.exists(SERIES_NAME):
	print "Making series dir"
	os.mkdir(SERIES_NAME)

INDEX_URL = "https://m.mangabat.com/read-js387959"
CHAP_LENGTH = len(INDEX_URL) + 8


def CHAPTER_FIND(soup):
	return [cli.find('a').get("href") for cli in soup.find_all("li", {"class": "a-h"})]

def IMG_FIND(soup):
	images = []
	for img in soup.find("div", {"class": "container-chapter-reader"}).find_all("img"):
		imgsrc = img["src"]
		images.append((imgsrc, IMG_NUM(imgsrc)))
	return images
		#print img
		#print img["src"]
	#return [(img.get("src").strip(), (int(img.get("id")[6:])) + 1) for img in soup.find("div", {"class": "container-chapter-reader"}).find_all("img")]
	#return [(img.get("data-src").strip(), (int(img.get("id")[6:])) + 1) for img in soup.find_all("img", {"class": "wp-manga-chapter-img"})]

#############################
def CHAPTER_NUM(chapterUrl):
	end = chapterUrl[CHAP_LENGTH:]
	try:
		if len(end) > 3:
			if end[0] == "0":
				return "{:03d}".format(int(end[0]))
			return "{:03d}".format(int(end[:3]))
		return "{:03d}".format(int(end))
	except:
		return end

def IMG_NUM(imageUrl):
	return int(imageUrl.split("/")[-1].split(".")[0])


###
def downloadImage(imageUrl, chapterNum, imageNum = None):
	imageNum = imageNum if imageNum else IMG_NUM(imageUrl)
	imageFilename = IMAGE_TEMPLATE.format(chapterNum, imageNum)
	if os.path.exists(imageFilename):
		print "Skipped " + imageFilename
		return
	imageOpener.retrieve(imageUrl, imageFilename)
	print "Saved " + imageUrl + " to " + imageFilename
	time.sleep(0.1)

def downloadChapter(chapterUrl, chapterNum = None):
	print "Downloading chapter " + chapterUrl
	chapterNum = chapterNum if chapterNum else CHAPTER_NUM(chapterUrl)

	if not os.path.exists(SERIES_NAME + "/" + chapterNum):
		print "Making chapter dir: " + SERIES_NAME + "/" + chapterNum
		os.mkdir(SERIES_NAME + "/" + chapterNum)

	print chapterNum, chapterUrl
	soup = BeautifulSoup(opener.open(chapterUrl), "html.parser")
	imgList = []
	try:
		imgList = IMG_FIND(soup)
	except Exception as e:
		print "error finding images"
		print e
	for (imageUrl, imageNum) in imgList:
		downloadImage(imageUrl, chapterNum, imageNum)

def downloadSeries(indexUrl):
	soup = BeautifulSoup(opener.open(indexUrl), "html.parser")

	chapterList = []
	try:
		chapterList = CHAPTER_FIND(soup)
	except Exception as e:
		print "error finding chapters"
		print e

	for chapterUrl in chapterList:
		#print chapterUrl
		downloadChapter(chapterUrl)



downloadSeries(INDEX_URL)
