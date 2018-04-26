#!/usr/bin/python

"""
Associates cities in the input list with their counties
in the premade dictionary.
"""

import re
import csv
import numpy as np

cityDict = np.load('countyDict.npy').item()
countyDict = {}
#Special case for alaska
alaskaPer = ['0.37715947248', '0.528870018006']
print cityDict

with open('electionData.csv') as elec_csv:
  reader = csv.DictReader(elec_csv)
  for row in reader:
    county = row['county_name'].upper()

    county = re.sub('((COUNTY.*)?(PARISH.*)?)', '', county).strip()
    county = re.sub('((CITY.*)+)', '(CITY)', county).strip()

    #special cases
    county = re.sub('((LAPORTE)+)', 'LA PORTE', county).strip()
    county = re.sub('DE\sKALB', 'DEKALB', county).strip()

    print county
    per_dem = row['per_dem']
    per_gop = row['per_gop']
    countyDict[county] = (per_dem, per_gop)
print 'Done making countyDict'

with open('city_election.csv', 'wb') as out:
  fieldnames = ['city', 'stateAbbr', 'per_dem', 'per_gop']
  writer = csv.DictWriter(out, fieldnames=fieldnames)
  writer.writeheader()
  for city in cityDict:
    print 'working on ' + city + '...'
    cityToWrite = city[:city.find(',')]
    abbr = city[city.rfind(', ') + 2:]
    if abbr == 'AK':
      percents = alaskaPer
    else:
      try:
        percents = countyDict[cityDict[city]]
      except KeyError:
        print '################### keyerr: ' + cityDict[city] + ' ###################'
    writer.writerow({'city':cityToWrite, 'stateAbbr': abbr, 'per_dem': percents[0], 'per_gop': percents[1]})


