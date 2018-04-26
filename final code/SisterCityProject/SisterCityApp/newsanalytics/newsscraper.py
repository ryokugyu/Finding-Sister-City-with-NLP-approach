# -*- coding: utf-8 -*-
"""
Created on Sun Apr  8 02:43:39 2018

@author: sachi
"""

import urllib
import urllib.request
import urllib.parse
import requests
from scrapy.http import HtmlResponse
from newspaper import Article

class ScrapeNews:


    @staticmethod
    def getNewsArticles(queryVal):
        finalurl = 'https://news.google.com/news/search/section/q/' +\
                urllib.parse.quote(queryVal)+'/'+urllib.parse.quote(queryVal)+'?hl=en&gl=US&ned=us'
        
        page=requests.get(finalurl)
        response = HtmlResponse(url=finalurl,body=page.text,encoding="utf-8")
        hrefList=[href for href in response.xpath('//a[@class="nuEeue hzdq5d ME7ew"]/@href').extract()]
        
        # =============================================================================
        # page=requests.get(hrefList[1])
        # response = HtmlResponse(url=finalurl,body=page.text,encoding="utf-8")
        # htmResponse=response.xpath('//p').text().extract()
        # =============================================================================
# =============================================================================
#         newsVal=[]
#         for selector in response.xpath('//p'):
#             newsVal.append(selector.xpath("text()").extract())
# =============================================================================
        #articleText=[for i in range(len(htmResponse)) ]
        articlesList=[]
        for i in range(5):
            #websiteCode=urllib.request.urlopen(hrefList[i]).getcode()
           # if websiteCode == 200: 
             try:
                article = Article(hrefList[i])
                article.download()
                article.parse()
                articlesList.append(article.text)
             except:
                print('article download failed')
                continue  
        return articlesList    