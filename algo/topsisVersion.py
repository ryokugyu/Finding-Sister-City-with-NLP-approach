#!/usr/bin/python

"""
City comparison algorithm
"""

import sys
import numpy as np
from skcriteria import Data, MIN, MAX
from skcriteria.madm import closeness
from math import cos, asin, sqrt

#Implementation of Haversine Formula for distance
#Takes coordinates as input and returns distance across earth's surface in km
def distance(lat1, lng1, lat2, lng2):
    p = 0.017453292519943295     #Pi/180
    a = 0.5 - cos((lat2 - lat1) * p)/2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lng2 - lng1) * p)) / 2
    return 12742 * asin(sqrt(a)) #2*R*asin


def normalize_weights(weights):
   max_min = [MIN if weight >= 0 else MAX for weight in weights]
   abs_weights = [abs(weight) for weight in weights]
   total = sum(abs_weights)
   normalized_weights = [float(weight) / total for weight in abs_weights]
   return (max_min, normalized_weights)

#header order:
##lat, lng, avgmaxtmp, avgmintmp, avgtmp, precipitation, population, per_dem, per_gop
cityDict = np.load('cityDict.npy').item()
cityName = raw_input("Enter city (please use full geography): ")
weights = input("Enter list of weights [prox, clim, demog, pol]: ")

try:
	input_city = cityDict[cityName]
	print("Raw in: ", input_city)
except KeyError:
	print "City couldn't be found"
	exit(1)

#normalizer
maxes = []
mins = []

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

for i in range(len(nodes.values()[0])): #don't normalize lat-long, use nodes
	mins.append(min(float(node[i]) for node in nodes.values()))
	maxes.append(max(float(node[i]) for node in nodes.values()))
#print mins
#print maxes

for node in nodes.values():
	for i in range(len(nodes.values()[0])):
		val = node[i]
		val = (val - mins[i]) / (maxes[i] - mins[i])
		node[i] = val

#cities now normalized
input_city_node = list(nodes[cityName])
print("Normalized: ", input_city_node)


for node in nodes.values():
	node = [abs(node[i] - input_city_node[i]) for i in range(len(node))]

x = normalize_weights(weights)
criteria = x[0]
weights = x[1]
print criteria
print weights
criteria_8 = [criteria[0], criteria[1], criteria[1], criteria[1], criteria[1], criteria[2], criteria[3], criteria[3]]
weights_8 = [weights[0], weights[1] / 4, weights[1] / 4, weights[1] / 4, weights[1] / 4, weights[2], weights[3] / 2, weights[3] / 2]


data = Data(nodes.values(), criteria_8, anames=nodes.keys(), weights=weights_8)
print "normalized weights: " + str(data.weights)
print data.criteria
weights_8 = [abs(weight) for weight in weights_8]
dm = closeness.TOPSIS()
dec = dm.decide(data)
print dec.e_.ideal
for i in dec.rank_[:10]:
	print(nodes.keys()[i])


