from PIL import Image
import json

import base64
import zlib

import math
import numpy as np

import datetime

################################################################################
###   Blueprint Stuff  #########################################################
################################################################################

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

################################################################################
###   Ellipse Generation   #####################################################
################################################################################

memoizedDistances = {}
hits = 0

directionMap = {
	"u": 0,
	"r": 2,
	"d": 4,
	"l": 6
}

chunkSizeX = 200
chunkSizeY = 100

def getSemiMinor(semiMajor, eccentricity):
	return int(math.sqrt( (1 - eccentricity**2) * semiMajor**2 ))

def getFocus(semiMajor, semiMinor):
	return int(math.sqrt(semiMajor**2 - semiMinor**2))

def getOptions(x, y):
	return [(x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)]

def outside(x, y, a, b):
	# checking the equation of
	# ellipse with the given point
	p = ((math.pow(x, 2) // math.pow(a, 2)) +
		 (math.pow(y, 2) // math.pow(b, 2)))
	return p > 1

# https://wet-robots.ghost.io/simple-method-for-distance-to-ellipse/
def solve(semi_major, semi_minor, p):
	px = abs(p[0])
	py = abs(p[1])

	t = math.pi / 4 if outside(px, py, semi_major, semi_minor) else math.atan2(py, px)

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
	focus = getFocus(semiMajor, semiMinor)

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

	points.add((-focus, 0))
	directions[(-focus, 0)] = "u"

	points.add((-focus-1, 1))
	directions[(-focus-1, 1)] = "l"

	dPoints = [(p[0]+focus, p[1]) for p in points]
	dDirections = {}
	for p in directions:
		dDirections[(p[0]+focus, p[1])] = directions[p]

	return dPoints, dDirections

def printPoints(semiMajor, points, directions):
	a = [[" " for x in xrange(semiMajor*2+1)] for y in xrange(semiMajor*2+1)]
	for p in points:
		a[p[1] + semiMajor][p[0] + semiMajor] = directions[p]

	for x in a:
		print " ".join(x)

def getCircleWithRadius(r):
	return getEllipse(r, 0)

def getChunkedPoints(ox, oy, points, directions):
	chunkedPoints = {}
	for p in points:
		d = directions[p]
		x = p[0]
		y = p[1]

		dx = x + ox
		dy = y + oy

		cx = dx - (dx % chunkSizeX) + chunkSizeX/2
		cy = dy - (dy % chunkSizeY) + chunkSizeY/2
		ck = (cx, cy)

		bpx = dx % chunkSizeX - chunkSizeX/2
		bpy = dy % chunkSizeY - chunkSizeY/2
		if ck not in chunkedPoints:
			chunkedPoints[ck] = []
		chunkedPoints[ck].append((bpx, bpy, d))

		# cx = x / chunkSizeX
		# cy = y / chunkSizeY
		# ck = (cx, cy)

		# mx = x % chunkSizeX
		# my = y % chunkSizeY
		# if ck not in chunkedPoints:
		# 	chunkedPoints[ck] = []
		# chunkedPoints[ck].append((mx, my, d))
	# {
	# 	chunk : [(1, 2, 3), (4, 5, 6), ...],
	# 	chunk : [(1, 2, 3), (4, 5, 6), ...],
	# }
	return chunkedPoints

def zeroTo360PiAtan(y, x):
	r = math.atan2(y, x)
	dr = r if r > 0 else (2*math.pi + r)
	return dr * (180 / math.pi)

BATCH_FOR_BOOK = 50
def partitionChunkedPoints(ox, oy, chunkedPoints):
	allChunks = []
	for c in chunkedPoints:
		allChunks.append(c)
	sortedChunks = sorted(allChunks, key=lambda p: zeroTo360PiAtan(p[1] - oy, p[0] - ox))

	# [[chunk, chunk], [chunk, chunk], ... ]
	partitions = [sortedChunks[i:i + BATCH_FOR_BOOK] for i in xrange(0, len(sortedChunks), BATCH_FOR_BOOK)]

	allps = []
	for p in partitions:
		# p = [chunk, chunk, ...]
		newp = {}
		for c in p:
			newp[c] = chunkedPoints[c]
		allps.append(newp)
	# [ { chunk: [], chunk: [] }, { chunk: [], chunk: [] }, ... ]
	return allps

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

def createBlueprintBookFromChunkedPoints(ox, oy, name, chunkedPoints):
	s = len(chunkedPoints)
	i = 0
	blueprints = []
	for ck in sorted(chunkedPoints, key=lambda p: zeroTo360PiAtan(p[1] - oy, p[0] - ox)):
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
	bpbook["blueprint_book"]["label"] = name
	bpbook["blueprint_book"]["active_index"] = 0
	return bpbook



################################################################################
###   Generate Solar System   ##################################################
################################################################################

sunx = -752
suny = 6383

def generateBlueprint(name, semiMajor, eccentricity, inner, outer):
	t1 = datetime.datetime.now()
	points, directions = getEllipse(semiMajor, eccentricity, inner, outer)
	print "got points"
	numPoints = len(points)
	t2 = datetime.datetime.now()
	cp = getChunkedPoints(sunx, suny, points, directions)
	print "chunked points"
	points = []
	directions = {}
	t3 = datetime.datetime.now()
	numChunks = len(cp)
	partitions = partitionChunkedPoints(sunx, suny, cp)
	print "partitioned chunks"
	cp = {}
	books = []

	# [ { chunk: [], chunk: [] }, { chunk: [], chunk: [] }, ... ]
	i = 0
	for p in partitions:
		bookname = "{} - {:05d}".format(name, i)
		i += 1
		bpbook = createBlueprintBookFromChunkedPoints(sunx, suny, bookname, p)
		bps = jsTobps(jTojs(bpbook))
		books.append(bps)
	partitions = []

	t4 = datetime.datetime.now()
	# bps = jsTobps(jTojs(bpbook))

	semiMinor = getSemiMinor(semiMajor, eccentricity)
	focus = getFocus(semiMajor, semiMinor)
	print "Times (ms) for ellipse {}, {}, {}".format(semiMajor, semiMinor, focus)
	print "  - generate ellipse : {}".format(int((t2 - t1).total_seconds() * 1000))
	print "  - chunk ellipse    : {}".format(int((t3 - t2).total_seconds() * 1000))
	print "  - generate bp book : {}".format(int((t4 - t3).total_seconds() * 1000))
	print "  - points: {}".format(numPoints)
	print "  - chunks: {}".format(numChunks)
	print "  - bpbook: {}".format(len(books))
	print "  - bpbook: {}".format(map(len, books))

	i = 0
	for bp in books:
		filename = "{} - {:05d}.txt".format(name, i)
		i += 1
		with open(filename, 'w') as file:
			file.write(bp)
	print "Total files: {}".format(i)
		# print bp


# generateBlueprint(20, 0.5, 1, 1)
# generateBlueprint("00 - Test", 100, 0.5, 1, 1)
# generateBlueprint("01 - Mercury",   1170, 0.206, 4, 5)
# generateBlueprint("02 - Venus  ",   2160, 0.007, 4, 5)
# generateBlueprint("03 - Earth  ",   3000, 0.017, 4, 5)
# generateBlueprint("04 - Mars   ",   4560, 0.093, 4, 5)
# generateBlueprint("05 - Jupiter",  15600, 0.048, 4, 5)
# generateBlueprint("06 - Saturn ",  28620, 0.054, 4, 5)
# generateBlueprint("07 - Uranus ",  57660, 0.047, 4, 5)
# generateBlueprint("08 - Neptune",  90180, 0.009, 4, 5)
# generateBlueprint("09 - Pluto  ", 118440, 0.2488, 4, 5)

print "********************************************************************"
print "hits: "
print hits
print len(memoizedDistances)
print "********************************************************************"
# print len(a)

################################################################################
###   Image Stuff   ############################################################
################################################################################

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

	for r in a:
		print r

# testjs = json.loads(decodeFromBlueprintString(test))
# for e in testjs["blueprint"]["entities"]:
# 	# print e["position"]
# 	e["position"]["y"] += 5
# 	e["position"]["x"] += 5

# newbp = encodeToBlueprintString(json.dumps(testjs, separators=(',',':')))
# print newbp

# j = b[1:].decode("base64").decode("zlib")

# image = Image.open("factorio_test.png")
# pixels = list(image.getdata())
# print pixels[:10]

# # t = lambda x: 1 if x == [255, 255, 255]
# t = lambda x: 1 if x > 0 else 0

# def t(x):
# 	# print x.shape
# 	return 1 if x > 0 else 0


# from scipy.misc import imread
# im = imread("factorio_test.png")
# print im[0][0]
# print im[0][1]
# print im[0][2]
# print im[1][0]
# print im[2][0]
# print im.shape

# blah = np.sum(im, axis=(2), keepdims=True)
# blah2 = np.array([t(x) for x in blah.ravel()])
# print blah.shape
# print blah2.shape
# blah2 = blah2.reshape(blah.shape)
# print blah2.shape
