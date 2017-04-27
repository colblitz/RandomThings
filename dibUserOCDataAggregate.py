import csv
import math

# submissions by time
# percentage of OC by time
# users OC flair vs account age
# score vs oc

num_submissions_by_time = {}
num_oc_submissions_by_time = {}
score_submissions_by_time = {}
score_oc_submissions_by_time = {}
score_nonoc_submissions_by_time = {}
num_submissions_by_score = {}
num_oc_submissions_by_score = {}
user_oc_scores = {}

WEEK = 604800

def toNearestWeek(t):
	return int(t) / WEEK

def isOC(s):
	return s[2] == 'OC' or '[OC]' in s[5]

def inc(d, k):
	if k not in d:
		d[k] = 0
	d[k] += 1

def add(d, k, v):
	if k not in d:
		d[k] = []
	d[k].append(v)

def processRow(s):
	# 0 - id, 1 - timestamp, 2 - flair, 3 - author, 4 - score, 5 - title
	week = toNearestWeek(s[1])
	score = int(s[4])
	inc(num_submissions_by_time, week)
	inc(num_submissions_by_score, max(0, int(math.log(score + 0.1))))
	add(score_submissions_by_time, week, score)
	if isOC(s):
		inc(num_oc_submissions_by_time, week)
		inc(num_oc_submissions_by_score, max(0, int(math.log(score + 0.1))))
		add(score_oc_submissions_by_time, week, score)
	else:
		add(score_nonoc_submissions_by_time, week, score)

with open('submissions.csv', 'r') as csvfile:
	filereader = csv.reader(csvfile, delimiter=',', quotechar='`', quoting=csv.QUOTE_MINIMAL)
	for row in filereader:
		processRow(row)

average_score_by_time = {}
average_oc_score_by_time = {}
average_nonoc_score_by_time = {}

for week in score_submissions_by_time:
	scores = score_submissions_by_time[week]
	average_score_by_time[week] = sum(scores) / len(scores)

for week in score_oc_submissions_by_time:
	scores = score_oc_submissions_by_time[week]
	average_oc_score_by_time[week] = sum(scores) / len(scores)

for week in score_nonoc_submissions_by_time:
	scores = score_nonoc_submissions_by_time[week]
	average_nonoc_score_by_time[week] = sum(scores) / len(scores)

def median(l):
	l = sorted(l)
	n = len(l)
	m = int(n/2.0)
	if n < 1:
		return None
	if n % 2 == 1:
		return l[m]
	else:
		return (l[m]+l[m-1]) / 2.0

median_score_by_time = {}
median_oc_score_by_time = {}
median_nonoc_score_by_time = {}

for week in score_submissions_by_time:
	scores = score_submissions_by_time[week]
	median_score_by_time[week] = median(scores)

for week in score_oc_submissions_by_time:
	scores = score_oc_submissions_by_time[week]
	median_oc_score_by_time[week] = median(scores)

for week in score_nonoc_submissions_by_time:
	scores = score_nonoc_submissions_by_time[week]
	median_nonoc_score_by_time[week] = median(scores)

def printDict(d):
	for k in sorted(d.keys()):
		print str(k) + ": " + str(d[k])

with open('aggregate.csv', 'w') as csvfile:
	filewriter = csv.writer(csvfile, delimiter=',', quotechar='`', quoting=csv.QUOTE_MINIMAL)
	filewriter.writerow(['Week', '# Posts', '# OC Posts', 'Average Score', 'Average OC Score', 'Average Non OC Score', 'Median Score', 'Median OC Score', 'Median Non OC Score'])
	for week in num_submissions_by_time:
		filewriter.writerow([
			str(week),
			str(num_submissions_by_time.get(week, 0)),
			str(num_oc_submissions_by_time.get(week, 0)),
			str(average_score_by_time.get(week, 0)),
			str(average_oc_score_by_time.get(week, 0)),
			str(average_nonoc_score_by_time.get(week, 0)),
			str(median_score_by_time.get(week, 0)),
			str(median_oc_score_by_time.get(week, 0)),
			str(median_nonoc_score_by_time.get(week, 0)),
		])

printDict(num_submissions_by_score)
printDict(num_oc_submissions_by_score)

print "Aggregate done"

