# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 12:56:19 2018

@author: sachi
"""

import pandas as pd
from sklearn.neighbors import KDTree

citycoord=[]
cities_dict={}
cityLatLong_Dict={}
cntDf=pd.read_csv('uscities.csv',sep=",")
for i in range(len(cntDf)):
          print(cntDf['city'][i])
          #citystate= city[0]+"-"+city[2].lower()
          cityName=cntDf['city'][i]
          stateName=cntDf['state_id'][i]
          lat=cntDf['lat'][i]
          long=cntDf['lng'][i]
          cityComb=cityName.lower()+"-"+stateName.lower()
          cityLatLong_Dict[cityComb]=str(lat)+"/"+str(long)
          city_coordinate_key = (lat, long)
          citycoord.append(city_coordinate_key)
          c =cityName+"-"+stateName
          cities_dict[city_coordinate_key] = c  
tree = KDTree(citycoord, leaf_size=2)
          

class Check_nearestloc:

    @staticmethod
    def mainfunction(cityStateComb):        
        extLatVal=cityLatLong_Dict[cityStateComb].split("/")
        latVal=extLatVal[0]
        longVal=extLatVal[1]
        dist, ind = tree.query([(latVal,longVal)], k=160)
        citiesList=[]
        for val in range(159):
            citiesList.append(cities_dict[citycoord[ind[0][val+1]]])
        
        
        return citiesList

    




