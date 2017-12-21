# -*- coding: utf-8 -*-
"""
This file reads and stores following details of each restaurant:-
Name of restaurant, link to its own page, no. of reviews posted on its page.
Created on Thu Nov  9 16:53:16 2017

@author: Anil
"""

from bs4 import BeautifulSoup
import re
import time
import requests

def extract_link_to_rest(url):
    fw=open('1 link to restaurants.txt','w')
    pageNum=42 # number of pages to collect (to be written manually before executing the code)
    
    for q in range(1,pageNum+1): # for each page 

        print ('page',q)
        html=None

        pageLink=url+'find_desc=Indian+Food&find_loc=Toronto,+ON,+Canada&start='+str(10*(q-1))# make the page url
		
        for i in range(5): # try 5 times
            try:
                #use the browser to access the url
                response=requests.get(pageLink,headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', })
                html=response.content # get the html
                break # we got the file, break the loop
            except Exception as e:# browser.open() threw an exception, the attempt to get the response failed
                print ('failed attempt',i)
#                time.sleep(2) # wait 2 secs
				
		
        if not html:continue # couldnt get the page, ignore
        
        soup = BeautifulSoup(html.decode('ascii', 'ignore'),'lxml') # parse the html 
        
        linksOfRest=soup.findAll('a', {'class':re.compile('biz-name js-analytics-click')}) # get all the review divs
        noOfRat = soup.findAll('span', {'class':re.compile('review-count rating-qualifier')})
        for i in range(2,len(noOfRat)):
            fw.write(linksOfRest[i].text +'\t'+ linksOfRest[i]['href'] +'\t'+ noOfRat[i].text.strip().split(' ')[0]+ '\n') # write to file
#		getCritic(review)+'\t'+getRating(review)+'\t'+getSource(review)+'\t'+getDate(review)+'\t'+getTextLen(review)+
        time.sleep(3)	# wait 2 secs 
    fw.flush()
    fw.close()
    
if __name__=='__main__':
    url='https://www.yelp.com/search?'
    extract_link_to_rest(url)