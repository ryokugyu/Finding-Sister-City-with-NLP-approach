import pandas as pd

cityDt = pd.read_csv('../../edited-list.csv', sep=",")

geo = []
for i, r in cityDt.iterrows():
	geo.append(r.Geography.replace('city','').replace('City','').replace('town','').replace('Town','').replace('village','').replace(' ,',',').strip().lstrip().rstrip().replace(' ,',','))

cityDt.drop('Geography',axis = 1)
cityDt['Geography'] = geo
cityDt.to_csv('tmp_city_list.csv',index=False,sep=",")