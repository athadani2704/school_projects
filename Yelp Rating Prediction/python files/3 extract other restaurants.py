# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 18:39:55 2017

@author: Anil
"""

from bs4 import BeautifulSoup
import re
import time
import requests
import os

def extract_user_rating(pageLink):
    html=None
    for i in range(5): # try 5 times
        try:
            #use the browser to access the url
            response=requests.get(pageLink,headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', })
            html=response.content # get the html
            break # we got the file, break the loop
        except Exception as e:# browser.open() threw an exception, the attempt to get the response failed
            print ('failed attempt',i)
            time.sleep(2)	              
    soup = BeautifulSoup(html.decode('ascii', 'ignore'),'lxml') # parse the html 

    ratings = soup.findAll('tr', {'class':re.compile('histogram_row histogram_row--')})
    total_rating, count = 0, 0
    for r in ratings:
        count += int(r.find('td', {'class':re.compile('histogram_count')}).text)
        total_rating += int(r.find('th', {'scope':re.compile('row')}).text.strip().split(' ')[0]) * int(r.find('td', {'class':re.compile('histogram_count')}).text)
    try:
        avg = round(total_rating/count, 2) # write to file
    except Exception as e:
        print("exception recieved", e)
        avg = 0
    print("avg rating by user: ",avg)
    return avg

def extract_other_rest(restName, link_to_rest):
    pageLink = 'https://www.yelp.com' + link_to_rest
    for i in range(5): # try 5 times
        try:
            #use the browser to access the url
            response=requests.get(pageLink,headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', })
            html=response.content # get the html
            break # we got the file, break the loop
        except Exception as e:# browser.open() threw an exception, the attempt to get the response failed
            print ('failed attempt',i)
            time.sleep(2)
    if not html:return 0 # couldnt get the page, ignore
    soup = BeautifulSoup(html.decode('ascii', 'ignore'),'lxml') # parse the html 
    f = open("restaurantFiles/otherFiles/" + restName + ".html", "a+")
    f.write(str(soup))
    f.close()

def extracting_ratings_and_other_rest():
    rating_by_user = open('3 ratings by user.txt', 'a+')
    other_rest = open('3 other restaurants.txt', 'a+')
    restFile = open('1 link to restaurants.txt')
    userFile = open('1 link to users.txt') # reading file for link to each user
#    creating a list of restaurant names that are already extracted
    existing_rest = []
    os.makedirs("restaurantFiles/otherFiles")
    for line in restFile:
        existing_rest.append(line.strip('\n').split('\t')[0])
    restFile.close()
#    flag = 0
    counter = 0
    for line in userFile:
#        if 'Mike D.' in line: flag +=1;continue
#        if flag == 0: continue
        elements = line.strip('\n').split('\t')
        nameOfUser1 = elements[0]
        nameOfUser = re.sub('[^a-zA-Z\d]',' ',nameOfUser1).strip()  #removing special character from name as folder 
#                                                                        name cannot contain special character
        if not os.path.isdir("userFiles/" + nameOfUser):
            continue
        pg = 0
        while counter < 5000:
            pg += 1
            if not os.path.isfile("userFiles/" + nameOfUser + "/" + nameOfUser + str(pg) + ".html"):
                break
            print("userFiles/" + nameOfUser + "/" + nameOfUser + str(pg) + ".html")
            f = open("userFiles/" + nameOfUser + "/" + nameOfUser + str(pg) + ".html")
            soup = BeautifulSoup(f,'lxml') # parse the html content of the file
            f.close()
            reviews = soup.findAll('div', {'class':re.compile('^review$')})
            if pg==1:
                avg_user_rating = extract_user_rating("https://www.yelp.com"+elements[1])
            
            for review in reviews:
                restName = review.find('a', {'class':re.compile('biz-name js-analytics-click')}).text.strip()
                
                rating_to_rest = review.find('img', {'class':re.compile('offscreen')})['alt'].strip().split(' ')[0]    
                if not rating_to_rest: rating_to_rest = 1

                print("restaurant name: ",restName)
                other_rest.write('\n' + restName)

                print(nameOfUser1 + '\t' + restName + '\t' + str(avg_user_rating) + '\t' + str(rating_to_rest))
                rating_by_user.write('\n' + nameOfUser1 + '\t' + restName + '\t' + str(avg_user_rating) + '\t' + str(rating_to_rest))

                if "/" in restName or restName in existing_rest: print("already in list: ", restName); continue # skips restaurants with "/" in name
                extract_other_rest(restName, review.find('a', {'class':re.compile('biz-name js-analytics-click')})['href'])          
                existing_rest.append(restName)
                counter +=1
    rating_by_user.close()
    other_rest.close()
    userFile.close()
    
if __name__=='__main__':
    extracting_ratings_and_other_rest()












