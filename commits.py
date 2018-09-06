import re
import csv

f = open('log.txt', 'r')

commitMessages = {}
for l in f:
	m = re.match(r"([0-9a-f]{35,40}).*", l)
	if m:
		commitMessages[m.group(1)] = l[40:]

f = open('log2.txt', 'r')

currentCommit = ["", "", "", 0, 0, 0, ""]
allCommits = []

while True:
	l = f.readline()
	if not l: break

	m = re.match(r"([0-9a-f]{35,40}).*", l)
	if m:
		allCommits.append(list(currentCommit))
		p = l.split('\t')
		commit = m.group(1)
		currentCommit[0] = commit
		currentCommit[1] = p[1].strip()
		currentCommit[2] = p[2].strip()
		currentCommit[6] = commitMessages[commit].strip()
	else:
		if "changed" in l or "insertions" in l or "deletions" in l:
			pieces = l.split(",")
			# print l

			c = 0
			i = 0
			d = 0
			for p in pieces:
				n = [int(s) for s in p.split() if s.isdigit()][0]
				if "changed" in p:
					c = n
				elif "insertion" in p:
					i = n
				elif "deletion" in p:
					d = n
			currentCommit[3] = c
			currentCommit[4] = i
			currentCommit[5] = d
			# print c, i, d
		else:
			if re.sub(r'\s+', '', l) is not "":
				print l

allCommits.append(list(currentCommit))

maxC = float(max(allCommits, key=lambda x: x[3])[3])
maxI = float(max(allCommits, key=lambda x: x[4])[4])
maxD = float(max(allCommits, key=lambda x: x[5])[5])

print maxC, maxI, maxD

print "\n"

def getScore(commit):
	c = commit[3]
	i = commit[4]
	d = commit[5]

	pc = float(c) / maxC
	pi = float(i) / maxI
	pd = float(d) / maxD

	return pc + pi + pd

allCommits.sort(key=lambda x: getScore(x), reverse=True)

with open('commits.csv', 'w') as csvfile:
	writer = csv.writer(csvfile, delimiter=",", quoting=csv.QUOTE_MINIMAL)
	writer.writerow(['Hash', 'Author', 'Date', 'Files Changed', 'Insertions', 'Deletions', 'Message'])
	for c in allCommits:
		writer.writerow(c)


