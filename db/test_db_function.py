import db_function as db
import csv
import time
#db_delete('catergories', {'city': 'aaa'})
#db_delete('catergories', {'city': 'bbb'})
#v1 = 'aaa'
#v2 = 'good'
#query = {'city': v1, 'weather': v2}
#db_insert('catergories', query)
#query = {'$set':{'city': 'aaa', 'weather': 'bad'}}
#db_update('catergories', {'weather': 'good'}, query) #aaa good to bad
#db_insert('catergories', {'city': 'bbb', 'weather': 'bad'})
#db_retrieve('catergories', {'weather': 'bad'}) #1 aaa bad, 1 bbb bad
#db_retrieve('catergories', {'weather': 'good'}) #none

#db.db_retrieve('catergories', {'Geography': 'Napoleon city, Missouri'})


f= open('test_db.txt','w+')
with open('city_with_data.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    start_time = time.clock()
    for row in reader:
        #print (row['CityName']) #'CityName'
        #print (row['StateFullName']) #'StateFullName'
        query = {'Geography': row['Geography'], 'stateFullName': row['stateFullName'], 
                 'lat': row['lat'], 'lng': row['lng'], 
                 'avgmaxtmp': row['avgmaxtmp'], 'avgmintmp': row['avgmintmp'], 'avgtmp': row['avgtmp'], 'precipitation': row['precipitation'], 
                 'population': row['population'], 'per_dem': row['per_dem'], 'per_gop': row['per_gop']}
        data = db.db_retrieve('catergories', query)
        if data.count() == 0:
            f.write('No %s\n' %(row['Geography']) )
        if data.count() > 1:
            f.write('Repeat %s\n' %(row['Geography'])  )
    print("--- %s seconds ---" % (time.clock() - start_time)) 
           
#start_time = time.clock()
#data = db.db_retrieve('catergories', {})
#        
#for document in data:
#    print(document)
#
#print("--- %s seconds ---" % (time.clock() - start_time))   