import praw

import config as Config

REDDITUSERAGENT    = Config.redditUserAgent
REDDITAPPID        = Config.redditAppId
REDDITAPPSECRET    = Config.redditAppSecret
REDDITUSERNAME     = Config.redditUsername
REDDITPASSWORD     = Config.redditPassword

reddit = praw.Reddit(
	user_agent=REDDITUSERAGENT,
	client_id=REDDITAPPID,
	client_secret=REDDITAPPSECRET,
	username=REDDITUSERNAME,
	password=REDDITPASSWORD)

# https://www.reddit.com/r/dataisbeautiful/wiki/flair#wiki_oc_flair

# submissions by time
# percentage of OC by time
# users OC flair vs account age
# score vs oc

print "getting submissions"
subreddit = reddit.subreddit('politics')
for submission in subreddit.submissions(1478592000, 1478678400):
    print(submission.title)

# subreddit = reddit.subreddit('dataisbeautiful')

# for submission in subreddit.submissions(1478592000, 1478678400):
	# print str(submission)
print "done"
# for comment in reddit.redditor('OC-Bot').comments.new()

