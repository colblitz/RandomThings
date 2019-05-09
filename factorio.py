from PIL import Image
import json

import base64
import zlib

a = "0eNqV2+1qWkEUheF7md8W5lvjrZRSkvRQBHOSRvsRgvfek6SU0k7FBwKijMuZ45t9Nmsvn8PN/uv08Libj2H7HHa39/MhbN8/h8Pu83y9f3nt+PQwhW3YHae7sArz9d3Ls8Pxfp7efb/e78NpFXbzp+lH2KbTh1WY5uPuuJveVF6fPH2cv97dTI/LgtH7V+Hh/rC85X5++bRF5l1dhafloZ9Oq38k8mUS7U2ijSQKSQx3US+TKGck2mUS+YxEv0winZFYXyQRzyhsLlI4t4erixTOXYgURWIIRUpERRlqGJx1qFHkKGOJKhLjkzQ6SRpqdNLIQ421HGW8jY1IjHdxJScZ7iJHkYhDiQQHGW8ig8J4D1Q7h2jlKhLD7yM3OMd4Ex0UxntYy71s+H+aN3IlxhJXchcZSpQo97KxRIK7yFghy61sLCGFc6xQ4Va2KCzNznG3/9Xp/L3T9Vs9WZ9+ay6t1e3jdJzCy0f/Z3m35c2WV1tebHm25YmWR1pt2rZxuyp2ye37NFguJbEbuN3A7QZuN3C7gdsN3G7gdgK3E7idwO0EbidwO4HbCdxO4DYDtxm4zcBtBm4zcJuB2wzcRuA2ArcRuI3AbQRuI3AbgdsI3GrgVgO3GrjVwK0GbjVwq4FbCdxK4FYCtxK4lcCtBG4lcCuBWwzcYuAWA7cYuMXALQZuMXALgVsI3ELgFgK3ELiFwC0EbiFws4GbDdxs4GYDNxu42cDNBm4mcDOBmwncTOBmAjcTuJnAzQRuMnCTgZsM3GTgJgM3GbjJwE0EbiJwE4GbCNxE4CYCNxG4ScCNxG0kbCNRGwnaSMxGQjYSsVGAjcJrFFyj0BoF1iisRkE1CqlWYa3AWn218mrV1Yqr1VYqrVRZqbBSXaWySlWViirVVGtirYe1FtY6WGtgrX+19pW6V2peqXel1pU6V2pcqW+lttV8ArMJzCUwk8A8ArMIzCEgg4D8AbIHyB0gc4C8AbIGyBkwK9acWDNizYc1G9ZcWDNhyYMlC5YcWDJgyX8l+5XcVzJfbdplwy6bddmoyyZdNuiyOReNuWjKRUMumnHRiIsmXDTgovmWBQosT2BxAksTWJjAsgQWJaAkAQUJKEdAMQJKEVCIgDIEFCGwzJZFtiyxZYEty2tZXMvSWhTWoqwWRbUoqUVBLcppUUzrTErrw+rt1xfbP36ssQr765tpv7w2TV+WZ9+mx8Or2LrE1Je/zdXmdPoJRSHzhA=="

b = "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"

# print a[1:].decode("base64").decode("zlib")

# print b[1:].decode("base64").decode("zlib")



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

print blah2[100:200,0:100].tolist()

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