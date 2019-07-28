from PIL import Image
import json

import base64
import zlib

a = "0eNqV2+1qWkEUheF7md8W5lvjrZRSkvRQBHOSRvsRgvfek6SU0k7FBwKijMuZ45t9Nmsvn8PN/uv08Libj2H7HHa39/MhbN8/h8Pu83y9f3nt+PQwhW3YHae7sArz9d3Ls8Pxfp7efb/e78NpFXbzp+lH2KbTh1WY5uPuuJveVF6fPH2cv97dTI/LgtH7V+Hh/rC85X5++bRF5l1dhafloZ9Oq38k8mUS7U2ijSQKSQx3US+TKGck2mUS+YxEv0winZFYXyQRzyhsLlI4t4erixTOXYgURWIIRUpERRlqGJx1qFHkKGOJKhLjkzQ6SRpqdNLIQ421HGW8jY1IjHdxJScZ7iJHkYhDiQQHGW8ig8J4D1Q7h2jlKhLD7yM3OMd4Ex0UxntYy71s+H+aN3IlxhJXchcZSpQo97KxRIK7yFghy61sLCGFc6xQ4Va2KCzNznG3/9Xp/L3T9Vs9WZ9+ay6t1e3jdJzCy0f/Z3m35c2WV1tebHm25YmWR1pt2rZxuyp2ye37NFguJbEbuN3A7QZuN3C7gdsN3G7gdgK3E7idwO0EbidwO4HbCdxO4DYDtxm4zcBtBm4zcJuB2wzcRuA2ArcRuI3AbQRuI3AbgdsI3GrgVgO3GrjVwK0GbjVwq4FbCdxK4FYCtxK4lcCtBG4lcCuBWwzcYuAWA7cYuMXALQZuMXALgVsI3ELgFgK3ELiFwC0EbiFws4GbDdxs4GYDNxu42cDNBm4mcDOBmwncTOBmAjcTuJnAzQRuMnCTgZsM3GTgJgM3GbjJwE0EbiJwE4GbCNxE4CYCNxG4ScCNxG0kbCNRGwnaSMxGQjYSsVGAjcJrFFyj0BoF1iisRkE1CqlWYa3AWn218mrV1Yqr1VYqrVRZqbBSXaWySlWViirVVGtirYe1FtY6WGtgrX+19pW6V2peqXel1pU6V2pcqW+lttV8ArMJzCUwk8A8ArMIzCEgg4D8AbIHyB0gc4C8AbIGyBkwK9acWDNizYc1G9ZcWDNhyYMlC5YcWDJgyX8l+5XcVzJfbdplwy6bddmoyyZdNuiyOReNuWjKRUMumnHRiIsmXDTgovmWBQosT2BxAksTWJjAsgQWJaAkAQUJKEdAMQJKEVCIgDIEFCGwzJZFtiyxZYEty2tZXMvSWhTWoqwWRbUoqUVBLcppUUzrTErrw+rt1xfbP36ssQr765tpv7w2TV+WZ9+mx8Or2LrE1Je/zdXmdPoJRSHzhA=="

b = "0eNqdnOtu4joURt8lv8kovgOvcjQ6CuAykUKSk4TOVBXvfsyt7RQTvJA6GrV8/ezYKzuO93bfs1W9911fNWO2fM+qddsM2fKf92yotk1ZH382vnU+W2bV6HfZLGvK3fG7l3IY87Evm6Fr+zFf+XrMDrOsajb+T7YUh9lDh3IY/G5VV80235XrX1Xjc/nFQh5+zjLfjNVY+XOPTt+8/dvsdyvfhzY+nLqq8/nY5tu+3Teb0ELXDuHX2ubY9p+T8i1b5jaYb6rer88f6WMfv3nKD8+d31T7Xe7rIO+rdd61tb911lfniJf68KrLwff5uO97P9565OaHOdvoHyZmpOmFRl3M31NXNaFPY/jgxkRdOhMzsR8mw9iGCftd1nXkitzZQsYsHLJQMYt5moWdsFikWZgJC1GkeagpD5Hmoac8ZJqHmPJQaR5yykNP39r3aI1SIkxShybHNg3WySlOg3VyduaTIfN2iBdnM/F3sJIx68VT1kWsm7Igt2XcQsDuuOQrlRJaz9Otv5C/Xw1jeZJG7sBrkC7iQVpq2EV7GcnHzyTzlPP3i49af94idbuthjE86Na/fGikDL/16vOub1+rTewpcQkFcRLcU2CKqNdz9080qMgFgTzaHVWQB0fcQjw1n/LxdCr5lHMCKEqR51T8sjV5XEbnT5l7uHbhifOAVzHRtbu3QehpX24jC79iopef9Hf7XXfvcSHjcUTNE5eN9hKQxB2f5x4O0WeYLp7yiq4g9Tf6h66uxug6NL9eoXrMp5bJrtfVtk5wVfe46P1/+/B/rAExMY76qXGMvxR8eyqE9wHfn98L7rmd76xvb0Fh4K5vZ023P77D3TZlcVPy0nHclKNNPbiodj/ea2pOm3pwUdemwmvrWNWXd9abKFRcX9G+3ObN5qUKsfDYyXt6DfUK6iXUC6YvmBy6w87DsYFDD2fWMrlLlC8+tzyA3DC5ZnLF5JLJBZIXSM28WcfZqLAhZ/PJYEkl8fIqBuWWyQ2TayZXTC6ZXCB5gdTMm3WcjQobcjafDJZUEh0D1zFwHQPXMXAdA9cxcB0D1yFwHQLXIXAdAtchcB0C1yFwHQLXMnAtA9cycC0D1zJwLQPXMnAtAtcicC0C1yJwLQLXInAtAtcicA0D1zBwDQPXMHANA9cwcA0D1yBwDQLXIHANAtcgcA0C1yBwDQJXM3A1A1czcDUDVzNwNQNXM3A1AlcjcDUCVyNwNQJXI3A1Alc/Ae48UX3Jti6YHLo7JrdMbphcM7licsnkAskLpGberONsVNiQs/lksDASUzGXDHPJMJcMc8kwlwxzyTCXDHOJMJcIc4kwlwhziTCXCHOJMJcIc4kwFwxzwTAXMIsCkygwhwJTKDCDwhIoLH/C0icse8KSJyx3wlInCHNBMC8Q5QWCnGUKb/OE67ZZ9370E2qF1BL1RBB1QcTIGXVaEbEmYjSLCBDEXiLWLHiz2M1Ct0BYC4Q1i9ssbKOojYI2itkoZKOIjQI2itcoXKNozZbebOXNFt5s3c2W3WzVzRbdaM2NltxoxY0W3Gi9jZbbaLWNFttorc02Tm73TaZi5O22SYJao54opJZILYi6IGLkjDqNxgMNtSFiS8SIvUSs2aa6RlhrhDXbUWcb6mw/nW2no910tJmO9tLRVjraSUcb6WgfHW2jo110luRkOU6W4mQZTpbgZPlNlt5E2U2U3ES5TZTaRJlNlNhEeU2U1jQEa1Z0wmpOWMkJqzhhBSes3oSVm6BqE1RsgmpNUKkJqjRBhSaozgSVmViCNSsCZDWArASQVQCyAkBW/8fK/1D1Hyr+Q7V/qPQPVf6hwj9U94fK/hzBmhVls5psVpLNKrJZQTarx2bl2KgaGxVjo1psVIqNKrFRITaqw0Zl2HOC9QJhzc7IsCMy7IQMOyDDzsew4zHodAw6HIPOxqCjMehkDDoYg87FoGMxi/tY/5yd/1DO8stf5pmFz1e+Pv1pDf9y/Pf79BU+ePX9cPJ1qhA2fM0X88Phf/h+AM0="

# print a[1:].decode("base64").decode("zlib")

# print b[1:].decode("base64").decode("zlib")

test = "0eNqdmP1q4zAQxF+l6G8b9G3Hr1LK4bS6qyBRjK2UhpB3Pyc52lyrtjOGQLCT/VnanZG0Por1Zh+GMaYsuqOIj7s0ie7+KKb4J/Wb8718GILoRMxhKyqR+u35Ko99mobdmOt12GRxqkRMT+FVdOpUFYJf4pj38523+Os/ankTqanI9ibSUJHuJtKeHioRUo45huu8LxeHX2m/XYdxns5XM67EsJvmsF06P3JG1a4Sh/nLz/SnOIbH62+XWX2AahrqTgWMwTEGHpvFoRaGOhyqYKjHoRqGNjAUH2gLMyXMXMFMvPRKwlA8oQp30JvW/4PaElSzUA9AcT/hyleW9roteV05mmOKHE/72wCpe7fN737KNWpIBN1yaImTV6yIAKiWLNQCUH4X0qXia37jUUWOoUWkgFnyW48GqG6ZNJEBexKt8FE3i1SPDLplBYpAaSsBOTCSVassnpJo8xQ1bzSrTiBvhjaSBKDvPgqvwximqca28w8D9iW2IwuNJMGTTCQHDVv04oJpWhZT3HTNiq6I+kf7+bwuF7KLE7aKpplvaHohzfysRGsWqhzYxK0lFYkwWecAK6T1rDyLZ0tLm6XYjtqWXcwcUOYV2+QCUCfZ1hGBKrbJRaCa7B0RpiF7XIRpydYRYTqyx0WYnuzxEGZDOhthsqe0T13EQ3V9Y9fdvOCrxKafIWfoc5zu5k9/d3lKJV7COF0iGyNV47TVel4r/gK447WR"

testbook = "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"

def blueprintStringToJsonString(s):
	return s[1:].decode("base64").decode("zlib")

def jsonStringToBlueprintString(js):
	return "0" + js.encode("zlib").encode("base64").replace("\n","")

def jsonStringToJson(js):
	return json.loads(js)

def jsonToJsonString(j):
	return json.dumps(j, separators=(',',':'))

def bpsTojs(s):
	return blueprintStringToJsonString(s)

def jsTobps(js):
	return jsonStringToBlueprintString(js)

def jsToj(js):
	return jsonStringToJson(js)

def jTojs(j):
	return jsonToJsonString(j)

class Icon:
	def __init__(self, types, name):
		self.types = types
		self.name = name

	def toJs(self, index):
		j = {}
		j["index"] = index + 1
		j["signal"] = {}
		j["signal"]["type"] = self.types
		j["signal"]["name"] = self.name
		return j

class Entity:
	def __init__(self, name, x, y, direction):
		self.name = name
		self.x = x
		self.y = y
		self.direction = direction

	def toJs(self, index):
		j = {}
		j["entity_number"] = index + 1
		j["name"] = self.name
		j["position"] = {}
		j["position"]["x"] = self.x
		j["position"]["y"] = self.y
		if self.direction:
			j["direction"] = self.direction
		return j

# class Blueprint:
# 	def __init__(self):

# print bpsTojs(testbook)


print "---------------------------------------------------"

import math


# e = math.sqrt(1 - minor^2 / major^2)
# e^2 = 1 - minor^2/major^2

# 1 - e^2 = minor^2 / major^2
# (1 - e^2) * major^2 = minor^2
# minor = math.sqrt( (1-e^2) * major^2)

def getSemiMinor(semiMajor, eccentricity):
	return int(math.sqrt( (1 - eccentricity**2) * semiMajor**2 ))

print "_---------------------------------"
print getSemiMinor(1170, 0.206)
print getSemiMinor(1170, 0.001)
print getSemiMinor(1170, 0.999)

def getOptions(x, y):
	return [(x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)]

def outside(x, y, a, b):
	# checking the equation of
	# ellipse with the given point
	p = ((math.pow(x, 2) // math.pow(a, 2)) +
		 (math.pow(y, 2) // math.pow(b, 2)))
	return p > 1

def solve(semi_major, semi_minor, p):
	px = abs(p[0])
	py = abs(p[1])

	t = math.pi / 4 if outside(px, py, semi_major, semi_minor) else math.atan2(px, py)

	a = semi_major
	b = semi_minor

	for x in range(0, 3):
		x = a * math.cos(t)
		y = b * math.sin(t)

		ex = (a*a - b*b) * math.cos(t)**3 / a
		ey = (b*b - a*a) * math.sin(t)**3 / b

		rx = x - ex
		ry = y - ey

		qx = px - ex
		qy = py - ey

		r = math.hypot(ry, rx)
		q = math.hypot(qy, qx)

		delta_c = r * math.asin((rx*qy - ry*qx)/(r*q))
		delta_t = delta_c / math.sqrt(a*a + b*b - x*x - y*y)

		t += delta_t
		t = min(math.pi/2, max(0, t))

	return (math.copysign(x, p[0]), math.copysign(y, p[1]))

memoizedDistances = {}
hits = 0

def getDistance(semiMajor, semiMinor, point):
	global hits
	k = (semiMajor, semiMinor, point)
	if k in memoizedDistances:
		hits += 1
		return memoizedDistances[k]
	closest = solve(semiMajor, semiMinor, point)
	d = math.hypot(point[0] - closest[0], point[1] - closest[1])
	memoizedDistances[k] = d
	return d

def addLayer(semiMajor, semiMinor, x, y, points, directions):
	newpoints = set()
	newpoints.add((x, y))
	last = (x, y)
	cx = x
	cy = y
	while True:
		options = [p for p in getOptions(cx, cy) if p != last and p not in points]
		if last in options: options.remove(last)
		closest = min(options, key=lambda x: getDistance(semiMajor, semiMinor, x))

		direction = "d"
		if closest[0] > cx:
			direction = "r"
		elif closest[0] == cx and closest[1] < cy:
			direction = "u"
		elif closest[0] < cx:
			direction = "l"

		directions[(cx, cy)] = direction

		if closest in newpoints:
			break
		newpoints.add(closest)
		last = (cx, cy)
		cx, cy = closest
	return newpoints

def getEllipse(semiMajor, eccentricity, inner = 0, outer = 0):
	semiMinor = getSemiMinor(semiMajor, eccentricity)

	directions = {}
	points = set()

	x = semiMajor
	y = 0
	newpoints = addLayer(semiMajor, semiMinor, x, y, set(), directions)
	points.update(newpoints)

	# TODO: Too many layers create pinches that become deadends
	for i in xrange(1, inner+1):
		x = semiMajor - i
		y = 0
		newpoints = addLayer(semiMajor, semiMinor, x, y, points, directions)

		points.update(newpoints)

	for i in xrange(1, outer+1):
		x = semiMajor + i
		y = 0
		newpoints = addLayer(semiMajor, semiMinor, x, y, points, directions)
		points.update(newpoints)

	return points, directions

def printPoints(semiMajor, points, directions):
	a = [[" " for x in xrange(semiMajor*2+1)] for y in xrange(semiMajor*2+1)]
	for p in points:
		a[p[1] + semiMajor][p[0] + semiMajor] = directions[p]

	for x in a:
		print " ".join(x)

def getCircleWithRadius(r):
	return getEllipse(r, 0)

directionMap = {
	"u": 0,
	"r": 2,
	"d": 4,
	"l": 6
}

# points, directions = getCircleWithRadius(25)
# printPoints(25, points, directions)

# points, directions = getEllipse(25, 0.5)
# printPoints(25, points, directions)

# points, directions = getEllipse(35, 0.5, 3)
# printPoints(35, points, directions)



chunkSize = 32
def getChunkedPoints(points, directions):
	chunkedPoints = {}
	for p in points:
		d = directions[p]
		x = p[0]
		y = p[1]
		cx = x / chunkSize
		cy = y / chunkSize
		ck = (cx, cy)

		mx = x % chunkSize
		my = y % chunkSize
		if ck not in chunkedPoints:
			chunkedPoints[ck] = []
		chunkedPoints[ck].append((mx, my, d))
	return chunkedPoints

def createBPFromChunk(ck, chunk):
	bp = {}
	bp["blueprint"] = {}
	bp["blueprint"]["item"] = "blueprint"
	bp["blueprint"]["label"] = str(ck)
	# bp["blueprint"]["version"] = "blueprint"
	icons = []
	icons.append(Icon("item", "transport-belt"))
	for i in xrange(len(icons)):
		icons[i] = icons[i].toJs(i)
	entities = []

	n = "transport-belt"

	for p in chunk:
		entities.append(Entity(n, p[0], p[1], directionMap[p[2]]))

	for i in xrange(len(entities)):
		entities[i] = entities[i].toJs(i)

	bp["blueprint"]["icons"] = icons
	bp["blueprint"]["entities"] = entities
	return bp

def createBlueprintBookFromChunkedPoints(chunkedPoints):
	s = len(chunkedPoints)
	i = 0
	blueprints = []
	for ck in sorted(chunkedPoints):
		cpoints = chunkedPoints[ck]
		# print ck
		# print cpoints

		bp = createBPFromChunk(ck, cpoints)
		bp["index"] = i
		i += 1
		blueprints.append(bp)
	bpbook = {}
	bpbook["blueprint_book"] = {}
	bpbook["blueprint_book"]["blueprints"] = blueprints
	bpbook["blueprint_book"]["item"] = "blueprint-book"
	bpbook["blueprint_book"]["label"] = "asdf"
	bpbook["blueprint_book"]["active_index"] = 0
	return bpbook

points, directions = getEllipse(20, 0.7, 1, 1)
printPoints(24, points, directions)

cp = getChunkedPoints(points, directions)

bpbook = createBlueprintBookFromChunkedPoints(cp)
print bpbook
bps = jsTobps(jTojs(bpbook))

print "********************************************************************"
print "********************************************************************"
print "********************************************************************"
print bps
print "********************************************************************"
print "********************************************************************"
print "********************************************************************"



# x = sorted(steps, key=lambda key: steps[key])
# 	# print jTojs(bp)
# 	bps = jsTobps(jTojs(bp))

chunkSize = 32


# for c in chunkedPoints:
# 	cpoints = chunkedPoints[c]
# 	t = [[" " for x in xrange(chunkSize)] for y in xrange(chunkSize)]
# 	for p in cpoints:
# 		t[p[1]][p[0]] = p[2]

# 	for x in t:
# 		print " ".join(x)
# 	print "--------------------"


# points, directions = getEllipse(38, 0.5, 0, 0)
# printPoints(40, points, directions)

bp = {}
bp["blueprint"] = {}
bp["blueprint"]["item"] = "blueprint"
bp["blueprint"]["label"] = "test"
# bp["blueprint"]["version"] = "blueprint"
icons = []
icons.append(Icon("item", "transport-belt"))
for i in xrange(len(icons)):
	icons[i] = icons[i].toJs(i)
entities = []

n = "transport-belt"

for p in points:
	entities.append(Entity(n, p[0], p[1], directionMap[directions[p]]))

for i in xrange(len(entities)):
	entities[i] = entities[i].toJs(i)
bp["blueprint"]["icons"] = icons
bp["blueprint"]["entities"] = entities

# print jTojs(bp)
bps = jsTobps(jTojs(bp))
print "********************************************************************"
print bps
print "********************************************************************"
print "hits: "
print hits
print len(memoizedDistances)
print "********************************************************************"
# r = 25
# def circle(x, y):
# 	return x*x + y*y - r*r
# def distance(x, y):
# 	return abs(math.sqrt(x*x + y*y) - r)


# x = 0
# y = 0
# points = set()

# def getStartingPoint():
# 	x = 0
# 	y = 0
# 	found = False
# 	distance = abs(circle(x, y))
# 	while not found:
# 		x += 1
# 		newd = abs(circle(x, y))
# 		if newd < distance:
# 			distance = newd
# 		else:
# 			found = True
# 			x -= 1
# 	return x, y

# x, y = getStartingPoint()

# print x, y

# def getOptions(x, y):
# 	return [(x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)]

# directions = {}
# points.add((x, y))

# last = (x, y)
# cx = x
# cy = y
# while True:
# 	options = getOptions(cx, cy)
# 	if last in options: options.remove(last)
# 	closest = min(options, key=lambda x: distance(*x))
# 	# print closest
# 	direction = "d"
# 	if closest[0] > cx:
# 		direction = "r"
# 	elif closest[0] == cx and closest[1] < cy:
# 		direction = "u"
# 	elif closest[0] < cx:
# 		direction = "l"

# 	directions[(cx, cy)] = direction

# 	if closest in points:
# 		break
# 	points.add(closest)
# 	last = (cx, cy)
# 	cx, cy = closest


# a = [[" " for x in xrange(r*2+1)] for y in xrange(r*2+1)]
# newpoints = set()
# for p in points:
# 	a[p[1] + r][p[0] + r] = directions[p]

# for x in a:
# 	print " ".join(x)




print "---------------------------------------------------"




def decodeFromBlueprintString(s):
	return s[1:].decode("base64").decode("zlib")

def encodeToBlueprintString(js):
	return "0" + js.encode("zlib").encode("base64").replace("\n","")

# def cycle(s):
# 	return encodeToBlueprintString(decodeFromBlueprintString(s))

def toGrid(js):
	j = json.loads(js)
	b = j["blueprint"]
	entities = b["entities"]
	maxn = 0
	maxx = 0
	maxy = 0
	minx = 0
	miny = 0
	for e in entities:
		p = e["position"]
		n = e["name"]
		maxn = max(maxn, len(n))
		maxx = max(maxx, p["x"])
		maxy = max(maxy, p["y"])
		minx = min(minx, p["x"])
		miny = min(miny, p["y"])
	tiles = b["tiles"]
	for t in tiles:
		p = t["position"]
		n = t["name"]
		maxn = max(maxn, len(n))
		maxx = max(maxx, p["x"])
		maxy = max(maxy, p["y"])
		minx = min(minx, p["x"])
		miny = min(miny, p["y"])
	print maxx, maxy, minx, miny
	width = maxx - minx
	height = maxy - miny
	a = [["" for x in xrange(width)] for y in xrange(height)]

	for e in entities:
		p = e["position"]
		x = p["x"] + minx
		y = p["y"] + miny
		print x,y
		a[y][x] = e["name"]

		# n = e["name"]
		# maxn = max(maxn, len(n))
		# maxx = max(maxx, p["x"])
		# maxy = max(maxy, p["y"])
		# minx = min(minx, p["x"])
		# miny = min(miny, p["y"])

	for r in a:
		print r

testjs = json.loads(decodeFromBlueprintString(test))
for e in testjs["blueprint"]["entities"]:
	# print e["position"]
	e["position"]["y"] += 5
	e["position"]["x"] += 5

newbp = encodeToBlueprintString(json.dumps(testjs, separators=(',',':')))
print newbp





import numpy as np



j = b[1:].decode("base64").decode("zlib")


image = Image.open("factorio_test.png")
pixels = list(image.getdata())
print pixels[:10]

# t = lambda x: 1 if x == [255, 255, 255]
t = lambda x: 1 if x > 0 else 0

def t(x):
	# print x.shape
	return 1 if x > 0 else 0


from scipy.misc import imread
im = imread("factorio_test.png")
print im[0][0]
print im[0][1]
print im[0][2]
print im[1][0]
print im[2][0]
print im.shape


blah = np.sum(im, axis=(2), keepdims=True)
blah2 = np.array([t(x) for x in blah.ravel()])
print blah.shape
print blah2.shape
blah2 = blah2.reshape(blah.shape)
print blah2.shape

# print blah2[100:200,0:100].tolist()

# print blah[100:200,0:100].tolist()
# np.apply_over_axes(np.sum, a, [0,2])

# print t(im[0][0])
# print t(im[0][1])
# print t(im[0][2])
# print t(im[1][0])
# print t(im[2][0])
# blah = t(im)
# print blah.shape


# toGrid(decodeFromBlueprintString(b))

# print b
# test = encodeToBlueprintString(j)
# print len(test)
# print test.replace("\n", "")


# test = b
# print "0:"
# print test
# test = cycle(test)
# print "1:"
# print test
# test = cycle(test)
# print "2:"
# print test
# test = cycle(test)
# print "3:"
# print test
# test = cycle(test)
# print "4:"
# print test
# test = cycle(test)
# print "5:"
# print test
# test = cycle(test)
# print "6:"
# print test



# test = b[1:]

# print test
# print "-----------"
# # print test.decode("base64").decode("zlib")
# print "-----------"
# print test.decode("base64").decode("zlib").encode("zlib").encode("base64")
# print "-----------"
# print test.decode("base64").decode("zlib").encode("zlib").encode("base64").decode("base64").decode("zlib")