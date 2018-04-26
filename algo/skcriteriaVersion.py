import sys
import numpy as np
import math
# Minimize for items with positive weights, maximize for items with negative weights
from skcriteria import Data, MIN, MAX
from skcriteria.madm import closeness
import sharedFormulas as form
from collections import OrderedDict

# Create a dictionary from the city_with_data file
city_dict = form.make_city_dict("city_with_data.csv")

# Get the user's input
city_name, weights = form.get_user_input(city_dict)

# Get the corresponding input city
input_city = city_dict[city_name]

# Calculate distances and absval differences from input city
distance_dict = form.calc_city_dict_distance(city_dict, input_city, True)

# Normalize the dictionary
normalized_dict = form.normalize_city_dict(distance_dict)

# Normalize the weights
criteria, weights = form.normalize_weights(weights)

# NOTE: THIS SHOULD BE UPDATED IF POSSIBLE
# Split weights into eight criteria
criteria_8 = [criteria[0], criteria[1], criteria[1], criteria[1], criteria[1], criteria[2], criteria[3], criteria[3]]
weights_8 = [weights[0], weights[1] / 4, weights[1] / 4, weights[1] / 4, weights[1] / 4, weights[2], weights[3] / 2, weights[3] / 2]


for city in normalized_dict:
    if normalized_dict[city][0] > .80 and normalized_dict[city][0] < 1.0:
        print (city, distance_dict[city])


# Perform analysis:

# data = Data(list(distance_dict.values()), criteria_8, weights_8, anames=list(distance_dict.keys()))
# print( "Normalized weights: ", str(data.weights))
# print( "Criteria: ", data.criteria)
# dm = closeness.TOPSIS()
# dec = dm.decide(data)
# print( dec.e_.ideal)
# for i in dec.rank_[:10]:
#     print( list(distance_dict.keys())[i], list( distance_dict.values() )[i] )
