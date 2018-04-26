import pandas as pd

df = pd.read_csv('uscitiesv1.3.csv', sep=",")
# cityDt = pd.read_csv('../../edited-list.csv', sep=",")
cityDt = pd.read_csv('tmp_city_list.csv', sep=",")
states = ['Alabama', 'Alaska', 'American Samoa', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'District of Columbia', 'Florida', 'Georgia', 'Guam', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'National',
          'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Northern Mariana Islands', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Puerto Rico', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virgin Islands', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']
stateDf = []
for i in states:
    tmp = df[df.state_name.str.contains(i)]
    cityTmp = cityDt[cityDt.Geography.str.contains(i)]
    cityLL = {}
    for index, row in tmp.iterrows():
        cityLL[row.city+", "+i] = [row.lat, row.lng]
    lat = []
    lng = []
    # print cityLL
    for index, row in cityTmp.iterrows():
        if row.Geography in cityLL:
            lat.append(cityLL[row.Geography][0])
            lng.append(cityLL[row.Geography][1])
        else:
            print 'Not Found: '+row.Geography
            lat.append('NA')
            lng.append('NA')
    cityTmp['lat'] = lat
    cityTmp['lng'] = lng
    stateDf.append(cityTmp)
dfLatLng = pd.concat(stateDf)
dfLatLng.to_csv('proximity_edited_list.csv', index=False)
