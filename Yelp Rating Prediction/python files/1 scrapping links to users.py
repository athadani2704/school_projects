# -*- coding: utf-8 -*-
"""
This file reads and stores following details of each restaurant:-
Name of restaurant, link to its own page, no. of reviews posted on its page.

link_to_users(url) function saves user name and link to the user in a file named '1 link to users.txt' until no. of reviews>=10K
and number of users >= 50 per restaurant
@author: Anil
"""

from bs4 import BeautifulSoup
import re
import os

# this function extracts link to first page of user and her/his name
def get_userName_and_link(review):
    html = review.find('a', {'class':re.compile('user-display-name js-analytics-click')})
    return html.text.strip(), html['href']

# this function extracts no. of reviews posted by that user. if they are greater than 100, it will report only 100
def get_reviewCount(review):
    html = review.find('li', {'class':re.compile('review-count responsive-small-display-inline-block')})
    if html:
        h = int(html.text.strip().split(' ')[0])
        if h>=100:
            return (h, 100)
        else: return (h,h)
    else: return (0,0)


def link_to_users(url):
    fw=open('1 link to users.txt','a+')
    f = open('1 link to restaurants.txt')
    listOfUser = [] # to avoid picking up same names again.
    noOfreviews = 0 # number of reviews covered by extracting users till now
#    flag = 0
    for line in f: # for each page
#        if 'Silver ' in line: flag = 1
#        if flag == 0: continue
        noOfUsers = 0 # number of users covered till now
        if noOfreviews >= 10000: print ('reviews read= ',noOfreviews); break
        nameOfRest = line.strip('\n').split('\t')[0]
        pg = 0
        if not os.path.isdir("restaurantFiles/"+nameOfRest): continue
        while 1>0:
            if noOfreviews >= 10000: print ('reviews read= ',noOfreviews); break
            review_flag = 0 # to check if it's first review. If yes skip it.
            pg += 1 # incrementing pages to change name of files to be read in each loop
            if not os.path.isfile("restaurantFiles/"+nameOfRest+'/'+nameOfRest+str(pg)+'.html'): break # checking if the file with this new name exists
            print ('reviews read= ',noOfreviews)
            read_html_file = open("restaurantFiles/"+nameOfRest+'/'+nameOfRest+str(pg)+'.html')
            print(nameOfRest+str(pg)+'.html')		              
            soup = BeautifulSoup(read_html_file,'lxml') # parse the html content of the file

            reviews=soup.findAll('div', {'class':re.compile('review-sidebar-content')}) # get all the review divs

            for review in reviews:
                if review_flag == 0: review_flag = 1; continue
                userName, linkToUser = get_userName_and_link(review)
                reviewCount, ishundred = get_reviewCount(review)
                if userName in listOfUser: continue
                else: listOfUser.append(userName)
                fw.write(userName + '\t' + linkToUser + '\t' + str(reviewCount) + '\t' + str(ishundred)+ '\n')
                noOfreviews +=ishundred
                noOfUsers +=1
            if noOfUsers >= 50: print ("Users read for this restarant: ",noOfUsers); break
    f.close()
    
if __name__=='__main__':
    url = 'file:///F:/Ki2/University%20applications/Stevens/Study%20Material/Second%20Sem/BIA%20660/Project/'
    link_to_users(url)