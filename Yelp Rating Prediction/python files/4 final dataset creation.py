# -*- coding: utf-8 -*-
"""

Created on Thu Nov 30 13:23:58 2017

@author: Anil
"""
from bs4 import BeautifulSoup
import re
import os
import pandas as pd

def extract_avg_rest_rating():
    f= open("1 link to restaurants.txt")
    f1 = open("3 other restaurants.txt")
    f2 = open("4 avg rest rating.txt", 'a+')
    pg = 1
    for line in f:
        restName = line.strip('\n').split('\t')[0]
        if not os.path.isfile("restaurantFiles/" + restName + "/" + restName + str(pg) + ".html"): continue
        
        r = open("restaurantFiles/" + restName + "/" + restName + str(pg) + ".html")
        soup = BeautifulSoup(r,'lxml') # parse the html content of the file
        r.close()
        try:
            rev = soup.find('div',{'class':re.compile('rating-info clearfix')})
            rating = rev.find('img',{'class':re.compile('offscreen')})['alt'].split(' ')[0]
        except:
            print("Exception occured")
            rating = 1
        print(restName + '\t' + str(rating))
        f2.write('\n' + restName + '\t' + str(rating))
    f.close()
    
    for line in f1:
        restName = line.strip('\n').split('\t')[0]
        if not os.path.isfile("restaurantFiles/otherFiles/" + restName + ".html"): continue
        r = open("restaurantFiles/otherFiles/" + restName + ".html")
        soup = BeautifulSoup(r,'lxml') # parse the html content of the file
        r.close()
        try:
            rev = soup.find('div',{'class':re.compile('rating-info clearfix')})
            rating = rev.find('img',{'class':re.compile('offscreen')})['alt'].split(' ')[0]
        except:
            print("Exception occured")
            rating = 1
        print(restName + '\t' + str(rating))
        f2.write('\n' + restName + '\t' + str(rating))
    f1.close()        

def final_file():
    user_file = open("3 ratings by user.txt")
    rest_file = open("4 avg rest rating.txt")
    final_file = open("5 final file.txt", 'a+')
    df2 = pd.read_table(rest_file, sep = '\t')
    df2 = df2.drop_duplicates()
    rest_file.close()
    flag=0 #to skip first line
    for line in user_file:
        if flag == 0: flag = 1; continue
        restName = line.strip('\n').split('\t')[1]
        print(restName)
        if restName in df2.restName.tolist():
            print(line.strip("\n") + "\t" + str(df2.avgRatingToThisRest[df2.restName==restName].item()))
            final_file.write("\n" + line.strip("\n") + "\t" + str(df2.avgRatingToThisRest[df2.restName==restName].item()))
    final_file.close()
    user_file.close()
    
extract_avg_rest_rating()
final_file()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    