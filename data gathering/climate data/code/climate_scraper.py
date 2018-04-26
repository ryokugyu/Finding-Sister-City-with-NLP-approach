from scrapy.selector import Selector
from scrapy.http import HtmlResponse

import requests
import pandas as pd
import numpy as np

import pandas as pd
import nearestlocation

response=''
def checkResp(cspair):
    finalurl='http://www.areavibes.com/'+cspair+'/weather/' 
    print(finalurl)
    page=requests.get(finalurl)
    response = HtmlResponse(url=finalurl,body=page.text,encoding="utf-8")
    htmResponse=response.xpath('//table[@class="av-default"]//tr[not(contains(@class,"head"))]').extract()
    return htmResponse 

complete_cities = pd.read_csv('finacities-list.csv',encoding='ISO-8859-1')


states={ 'Alaska':'AK', 'Alabama':'AL', 'Arkansas':'AR', 'American Samoa':'AS', 'Arizona':'AZ', 'California':'CA', 'Colorado':'CO', 
        'Connecticut':'CT', 'District of Columbia':'DC', 'Delaware':'DE', 'Florida':'FL', 'Georgia':'GA', 'Guam':'GU', 'Hawaii':'HI'
        , 'Iowa':'IA', 'Idaho':'ID', 'Illinois':'IL', 'Indiana':'IN', 'Kansas':'KS', 'Kentucky':'KY', 'Louisiana':'LA', 
        'Massachusetts':'MA', 'Maryland':'MD', 'Maine':'ME', 'Michigan':'MI', 'Minnesota':'MN', 'Missouri':'MO', 
        'Northern Mariana Islands':'MP', 'Mississippi':'MS', 'Montana':'MT', 'National':'NA', 'North Carolina':'NC', 
        'North Dakota':'ND', 'Nebraska':'NE', 'New Hampshire':'NH', 'New Jersey':'NJ', 'New Mexico':'NM', 'Nevada':'NV',
        'New York':'NY', 'Ohio':'OH', 'Oklahoma':'OK', 'Oregon':'OR', 'Pennsylvania':'PA', 'Puerto Rico':'PR', 'Rhode Island':'RI',
        'South Carolina':'SC', 'South Dakota':'SD','Tennessee':'TN', 'Texas':'TX', 'Utah':'UT', 'Virginia':'VA',
        'Virgin Islands':'VI', 'Vermont':'VT', 'Washington':'WA', 'Wisconsin':'WI', 'West Virginia':'WV', 'Wyoming':'WY'
}

# =============================================================================
# page=requests.get('http://www.areavibes.com/farrell-pa/weather/')
# response = HtmlResponse(url='http://www.areavibes.com/farrell-pa/weather/',body=page.text,encoding="utf-8")
# ab=response.xpath('//span/text()').extract()
# 
# =============================================================================
climateData = pd.DataFrame()
climateDataList=[]
for i in range(len(complete_cities)):
    current_comb=complete_cities['Geography'][i]
    print(current_comb)
    #complete_cities['Geography'][i]='Canoochee CDP, Georgia'
    cityStatepair=''
    if(';' in complete_cities['Geography'][i]):
        splitVals=complete_cities['Geography'][i].split(";")
        city=splitVals[0].replace("CDP","").replace("town","").replace("city","").replace("village","").rstrip().lower().replace(" ","+")
        print(splitVals[1])
        state=states[splitVals[1].strip()]
        cityStatepair=city+"-"+state.lower()     
    else:
        splitVals=complete_cities['Geography'][i].split(",")
        city=splitVals[0].replace("CDP","").replace("town","").replace("city","").replace("village","").rstrip().lower().replace(" ","+")
        state=states[splitVals[1].strip()]
        cityStatepair=city+"-"+state.lower()  
    extractResponse=checkResp(cityStatepair)
    
    if len(extractResponse)==0:
       nearLoc=nearestlocation.Check_nearestloc()   
       locVal=nearLoc.mainfunction(cityStatepair.replace("+"," ")) 
    elif 'n/a' in extractResponse[0]:
        nearLoc=nearestlocation.Check_nearestloc()   
        locVal=nearLoc.mainfunction(cityStatepair.replace("+"," "))
        for i in range(159):
            print(i)
            currResp=checkResp(locVal[i].lower().replace(" ","+" ))
            if len(currResp)==0:
                continue
            #print(currResp)
            if 'n/a' in currResp[0]:
                continue
            else:
                break
        citystpair=locVal[i].lower().replace(" ","+" )    
    else:
        citystpair=cityStatepair
        
    finalurl='http://www.areavibes.com/'+citystpair+'/weather/' 
    print(finalurl)
    page=requests.get(finalurl)
    response = HtmlResponse(url=finalurl,body=page.text,encoding="utf-8")
    tempVals=[]
    baseMinTemp=''
    baseMaxTemp=''
    baseAvgTemp=''
    for info in response.xpath('//table[@class="av-default"]//tr[not(contains(@class,"head"))]')[:13]:
        cntr=0
        tmpInt={}
        if(cntr<12):         
            tmpInt['avgmintmp']=info.xpath('td[2]//text()').extract_first()
            tmpInt['avgmaxtmp']=info.xpath('td[3]//text()').extract_first()
            tmpInt['avgtmp']=info.xpath('td[4]//text()').extract_first()   
            tmpInt['precipitation']=info.xpath('td[5]//text()').extract_first()
            
            if 'n/a' not in tmpInt['avgmintmp']:
                baseMinTemp=tmpInt['avgmintmp']
            else:
                tmpInt['avgmintmp']=baseMinTemp
            if 'n/a' not in tmpInt['avgmaxtmp']:
                baseMaxTemp=tmpInt['avgmaxtmp']
            else:
                tmpInt['avgmaxtmp']=baseMaxTemp    
            if 'n/a' not in tmpInt['avgtmp']:
                baseAvgTemp=tmpInt['avgtmp']
            else:
                tmpInt['avgtmp']=baseAvgTemp
                
            tempVals.append(tmpInt)
        cntr=cntr+1

    avgmaxtmp=np.mean([int(tempVals[i]['avgmaxtmp'].replace("°F","")) for i in range(11)])
    avgmintmp=np.mean([int(tempVals[i]['avgmintmp'].replace("°F","")) for i in range(11)])
    avgtmp=np.mean([int(tempVals[i]['avgtmp'].replace("°F","")) for i in range(11)])
    
    precipitation=np.mean([float(tempVals[i]['precipitation'].replace('"','').replace('n/a','0')) for i in range(11)])
    climateCurrent={}
    climateCurrent['cityStatepair']=current_comb
    climateCurrent['avgmintmp']=avgmintmp
    climateCurrent['avgmaxtmp']=avgmaxtmp
    climateCurrent['avgtmp']=avgtmp
    climateCurrent['precipitation']=precipitation
    climateDataList.append(climateCurrent)
    

     
    
dfClimate = pd.DataFrame(climateDataList)
    
dfClimate.to_csv('climate_data_complete.csv')    
    
    
    
    
