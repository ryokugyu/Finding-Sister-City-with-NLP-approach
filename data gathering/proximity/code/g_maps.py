import pandas as pd
import math
import requests

df = pd.read_csv('proximity_edited_list.csv',sep=',')
api_key = "AIzaSyAsGdDWgWwFQDGdHxP5qpUrZS2Z46fUvAo"

n = 0
lat = []
lng = []
for index, row in df.iterrows():
	if math.isnan(row.lat) or math.isnan(row.lng):
		address = row['Geography']
		try:
			api_response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}'.format(address, api_key))
			api_response_dict = api_response.json()
			if api_response_dict['status'] == 'OK':
				lat.append(api_response_dict['results'][0]['geometry']['location']['lat'])
				lng.append(api_response_dict['results'][0]['geometry']['location']['lng'])
				n += 1
				print(n, address)
			else:
				lat.append('NA')
				lng.append('NA')
				print("Error!")
		except:
			lat.append('NA')
			lng.append('NA')
	else:
		lat.append(row.lat)
		lng.append(row.lng)
df['lat'] = lat
df['lng'] = lng
df.to_csv('proximity_2.csv',sep=',')