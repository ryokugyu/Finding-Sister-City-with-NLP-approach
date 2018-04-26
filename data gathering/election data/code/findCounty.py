#!/usr/bin/python

"""
This uses uscounties.com to lookup which county
a given city is in. In the context of the sister
cities project, it can be used to associate data
at the county level to cities within that county,
in case city specific data is not available.
"""

import re
import requests
from bs4 import BeautifulSoup
import csv
import sys
import numpy as np

base = 'http://www.uscounties.com/zipcodes/search.pl?query='
countyDict = {}
with open('finacities-list.csv') as csvfile, open('edited-list.csv', 'wb') as out:
  print 'Printed cities couldn\'t be found: '
  reader = csv.DictReader(csvfile)
  writer = csv.DictWriter(out, fieldnames=reader.fieldnames)
  writer.writeheader()
  for row in reader:
    try:
      trimCity = re.sub('((city.*)?(town.*)?(village.*)?)','',row['Geography']).strip()
      stateAbbr = row['stateAbbr']
      #print(trimCity + row['stateAbbr'])
      query = trimCity + '+' + stateAbbr +'&stpos=0&stype=AND'
      #query = 'lexington+va&stpos=0&stype=AND'
      search = requests.get(base + query)
      soup = BeautifulSoup(search.content, 'html.parser')
      result = soup.find('tr', class_='results')
      if result:
        county = result.find_all('td')[2].string.strip()
        countyDict[trimCity + ', ' + stateAbbr] = county
        writer.writerow(row)
      else:
        print trimCity + ', ' + stateAbbr
    except KeyboardInterrupt:
      raise
    except:
      print("ERROR: ", sys.exc_info()[0])
      print "err at " + trimCity + ", " + stateAbbr

np.save("countyDict.npy", countyDict)