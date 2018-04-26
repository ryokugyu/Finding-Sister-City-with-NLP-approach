"""
City comparison algorithm
"""

import sys
from sklearn import neighbors as skln
import sharedFormulas as form

# Create a dictionary from the city_with_data file
city_dict = form.make_city_dict("../city_with_data.csv")

# Get the user's input
city_name, weights = form.get_user_input(city_dict)

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
dist, ind = tree.query([input_city_node], k=10)
#print dist
#print ind

for near in ind[0]:
    print( list( normalized_dict.keys() )[near])
    print( list( city_dict.values() )[near] )