import urllib
import urllib2
import time
from bs4 import BeautifulSoup

urllib.URLopener.version = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'

base = "https://onlinemanga.xyz/half+%26+half+%28seo+kouji%29+manga/1851/chapters?page="

opener = urllib2.build_opener()
opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36')]

def getFilename(url):
	return url.split('/')[-1].split('#')[0].split('?')[0]


# https://fs.onlinemanga.xyz/files/full/manga_animelove_3/1851/chapters/64309/1346166.jpg
# https://fs.onlinemanga.xyz/files/full/manga_animelove_3/1851/chapters/64309/1346167.jpg
# https://fs.onlinemanga.xyz/files/full/manga_animelove_3/1851/chapters/64309/1346168.jpg
# https://fs.onlinemanga.xyz/files/full/manga_animelove_3/1851/chapters/64309/1346169.jpg
# https://fs.onlinemanga.xyz/files/full/manga_animelove_3/1851/chapters/64309/1346170.jpg
# https://fs.onlinemanga.xyz/files/full/manga_animelove_3/1851/chapters/64309/1346171.jpg

def getImage(cn, i, url):
	print "   " + str(i)
	filename = "halfandhalf/halfandhalf-{:02d}-{:03d}.jpg".format(cn, i)
	
	testfile = urllib.URLopener()
	testfile.retrieve(url, filename)
	time.sleep(0.1)

def getImageLinksFromChapter(cn, chapterUrl):
	print "getting chapter " + str(cn)
	cSoup = BeautifulSoup(opener.open(chapterUrl), "html.parser")
	# print cSoup
	i = 0
	for a in cSoup.find_all('a', attrs={"data-ngthumb": True}):
		imgLink = a.get('href')
		getImage(cn, i, imgLink)
		i += 1

for i in range(1, 14):
	chapterUrl = base + str(i)
	getImageLinksFromChapter(i, chapterUrl)
	



# "https://fs.onlinemanga.xyz/files/full/manga_animelove_3/1851/chapters/64304/1345996.jpg"



# series = []

# def processDirectory(url):
# 	series = []
# 	dSoup = BeautifulSoup(opener.open(url), "html.parser")
# 	for link in dSoup.find_all('a'):
# 		try:
# 			url = link['href']
# 		except:
# 			continue
# 		if "reader/series" in url:
# 			series.append(url)
# 	return series

# def processSeries(url):
# 	chapters = []
# 	sSoup = BeautifulSoup(opener.open(url), "html.parser")
# 	for link in sSoup.find_all('a'):
# 		try:
# 			url = link['href']
# 		except:
# 			continue
# 		if "reader/read" in url:
# 			chapters.append(url)
# 	return chapters


# for directory in directories:
# 	dSoup = BeautifulSoup(opener.open(directory), "html.parser")
# 	for link in dSoup.find_all('a'):
# 		try:
# 			url = link['href']
# 		except:
# 			continue
# 		if "reader/series" in url:
# 			series.append(url)
# 		# if link.parent.name != 'div':
# 		# 	print "skipping", link, link.parent
# 		# print link

# def convertChapterToZip(src):
# 	return '/'.join(src.split('/')[:-1]) + "%5BYoManga%5D"

# series = list(set(series))
# for s in series:
# 	print s
# 	chapters = []
# 	sSoup = BeautifulSoup(opener.open(s), "html.parser")
# 	for link in sSoup.find_all('a'):
# 		try:
# 			url = link['href']
# 		except:
# 			continue
# 		if "reader/read" in url:
# 			chapters.append(url)


# 	for c in list(set(chapters)):
# 		print c
# 		cSoup = BeautifulSoup(opener.open(c), "html.parser")

# 		print cSoup.find('img', class_='open')['src']

# 		https://yomanga.co/reader/content/comics/narakarana_57fee5e8a3db0/2_0__58016a762c932/00.jpg
# 		https://yomanga.co/reader/content/comics/narakarana_57fee5e8a3db0/11_0__581a5acbdb52a/%5BYoManga%5DNarakarana_c11.zip

# 		break
# 	break

	# https://yomanga.co/reader/read/cohabitation/en/0/51/page/1


# fp = webdriver.FirefoxProfile('/home/colblitz/.mozilla/firefox/a4h19pj2.test')
# fp.set_preference("browser.download.dir", "/home/colblitz/Dropbox/yomanga")
# fp.set_preference("browser.download.manager.showWhenStarting", False)
# fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream");

# browser = webdriver.Firefox(firefox_profile=fp)

# for s in series:
# 	print s
# 	browser.get(s)
# 	# you can use your url here
# 	for i, downloadButton in enumerate(browser.find_elements_by_class_name("fa-download")):
# 		print i
# 		downloadButton.click()
# 		time.sleep(5)

# 	break
# browser.close();



# mainPageUrl = "http://leagueoflegends.wikia.com/wiki/League_of_Legends_Wiki"
# mainPage = urllib2.urlopen(mainPageUrl)

# mainPageSoup = BeautifulSoup(mainPage, "html.parser")

# baseUrl = "http://leagueoflegends.wikia.com"

# csvfile = open('skins.csv', 'wb')
# csvwriter = csv.writer(csvfile, delimiter='\t', quotechar='\'', quoting=csv.QUOTE_MINIMAL)

# def nsToS(ns):
# 	return unicode(ns).encode('ascii','replace')

# def getSkinsFromGallery(gallery, champName, typeName):
# 	for skin in gallery.find_all('div', class_="lightbox-caption"):
# 		name = nsToS(skin.contents[0]).strip()
# 		rp = 0
# 		date = ""
# 		r = skin.find('div', style="float:right")
# 		if r.span:
# 			if r.span.a.next_sibling:
# 				rp = int(unicode(r.span.a.next_sibling))
# 			else:
# 				rp = int(unicode(r.span.previous_sibling))
# 			date = nsToS(r.span.next_sibling)[3:]
# 		else:
# 			date = nsToS(r.string).split("/")[-1].replace('?','')
# 		# print champName, name, str(rp), date, typeName
# 		csvwriter.writerow([champName, name, str(rp), date, typeName])


# def getChampSkins(champSkinsSoup, champName):
# 	for span in champSkinsSoup.findAll('span'):
# 		if span.parent.name == 'h2':
# 			if span.string in ['Available', 'Legacy', 'Limited Edition']:
# 				typeString = nsToS(span.string)
# 				getSkinsFromGallery(span.parent.next_sibling.next_sibling, champName, typeString)
# 			elif span.string not in ['Screenshots', 'References', 'Chroma Packs']:
# 				print span.string

# for tag in mainPageSoup.find("ol", class_="champion_roster").find_all('a'):
# 	champName = tag['href'].split('/')[2].encode('ascii','replace').strip()
# 	champSkinsUrl = baseUrl + tag['href'] + "/Skins"
# 	champSkinsSoup = BeautifulSoup(urllib2.urlopen(champSkinsUrl), "html.parser")
# 	getChampSkins(champSkinsSoup, champName)

# csvfile.close()
# print "done"