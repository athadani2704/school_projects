# -*- coding: utf-8 -*-
"""
following code reads 'link to restaurants.txt' file and extracts all pages of a user in a
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

def save_each_user_html_details(url,cuisine):
    countOfReview, limitCount = 0, 0
    f = open('1 link to users.txt') # reading file for link to each user
#    flag = 0
    for line in f:
#        if 'Amritpal ' in line: flag +=1
#        if flag == 0: continue
        elements = line.strip('\n').split('\t')
        nameOfUser = elements[0]
        nameOfUser = re.sub('[^a-zA-Z\d]',' ',nameOfUser).strip()  #removing special character from name as folder 
#                                                                        name cannot contain special character
        urlToUser = elements[1].split("?")[1]
        noOfReviewsUserHas = int(elements[3]) # taken here so that we do not need to count more than this amount
        if os.path.isfile("userFiles/" + nameOfUser):
            continue
        os.makedirs("userFiles/" + nameOfUser) # making a new directory to store all pages of a user
        pg = 0
        while 1>0:
            pg += 1
            print ('pg=',pg) # keeping a track of current page being extracted
            html=None
            pageLink=url + "/user_details_reviews_self?" + urlToUser + "&rec_pagestart="+str(10*(pg-1))
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
            reviewsPerPg = soup.findAll('a',{'class':re.compile('biz-name js-analytics-click')}) # checking no. of reviews per page
            noOfpages = soup.find('div',{'class':re.compile('page-of-pages arrange_unit arrange_unit--fill')})
            noOfpages = noOfpages.text.strip().split(' ')
            f_user_html=open("userFiles/" + nameOfUser +'/'+nameOfUser + noOfpages[1]+'.html','a+')
            f_user_html.write(str(soup))
            f_user_html.close()
            print("reviews on this page ", len(reviewsPerPg))
            countOfReview += len(reviewsPerPg)
            limitCount += len(reviewsPerPg)
            if noOfpages[1] == noOfpages[3] or limitCount >= noOfReviewsUserHas: 
                limitCount = 0; print("reviews covered "+ str(countOfReview)); break # keeping a track of when to stop looking for next page of the current restaurant
            time.sleep(2)
            print("reviews covered "+ str(countOfReview))
        time.sleep(5)
    f.close()
    
if __name__=='__main__':
    url = 'https://www.yelp.com'
    cuisine = 'indian'
    save_each_user_html_details(url,cuisine)


