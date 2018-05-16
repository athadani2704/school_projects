# -*- coding: utf-8 -*-
"""
This file clubs all the three final files to create a final dataset that is then
used to train and test the model (70-30%) being the ratio.
Created on Sat Nov 25 13:27:48 2017

@author: Anil
"""

from sklearn import preprocessing
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
import pandas as pd
from sklearn.neural_network import MLPClassifier ###########for neural network
#from sklearn.neighbors import KNeighborsClassifier ################## for kNN
#def convert_to_ids(df):
#    userIds = 0
#    pass

file1 = open('5 final file Indian.txt')
file2 = open('5 final file Japanese.txt')
file3 = open('5 final file Italian.txt')
df1 = pd.read_table(file1, sep = '\t')
df2 = pd.read_table(file2, sep = '\t')
df3 = pd.read_table(file3, sep = '\t')
file1.close()
file2.close()
file3.close()
#file = open('5 final file.txt')
#df = pd.read_table(file, sep = '\t')
#file.close()
df = df1.append(df2, ignore_index = True)
df = df.append(df3, ignore_index = True)
le = preprocessing.LabelEncoder()
df.userName = le.fit_transform(df.userName)
df.restName = le.fit_transform(df.restName)
df = df.drop_duplicates()
df1 = df.copy()
for i in df.columns[2:5]:
    df1.loc[df1[i]<3,i] = -1
    df1.loc[df1[i]==3,i] = 0
    df1.loc[df1[i]>3,i] = 1
#df = df.iloc[:,1:5]
#df = convert_to_ids(df)
train = df1.sample(int(0.7*len(df1)))
test = df1[df1.apply(lambda x: x.values.tolist() not in train.values.tolist(), axis=1)]

clf = RandomForestClassifier(max_depth=600, max_features='log2', min_samples_split=180, random_state=150, n_estimators=2000, criterion='entropy')
#clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)
#clf = KNeighborsClassifier(n_neighbors=3) # for kNN
#train all classifier on the same datasets
clf.fit(train.iloc[:,train.columns!='ratingToRest'],train.ratingToRest)

#use hard voting to predict (majority voting)
pred=clf.predict(test.iloc[:,test.columns!='ratingToRest'])

#print accuracy
print (accuracy_score(pred,test.ratingToRest))
