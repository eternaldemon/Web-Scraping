# -*- coding: utf-8 -*-
"""
Created on Sat Oct 24 12:44:59 2020

@author: eternal_demon(Bhanu)
"""
# Importing required libraries
import pandas as pd
from googlesearch import search


# Reading the given dataset.
data = pd.read_csv('task4data.csv')
print(data.head())
# Function which returns the url for each Google Search Code
def getlink(query):
    for j in search(query,tld="com",num=2,stop=1, pause=2):
        if j.startswith("https://www.oneill.com/"):
            return j
            #print(count)
        else:
            # IF in first  2 urls no url is of www.oneill.com then it returns not found.
            temp = "NOT FOUND"
            return temp
            #print(count)

# Getting link for each Google Search Code and storing it in queryresults.
queries = data['Google Search Code']
queryresults = list()
for query in queries:
    a = getlink(query)
    if(type(a)!=str):
        # If returned value if of None Type that means link not found/product not available on oneill.com
        queryresults.append("NOT FOUND")
        print("NOT FOUND")
    else:
        queryresults.append(a)
        print(a)
    
# Adding the Product Page URL column to given dataset.        
data['Product Page URL'] = queryresults
print(data.head())
# Rewrite the given dataset as we filled the Product Page URL.
data.to_csv('task4data.csv',index=False)




    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

