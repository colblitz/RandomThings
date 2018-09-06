import random

def attempt():
	picked = dict((v, 0) for v in range(140))
	for x in xrange(70):
		for i in random.sample(range(140), 15):
			picked[i] += 1
	return summary(picked)

def summary(d):
	n = {}
	for i in d:
		times = d[i]
		n[times] = n.get(times, 0) + 1
	return n

a = {}
for x in xrange(100000):
	r = attempt()
	for i in r:
		a[i] = a.get(i, 0) + r[i]
for x in a:
	a[x] = a[x] / 100000.0

print a