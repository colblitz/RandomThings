import os
from PIL import Image
import re

base = "runway-de-waratte"
imageBase = base + "/" + base + "-{:03d}-{:03d}.jpg"

def fixDir(filename):
    dirPath = os.path.join(base, filename)
    m = re.findall(r"\d+$", filename)
    cNumber = int(m[0])
    print cNumber
    allfiles = os.listdir(dirPath)
    if len(allfiles) == 0:
        os.rmdir(dirPath)
        return
    
    for image in os.listdir(dirPath):
        imagePath = os.path.join(dirPath, image)
        if "Store" in image:
            continue
        if image.endswith(".webp"):
            newPath = os.path.splitext(imagePath)[0]+'.jpg'
            print imagePath, newPath
            im = Image.open(imagePath).convert("RGB")
            im.save(newPath, "jpeg")
        m = re.findall(r"\d+$", os.path.splitext(image)[0])
        iNumber = int(m[0])
        newName = imageBase.format(cNumber, iNumber)
        os.rename(imagePath, newName)
            
            

for filename in os.listdir(base):
    if os.path.isdir(os.path.join(base, filename)):
        fixDir(filename)


##import urllib2
##from bs4 import BeautifulSoup
##import urllib
##
##opener = urllib2.build_opener()
##opener.addheaders = [('User-Agent', "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36")]
##
##opener = urllib.request.build_opener()
##
##soup = BeautifulSoup(opener.open("https://w11.mangafreak.net/Manga/Runway_De_Waratte"), "html.parser")
##
##downloadLinks = soup.find("div", {"class": "manga_series_list"}).find_all("a", {"download": True})
##for l in downloadLinks:
##    print l.get("href"), l.get("download")

##
##
##import urllib
##import os
##import re
##
##urllib.URLopener.version = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"
##opener = urllib.URLopener()
##
##links = ["http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_1"]
##
##seriesDir = "runway-de-waratte"
##path = seriesDir + "/" + seriesDir + "-{:03d}.zip"
##if not os.path.exists(seriesDir):
##    print "Making series dir"
##    os.mkdir(seriesDir)
##
##for l in links:
##
##    m = re.findall(r"\d+$", l)
##    n = int(m[0])
##    f = path.format(n)
##    print l, f
##    opener.retrieve(l, f)
##
##links = [
##    "http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_1",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_2",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_3",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_4",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_5",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_6",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_7",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_8",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_9",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_10",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_11",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_12",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_13",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_14",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_15",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_16",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_17",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_18",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_19",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_20",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_21",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_22",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_23",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_24",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_25",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_26",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_27",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_28",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_29",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_30",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_31",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_32",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_33",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_34",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_35",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_36",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_37",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_38",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_39",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_40",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_41",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_42",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_43",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_44",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_45",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_46",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_47",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_48",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_49",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_50",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_51",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_52",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_53",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_54",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_55",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_56",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_57",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_58",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_59",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_60",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_61",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_62",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_63",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_64",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_65",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_66",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_67",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_68",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_69",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_70",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_71",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_72",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_73",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_74",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_75",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_76",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_77",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_78",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_79",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_80",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_81",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_82",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_83",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_84",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_85",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_86",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_87",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_88",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_89",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_90",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_91",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_92",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_93",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_94",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_95",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_96",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_97",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_98",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_99",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_100",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_101",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_102",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_103",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_104",
##"http://images.mangafreak.net:8080/downloads/Runway_De_Waratte_105"]
##
##
##
##import urllib
##import time
##import re
##import os
##
##urllib.URLopener.version = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"
####imageOpener = urllib.URLopener()
##imageOpener.retrieve(img_link, iFilename)
##opener = urllib2.build_opener()
##opener.addheaders = [('User-Agent', "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36")]
##
##seriesDir = "runway-de-waratte"
##imagePath = seriesDir + "/" + seriesDir + "-{:03d}-{:03d}.jpg"
##
##if not os.path.exists(seriesDir):
##    print "Making series dir"
##    os.mkdir(seriesDir)
##
##imageOpener = urllib.URLopener()
##imageOpener.retrieve(img_link, iFilename)
##def downloadChapter(cSoup):
##    cLink = cSoup.find("a").get("href")
##    m = re.findall(r"\d+$", cLink)
##    cNumber = int(m[0])
##
##    print "Getting chapter", cNumber, cLink
##
##    soup = BeautifulSoup(opener.open(cLink), "html.parser")
##    img_list = soup.find(
##        "div", {"class": "vung-doc", "id": "vungdoc"}
##    )
##
##    for img in img_list.find_all("img"):
##        img_link = img.get("src")
##        img_title = img.get("title", "").strip(" - Mangakakalot.com")
##        
##        m2 = re.findall(r"\d+$", img_title)
##        iNumber = int(m2[0])
##        iFilename = imagePath.format(cNumber, iNumber)
##        imageOpener.retrieve(img_link, iFilename)
##        time.sleep(0.1)
##
##        print iNumber, img_link, iFilename
##    
##
##def downloadSeries(url):
##    soup = BeautifulSoup(opener.open(url), "html.parser")
##   
##    chapter_list = soup.find("div", {"class": "chapter-list"}).find_all(
##        "div", {"class": "row"}
##    )[::-1]
##    for chapter in chapter_list:
##        downloadChapter(chapter)
##        break
##    print "done"
##
##downloadSeries("https://mangakakalot.com/read-cc7sv158504870005")

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
	


