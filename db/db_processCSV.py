import db_function as db
import csv
import time

start_time = time.clock()

with open('city_with_data.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    db.db_connect().drop_collection('catergories')
    for row in reader:
        print (row['Geography']) #'CityName'
        query = {'Geography': row['Geography'], 'stateFullName': row['stateFullName'], 
                 'lat': row['lat'], 'lng': row['lng'], 
                 'avgmaxtmp': row['avgmaxtmp'], 'avgmintmp': row['avgmintmp'], 'avgtmp': row['avgtmp'], 'precipitation': row['precipitation'], 
                 'population': row['population'], 'per_dem': row['per_dem'], 'per_gop': row['per_gop']}
        db.db_insert('catergories', query)

print("--- %s seconds ---" % (time.clock() - start_time))
