#!/usr/bin/python

"""
Creates numpy dictionary for faster testing; this
is a placeholder until the database is constructed
"""

import csv
import numpy as np
import sys

cityDict = {}
with open('city_with_data.csv') as city_csv:
	reader = csv.DictReader(city_csv)

	#lat, lng, avgmaxtmp, avgmintmp, avgtmp, precipitation, population, per_dem, per_gop
	header_names = reader.fieldnames
	for row in reader:
		raw_in = [row[header] for header in header_names]
		raw_in = raw_in[4:]
		try:
		    cols = [float(i) for i in raw_in]
		except:
			print "err"
			continue
		cityDict[row['Geography']] = cols 
print cityDict

np.save("cityDict.npy", cityDict)