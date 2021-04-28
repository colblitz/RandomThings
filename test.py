# try:
# 	from urllib.parse import urlparse
# except ImportError:
# 	from urlparse import urlparse


# import praw
# from pprint import pprint

# import config as Config

# REDDITUSERAGENT = Config.redditUserAgent
# REDDITAPPID     = Config.redditAppId
# REDDITAPPSECRET = Config.redditAppSecret
# REDDITUSERNAME  = Config.redditUsername
# REDDITPASSWORD  = Config.redditPassword
# IMGURCLIENTID   = Config.imgurClientId

# reddit = praw.Reddit(
# 	user_agent=REDDITUSERAGENT,
# 	client_id=REDDITAPPID,
# 	client_secret=REDDITAPPSECRET,
# 	username=REDDITUSERNAME,
# 	password=REDDITPASSWORD)

# i = 0
# saved = reddit.user.me().saved(limit=1000)
# urls = []
# for l in saved:
# 	# print l.id, l.permalink
# 	try:
# 		url = l.url
# 		urls.append(url)
# 	except:
# 		pass
# 	i += 1
# print i

# with open("url.txt", "w") as f:
# 	for u in urls:
# 		f.write(u + "\n")

import praw

import os
import json
import time
import urllib
import requests

import config as Config

REDDITUSERAGENT = Config.redditUserAgent
REDDITAPPID     = Config.redditAppId
REDDITAPPSECRET = Config.redditAppSecret
REDDITUSERNAME  = Config.redditUsername
REDDITPASSWORD  = Config.redditPassword

reddit = praw.Reddit(
	user_agent=REDDITUSERAGENT,
	client_id=REDDITAPPID,
	client_secret=REDDITAPPSECRET,
	username=REDDITUSERNAME,
	password=REDDITPASSWORD)

PROCESS_LOG = "processLog.txt"

urllib.URLopener.version = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
urlRetriever = urllib.URLopener()

if os.path.exists(PROCESS_LOG):
	os.remove(PROCESS_LOG)

def getLastProcessed(subreddit):
	latest = 0
	if os.path.exists(PROCESS_LOG):
		with open(PROCESS_LOG, 'r') as f:
			for line in f:
				parts = line.split(",")
				if subreddit == parts[0]:
					latest = max(latest, parts[1])
	return int(latest)

def updateLastProcessed(subreddit, latestSeen):
	with open(PROCESS_LOG, 'a+') as f:
		f.write("{},{}\n".format(subreddit, latestSeen))

SUBMISSIONS_BASE = "https://api.pushshift.io/reddit/submission/search/"
# SUBMISSIONS_BASE = "https://api.pushshift.io/reddit/search/submission/"
BATCH_SIZE = 500
SCORE_THRESHOLD = 5

def buildSearch(subreddit, fields, after, threshold=SCORE_THRESHOLD):
	return "{}?subreddit={}&score=>{}&size={}&fields={}&after={}".format(SUBMISSIONS_BASE, subreddit, threshold, BATCH_SIZE, ','.join(fields), after)

def downloadSubreddit(info, subreddit, threshold):
	now = int(time.time())
	latestSeen = getLastProcessed(subreddit)
	print "Starting from", latestSeen

	processed = set()
	bi = 0
	while latestSeen <= now:
		print "Starting Batch %03d ------------------------" % bi
		url = buildSearch(subreddit, ['created_utc', 'id', 'author', 'score'], latestSeen, threshold)
		print "Url:", url
		data = json.loads(requests.get(url).text)['data']
		print "Results:", len(data)

		if len(data) == 0:
			print "No more"
			updateLastProcessed(subreddit, latestSeen)
			return

		ids = []
		for s in data:
			date = s['created_utc']
			latestSeen = max(latestSeen, date)

			rid = s['id']
			ids.append(rid)
			score = s['score']
			author = s['author']

			info[rid] = { "id": rid, "date": date, "author": author, "score": score, "updated": False }

			#print rid, score, author

		ids2 = [i if i.startswith('t3_') else 't3_' + i for i in ids]
		print "Getting updated scores for posts"
		nscores = reddit.info(ids2)

		for s in nscores:
			s_info = info[s.id]
			s_info["score"] = s.score
			s_info["updated"] = True
			info[s.id] = s_info

		print "Done with batch"
		bi += 1

	print "Done with batches, last seen:", latestSeen
	updateLastProcessed(subreddit, latestSeen)

print "download subreddit"
info = {}
#downloadSubreddit(info, "dataisbeautiful", 10)

print "--------------------------------"

def getPostRowString(p):
	return "%s, %s, %s, %s, %s\n" % (p["date"], p["id"], p["author"], p["score"], p["updated"])

allposts = sorted(info.items(), key=lambda x: x[1]["date"])
allposts = [i[1] for i in allposts]

print "total posts processed: ", len(allposts)
# with open("postbackup2.txt", "w+") as f:
# 	for p in allposts:
# 		f.write(getPostRowString(p))


userScores = {}
for p in allposts:
	author = p["author"]
	score = p["score"]
	if author in userScores:
		userScores[author] = userScores[author] + score
	else:
		userScores[author] = score
	# print p["id"], p["date"], p["author"], p["score"]

print "--------------------------------"

sortedScores = sorted(userScores.items(), key=lambda x: x[1], reverse=True)

for u in sortedScores[:50]:
	print "% 5d" % u[1], u[0]


# with open("testfile2.txt", "w+") as f:
# 	for u in sortedScores:
# 		f.write("% 6d, %s\n" % (u[1], u[0]))

n = 20
topN = set()
with open("testfile2.txt", "r") as f:
	# skip [deleted]
	deleted = f.readline()
	while len(topN) < n:
		l = f.readline().strip()
		topN.add(l.split(", ")[1])

print "Top %d:" % n
for u in topN:
	print u

totalSoFar = {}
lastPerAuthor = {}
datapoints = []
with open("postbackup2.txt", "r") as f:
	for line in f:
		# 1373986196, 1iez9n, Hwh69, 102, True"
		pieces = line.strip().split(", ")
		timestamp = int(pieces[0])
		author = pieces[2]
		score = int(pieces[3])

		if author in topN:
			if author not in totalSoFar:
				totalSoFar[author] = score
				lastPerAuthor[author] = [timestamp, author, score]
				datapoints.append([timestamp, author, score])
			else:
				totalSoFar[author] = totalSoFar[author] + score
				lastPerAuthor[author] = [timestamp, author, totalSoFar[author]]
				datapoints.append([timestamp, author, totalSoFar[author]])


import csv

fields = ["Timestamp", "Author", "Karma"]

with open("data.csv", "w+") as f:
	csvwriter = csv.writer(f)
	csvwriter.writerow(fields)
	csvwriter.writerows(datapoints)


import pandas as pd
import plotly.express as px
df = pd.read_csv('data.csv')

df['Timestamp'] = df['Timestamp'].apply(lambda x: pd.to_datetime(x, unit='s'))
print df.head()

# >>> df = pd.DataFrame(['05SEP2014:00:00:00.000'],columns=['Mycol'])
# >>> df
#                     Mycol
# 0  05SEP2014:00:00:00.000
# >>> import datetime as dt
# >>> df['Mycol'] = df['Mycol'].apply(lambda x:
#                                     dt.datetime.strptime(x,'%d%b%Y:%H:%M:%S.%f'))
# >>> df
#        Mycol
# 0 2014-09-05



fig = px.line(df, x = 'Timestamp', y = 'Karma', color = "Author")


for author in lastPerAuthor:
	dp = lastPerAuthor[author]
	timestamp = dp[0]
	author = dp[1]
	karma = dp[2]
	atext = "%s: %d" % (author, karma)
	fig.add_annotation(x = pd.to_datetime(timestamp, unit='s'), y = karma, text=atext)

fig.update_annotations(dict(
            xref="x",
            yref="y",
            ax=0,
            ay=-20
))

fig.update_yaxes(nticks=15)
fig.update_layout(yaxis_tickformat = 'd')


fig.update_xaxes(nticks=20)

fig.show()

# import plotly.express as px
# df = px.data.iris()

# print df
# print type(df)

# import plotly.express as px
# df = px.data.gapminder().query("continent == 'Oceania'")
# print df
# fig = px.line(df, x='year', y='pop', color='country')
# fig.show()

# fig = px.scatter(df, x="sepal_width", y="sepal_length", color="species", size='petal_length', hover_data=['petal_width'])
# fig.show()

