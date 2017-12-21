# -*- coding: utf-8 -*-
"""
following code reads 'link to restaurants.txt' file and extracts all pages of a restaurant in a
folder of its own name. It stops as soon as 10K reviews have been extracted.
Created on Wed Nov 15 16:51:32 2017

@author: Anil
"""
""" this code saves all content of a restaurant's pages to a text file"""

from bs4 import BeautifulSoup
import re
import time
import requests
import os

def save_each_rest_html_details(url,cuisine):
    count_of_review = 0
    f = open('link to restaurants.txt') # reading file for link to each restaurant
#    flag = 0
    for line in f:
#        if 'the-indian-kitchen-thornhill' in line: flag +=1; continue
#        if flag == 0: continue
        elements = line.strip('\n').split('\t')
        nameOfRest = elements[0]
        urlToRest = elements[1].split("?")[0]
        os.makedirs(nameOfRest) # making a new directory to store all pages of a restaurant
        print("no. of reviews covered",count_of_review) # keeping a track of total no. of reviews
        count_of_review += int(elements[2])
        if count_of_review >=10000: break
        pg = 0
        while 1>0:
            pg += 1
            print ('pg=',pg) # keeping a track of current page being extracted
            html=None
            pageLink=url+urlToRest+'?start='+str(20*(pg-1))
            print(pageLink)
            for i in range(5): # try 5 times
                try:
                    #use the browser to access the url
                    response=requests.get(pageLink,headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', })
                    html=response.content # get the html
                    break # we got the file, break the loop
                except Exception as e:# browser.open() threw an exception, the attempt to get the response failed
                    print ('failed attempt',i)
                    time.sleep(2)
            if not html:continue # couldnt get the page, ignore
            
            soup = BeautifulSoup(html.decode('ascii', 'ignore'),'lxml') # parse the html 
            
            noOfpages = soup.find('div',{'class':re.compile('page-of-pages arrange_unit arrange_unit--fill')})
            print(noOfpages.text.strip())
            noOfpages = noOfpages.text.strip().split(' ')
            f_rest_html=open(nameOfRest+'/'+nameOfRest+noOfpages[1]+'.html','a+')
            f_rest_html.write(str(soup))
            f_rest_html.close()            
            if noOfpages[1] == noOfpages[3]: break # keeping a track of when to stop looking for next page of the current restaurant
            time.sleep(2)
        time.sleep(5)
    f.close()
    
if __name__=='__main__':
    url = 'https://www.yelp.com'
    cuisine = 'indian'
    save_each_rest_html_details(url,cuisine)


