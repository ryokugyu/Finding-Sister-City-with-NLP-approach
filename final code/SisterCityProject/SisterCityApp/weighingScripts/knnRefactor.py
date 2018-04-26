"""
City comparison algorithm
"""

import os
from sklearn import neighbors as skln
from SisterCityApp.weighingScripts import sharedFormulas as form
from math import sin, cos, sqrt, atan2, radians

dirname2 = os.path.dirname(os.path.realpath('__file__'))
dirname2+='\\SisterCityApp\\\weighingScripts\\'
# Create a dictionary from the city_with_data file
city_dict = form.make_city_dict(dirname2+"city_with_data.csv")
#city_name, weights = form.get_user_input(city_dict)


class WeighCities:
    # Get the user's input
    # approximate radius of earth in km
    def calcDistLatLong(lat1,long1,lat2,long2):
        R = 6373.0
        
        lat1 = radians(lat1)
        lon1 = radians(long1)
        lat2 = radians(lat2)
        lon2 = radians(long2)
        
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        
        distance = R * c
        
        distVal= distance*0.621371
        
        return distVal
   
    
    def getMatchedCities(self,city_name,weights):
        # Get the corresponding input city
        input_city = city_dict[city_name]
        
        # Calculate distances from input city
        distance_dict = form.calc_city_dict_distance(city_dict, input_city, False)
        
        # Normalize the city dictionary
        normalized_dict = form.normalize_city_dict(distance_dict)
        
        # Normalize the weights
        # _, weights = form.normalize_weights(weights)
        
        input_city_node = normalized_dict[city_name]
        # Perform knn analysis
        for node in normalized_dict.values():
            #print node
            node[0] = node[0] * weights[0] #prox
            node[1:5] = [node[i] * weights[1] for i in range(1,5)] #climate
            node[5] = node[5] * weights[2] #population
            node[6:8] = [node[i] * weights[3] for i in range(6, 8)] #politics
            node[7:9] = [node[i] * weights[4] for i in range(7, 9)] #economy
            node[9:] = [node[i] * weights[2] for i in range(9, len(node))] #other demographics
            # print(node)
        
        tree = skln.KDTree(list(normalized_dict.values()), leaf_size=2)
        dist, ind = tree.query([input_city_node], k=6)
        #print dist
        #print ind
        cityValuesList=[]
        cntr=0
        refLat=''
        refLong=''
        for near in ind[0]:
            cntr+=1
            cityDict={}
            cityDict['cityname']=list( normalized_dict.keys() )[near]
            currlist=list(city_dict.values())
            latitude=currlist[near][0]
            longitude=currlist[near][1]
            if cntr>1:
                currDist=WeighCities.calcDistLatLong(refLat,refLong,latitude,longitude)
            else:
                currDist=0
                refLat=latitude
                refLong=longitude
                
            cityDict['cityname']=list(normalized_dict.keys() )[near]
            cityDict['latitude']=currlist[near][0]
            cityDict['longitude']=currlist[near][1]
            cityDict['distance']=("{0:.2f}".format(currDist))
            cityDict['avgmaxtmp']=("{0:.2f}".format(currlist[near][2]))
            cityDict['avgmintmp']=("{0:.2f}".format(currlist[near][3]))
            cityDict['avgtmp']=("{0:.2f}".format(currlist[near][4]))
            cityDict['rainfall']=("{0:.2f}".format(currlist[near][5]))
            cityDict['population']=currlist[near][6]
            cityDict['perDem']=("{0:.2f}".format(currlist[near][7]*100))
            cityDict['perGOP']=("{0:.2f}".format(currlist[near][8]*100))
            cityDict['medianIncome']=currlist[near][9]
            cityDict['meanIncome']=currlist[near][10]
            cityDict['marriedMales']=currlist[near][11]
            cityDict['marriedFemale']=currlist[near][12]
            cityDict['highSchoolGrad']=currlist[near][13]
            cityDict['usborn']=currlist[near][16]
            cityDict['usbornRes']=currlist[near][17]
            cityDict['usbornNonres']=currlist[near][18]
            cityDict['uscitforeignborn']=currlist[near][19]    
            cityDict['nonuscitForeignBorn']=currlist[near][20] 
            
            cityValuesList.append(cityDict)

        return cityValuesList   

    
           # print( list( normalized_dict.keys() )[near])
           # print( list( city_dict.values() )[near] )