#Implementation of Haversine Formula for distance
#Takes coordinates as input and returns distance across earth's surface in km
from skcriteria import MIN, MAX
from math import cos, asin, sqrt, pi
from collections import OrderedDict
import csv
import copy

#number of columns in each data category
#NUM_PROX = 1
#NUM_CLIM = 4
#NUM_DEMO = 11
#NUM_POLI = 2
#NUM_ECON = 2


def distance(lat1, lng1, lat2, lng2):
    p = pi/180     #Pi/180
    a = 0.5 - cos((lat2 - lat1) * p)/2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lng2 - lng1) * p)) / 2
    return 12742 * asin(sqrt(a)) #2*R*asin

# Takes a list of values and normalizes them from 0 to 1
# Used in scikit-criteria 
def normalize_weights(weights):
   max_min = [MIN if weight >= 0 else MAX for weight in weights]
   abs_weights = [abs(weight) for weight in weights]
   total = sum(abs_weights)
   normalized_weights = [float(weight) / total for weight in abs_weights]
   return (max_min, normalized_weights)

"""
Creates numpy dictionary for faster testing; this
is a placeholder until the database is constructed
"""
def make_city_dict(filename):
    city_dict = OrderedDict()
    with open(filename, 'r') as city_csv:
        reader = csv.DictReader(city_csv)

        header_names = reader.fieldnames
        
        for row in reader:
            str_row = [row[header] for header in header_names][4:]
            try:
                float_row = [float(x) for x in str_row]
            except:
                # print("Error converting row")
                continue
            city_dict[row['Geography']] = float_row
    return city_dict

"""
Calculates the distance between cities
NOTE: Also takes absval difference between input city and other city parameters
if take_diff is TRUE
"""
def calc_city_dict_distance(city_dict, input_city, take_diff):
    # If we don't make a deep copy, the input city values will be overwritten
    # That means, going forward, all subtractions will be invalid
    distance_dict = copy.deepcopy(city_dict)
    input_lat = input_city[0]
    input_lng = input_city[1]
    for city in distance_dict:
        city_entry = distance_dict[city]
        if take_diff:
            # Take differences from items, excluding lat and lng
            for i in range(2, len(city_entry)):
                city_entry[i] = abs(city_entry[i] - input_city[i])
                if input_city[i] == 0:
                    print("Processing error")
                    print (input_city[i])
                    exit()
                #     exit()
                # print("Good")
        dist = distance(input_lat, input_lng, city_entry[0], city_entry[1])
        distance_dict[city] = [dist] + city_entry[2:]
    return distance_dict

"""Returns/validates input city and weights"""
def get_user_input(city_dict):
    city_name = ""
    while city_name not in city_dict:
        if city_name: print("Invalid Name")
        city_name = input("Enter city (use full geography): ")

    weights = []
    while len(weights) != 5:
        if weights: print("Invalid Weights")
        weights = input("Enter list of weights [prox, clim, demog, pol, econ]: ").split(",")
        try:
            weights = [float(weight.strip()) for weight in weights]
        except:
            print("Error: non-numeric weights")
            weights = []
            continue

    return (city_name, weights)


"""
Normalize all values to be between 0 and 1
"""
def normalize_city_dict(city_dict):
    normalized_dict = copy.deepcopy(city_dict)
    # Hacky way to get the "first" dictionary item
    length = len(city_dict[next(iter(city_dict))])
    mins = copy.deepcopy(city_dict[next(iter(city_dict))])
    maxes = copy.deepcopy(city_dict[next(iter(city_dict))])

    # THIS WILL NORMALIZE THE LAT AND LNG IF DONE BEFORE CALCULATING THE DISTANCES
    for city in city_dict:
        city_entry = city_dict[city]
        for i in range(length):
            mins[i] = min( mins[i], city_entry[i] )
            maxes[i] = max( maxes[i], city_entry[i] )
    
    for city in normalized_dict:
        city_entry = normalized_dict[city]
        for i in range(length):
            city_entry[i] = (city_entry[i] - mins[i]) / (maxes[i] - mins[i])

    return normalized_dict

# test_dict = normalize_city_dict(make_city_dict("city_with_data.csv"))
