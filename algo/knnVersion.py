#!/usr/bin/python

"""
City comparison algorithm
"""

import sys
import numpy as np
from sklearn import neighbors as skln
from math import cos, asin, sqrt

#Implementation of Haversine Formula for distance
#Takes coordinates as input and returns distance across earth's surface in km
def distance(lat1, lng1, lat2, lng2):
    p = 0.017453292519943295     #Pi/180
    a = 0.5 - cos((lat2 - lat1) * p)/2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lng2 - lng1) * p)) / 2
    return 12742 * asin(sqrt(a)) #2*R*asin

#header order:
##lat, lng, avgmaxtmp, avgmintmp, avgtmp, precipitation, population, per_dem, per_gop
cityDict = np.load('cityDict.npy').item()
cityName = raw_input("Enter city (please use full geography): ")
weights = input("Enter list of weights [prox, clim, demog, pol]: ")
#weights = [sqrt(w) for w in weights] #use sqrt of weight for calculation
try:
	input_city = cityDict[cityName]
	print("Raw in: ", input_city)
except KeyError:
	print "City couldn't be found"
	exit(1)

#normalizer
entries = cityDict.values()
maxes = []
mins = []
numCols = len(entries[0]) #length of each entry


nodes = {}
input_lat = input_city[0]
input_lng = input_city[1]
for city in cityDict:
	entry = cityDict[city]
	dis = distance(input_lat, input_lng, entry[0], entry[1])
	nodes[city] = [dis] + entry[2:]
	#climate = [(i * weights[1]) / 4 for i in entry[2:6]] #slice climate data and reduce weight
	#nodes[city] = [dis * weights[0]] + climate + [entry[6] * weights[2]] + [i * weights[3] for i in entry[7:]]
#print nodes

for i in range(len(nodes.values()[0])): #don't normalize lat-long
	mins.append(min(float(node[i]) for node in nodes.values()))
	maxes.append(max(float(node[i]) for node in nodes.values()))
#print mins
#print maxes

for node in nodes.values():
	for i in range(len(nodes.values()[0])):
		val = node[i]
		val = (val - mins[i]) / (maxes[i] - mins[i])
		node[i] = val

#cityDict is now normalized
input_city_node = nodes[cityName]
print("Normalized: ", input_city_node)


for node in nodes.values():
	node = [node[i] - input_city_node[i] for i in range(len(node))]
	#print node
	node[0] = node[0] * weights[0]
	node[1:5] = [node[i] * weights[1] for i in range(1,5)]
	node[5] = node[5] * weights[2]
	node[6:] = [node[i] * weights[3] for i in range(6, len(node))]
	print(node)
tree = skln.KDTree(nodes.values(), leaf_size=2)
dist, ind = tree.query([input_city_node], k=10)
#print dist
#print ind

for near in ind[0]:
	print nodes.keys()[near]

