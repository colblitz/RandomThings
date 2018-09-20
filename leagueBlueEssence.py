import random
import numpy

skinEssences = [
	[13, 1280.5],
	[22, 1527.5],
	[24, 1839.5],
	[47, 1969.5],
	[32, 2112.5]
]

skins = {}

i = 1
for tier in skinEssences:
	for r in xrange(tier[0]):
		skins[i] = tier[1]
		i += 1

def getShard():
	return skins[random.randint(1, 138)]

def convertIP(n):
	numShards = n / 1700
	newBE = n % 1700
	for r in xrange(numShards):
		newBE += getShard()
	return newBE

def simulate(n, ip):
	tests = []
	for r in xrange(n):
		tests.append(convertIP(ip))
	return tests

def calculateStats(a):
	arr = numpy.array(a)
	print numpy.mean(arr)
	print numpy.std(arr)

calculateStats(simulate(50000, 111000))