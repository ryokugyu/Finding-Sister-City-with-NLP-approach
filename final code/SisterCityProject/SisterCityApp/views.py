from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
import os
#import sys  
#sys.path.append(os.path.abspath(os.path.dirname('__file__')+'/'))
from SisterCityApp.newsanalytics import news_rank
from SisterCityApp.weighingScripts import knnRefactor
import math


# Create your views here.
def homePage(request):
    return render(request, 'index.html')

def searchCity(request):
    cityVal=request.POST['cityinput']
    climateWt=request.POST['climate-value2']
    demogWt=request.POST['demographics-value2']
    economyWt=request.POST['economy-value2']
    politicsWt=request.POST['politics-value2']
    proximityWt=request.POST['proximity-value2']
    print(cityVal)
    print(climateWt)
    print(demogWt)
    print(economyWt)
    print(politicsWt)
    print(proximityWt)
    weightsColl=[int(proximityWt),int(climateWt),int(demogWt),int(politicsWt),int(economyWt)]
    weightObj=knnRefactor.WeighCities()
    matchedCitiesAtt=weightObj.getMatchedCities(cityVal,weightsColl)
    print(matchedCitiesAtt)
    request.session['Citieslist']=matchedCitiesAtt

    return render(request, 'results.html',{'matchedCities':matchedCitiesAtt})

def searchSpecific(request):
    list_to_process = request.session['Citieslist']
    print(list_to_process)
# =============================================================================
#     cityone=request.POST['cityone']
#     citytwo=request.POST['citytwo']
#     citythree=request.POST['citythree']
#     cityfour=request.POST['cityfour']
#     cityfive=request.POST['cityfive']
# =============================================================================
    searchQuery=request.POST['searchQuery']

   # cityList=[cityone,citytwo,citythree,cityfour,cityfive]
    citiesList= [list_to_process[cntr]['cityname'] for cntr in range(len(list_to_process))]
    newsrankObj=news_rank.newsrank()
    bestCities=newsrankObj.getTopCity(searchQuery,citiesList[1:])
    cityRankedList=[]

    for vals in bestCities:
        for innVal in list_to_process[1:]: 
            if innVal['cityname']== vals['City']:
               if math.isnan(float(vals['Score'])):
                  continue 
               innVal['score']=vals['Score']
               cityRankedList.append(innVal)
    print(bestCities)
    print(cityRankedList)
    return render(request, 'refinedSearchResults.html',{'cityRankedList':cityRankedList})    
	   
		
		
		
			 