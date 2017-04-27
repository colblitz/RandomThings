import praw
import prawcore
import time
import csv
import sys

import config as Config

REDDITUSERAGENT    = Config.redditUserAgent
REDDITAPPID        = Config.redditAppId
REDDITAPPSECRET    = Config.redditAppSecret
REDDITUSERNAME     = Config.redditUsername
REDDITPASSWORD     = Config.redditPassword

print "Start of script"

reddit = praw.Reddit(
	user_agent=REDDITUSERAGENT,
	client_id=REDDITAPPID,
	client_secret=REDDITAPPSECRET,
	username=REDDITUSERNAME,
	password=REDDITPASSWORD)
subreddit = reddit.subreddit('dataisbeautiful')

submissions = []

# Get last timestamp gotten
try:
	csvfile = open('submissions.csv', 'r')
	for line in csvfile:
		pass
	last = line
	lastTimestamp = int(last.split(',')[1])
except:
	lastTimestamp = int(time.time())

csvfile = open('submissions.csv', 'ab+')
filewriter = csv.writer(csvfile, delimiter=',', quotechar='`', quoting=csv.QUOTE_MINIMAL)

def getBatch(start, end):
	print("Getting batch from " + str(start) + " to " + str(end) + " .... "),
	sys.stdout.flush()
	n = 0
	retry = True
	while retry:
		try:
			for submission in subreddit.submissions(start, end):
				filewriter.writerow([submission.id, int(submission.created_utc), submission.link_flair_text, submission.author, submission.score, submission.title.encode('utf-8')])
				n += 1
			retry = False
		except prawcore.exceptions.ServerError as e:
			# Wait a minute
			print("."),
			sys.stdout.flush()
			time.sleep(60)
	print "Got " + str(n) + " in batch"
	return n

PERIOD = 604800 # Week
currentEnd = lastTimestamp - 1
currentStart = currentEnd - PERIOD
# Subreddit is 5 years old - 2011-01-01 = 1293840000
STARTOFSUBREDDIT = 1293840000

print "Start getting submissions"
# while currentStart > int(time.time()) - 4*PERIOD:
while currentStart > STARTOFSUBREDDIT:
	n = getBatch(currentStart, currentEnd)
	if n == 0:
		PERIOD = PERIOD * 2
	currentStart -= PERIOD
	currentEnd -= PERIOD

csvfile.close()

print "Done with script"