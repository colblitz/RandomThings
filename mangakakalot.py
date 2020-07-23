import urllib
import urllib2
import time
from bs4 import BeautifulSoup
import re
import os

urllib.URLopener.version = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"

opener = urllib2.build_opener()
opener.addheaders = [('User-Agent', "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36")]

seriesDir = "runway-de-waratte"
imagePath = seriesDir + "/" + seriesDir + "-{:03d}-{:03d}.jpg"

if not os.path.exists(seriesDir):
    print "Making series dir"
    os.mkdir(seriesDir)

imageOpener = urllib.URLopener()

def downloadChapter(cSoup):
    cLink = cSoup.find("a").get("href")
    m = re.findall(r"\d+$", cLink)
    cNumber = int(m[0])

    print "Getting chapter", cNumber, cLink

    soup = BeautifulSoup(opener.open(cLink), "html.parser")
    img_list = soup.find(
        "div", {"class": "vung-doc", "id": "vungdoc"}
    )

    for img in img_list.find_all("img"):
        img_link = img.get("src")
        img_title = img.get("title", "").strip(" - Mangakakalot.com")
        
        m2 = re.findall(r"\d+$", img_title)
        iNumber = int(m2[0])
        iFilename = imagePath.format(cNumber, iNumber)
        imageOpener.retrieve(img_link, iFilename)
        time.sleep(0.1)

        print iNumber, img_link, iFilename
    

def downloadSeries(url):
    soup = BeautifulSoup(opener.open(url), "html.parser")
   
    chapter_list = soup.find("div", {"class": "chapter-list"}).find_all(
        "div", {"class": "row"}
    )[::-1]
    for chapter in chapter_list:
        downloadChapter(chapter)
        break
    print "done"

downloadSeries("https://mangakakalot.com/read-cc7sv158504870005")

##
##
##
##def getFilename(url):
##	return url.split('/')[-1].split('#')[0].split('?')[0]
##
##def getImage(cn, i, url):
##	print "   " + str(i)
##	filename = "halfandhalf/halfandhalf-{:02d}-{:03d}.jpg".format(cn, i)
##	
##	testfile = urllib.URLopener()
##	testfile.retrieve(url, filename)
##	time.sleep(0.1)
##
##def getImageLinksFromChapter(cn, chapterUrl):
##	print "getting chapter " + str(cn)
##	cSoup = BeautifulSoup(opener.open(chapterUrl), "html.parser")
##	# print cSoup
##	i = 0
##	for a in cSoup.find_all('a', attrs={"data-ngthumb": True}):
##		imgLink = a.get('href')
##		getImage(cn, i, imgLink)
##		i += 1
##
##for i in range(1, 14):
##	chapterUrl = base + str(i)
##	getImageLinksFromChapter(i, chapterUrl)
	


