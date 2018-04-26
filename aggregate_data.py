import pandas as pd

cityDt = pd.read_csv('edited-list.csv',sep=',')
proDt = pd.read_csv('data gathering/proximity/data/proximity_2.csv')

tmp = pd.merge(cityDt, proDt, on='id')
tmp.to_csv('city-list-with-proximity.csv',sep=',')

cliDt = pd.read_csv('data gathering/climate data/data file/climate_data_complete.csv')
tmp2 = pd.merge(tmp, cliDt, on='Geography')
tmp2.to_csv('city-list-with-proximity-climate.csv',sep=',')

popDt = pd.read_csv('data gathering/proximity/code/population_edited_list.csv')
tmp2 = pd.merge(tmp, popDt, on='id')
tmp2.to_csv('city-list-with-proximity-climate-population.csv',sep=',')

eleDt = pd.read_csv('data gathering/election data/data/final_election.csv')
tmp = pd.merge(tmp2, eleDt, on='Geography')
tmp.to_csv('city-list-with-proximity-climate-population-election.csv',sep=',')

ecoDt = pd.read_csv('data gathering/economy/economy_data.csv')
tmp = pd.merge(tmp2, ecoDt, on='Geography')
tmp.to_csv('city_with_data.csv',sep=',')

