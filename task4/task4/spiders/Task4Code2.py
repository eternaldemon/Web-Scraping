"""
Created on Sat Oct 24 12:59:59 2020

@author: eternal_demon(Bhanu)
"""
##############################################################################

# This Code parses the site to get only the price of the required item.
# Task4Code1 updates the Product Page Url in the given data file itself.
# Run Task4Code1.py separately before executing the following code through terminal/cmd.
#############################################################################

# Importing required Libraries
import scrapy
import pandas as pd

class task4(scrapy.Spider):
    # Defining the spider name and creating a price list
    name = "task4"
    pricelist = list()
        
    # Function that starts parsing according to the applied conditions.
    def start_requests(self):
        data = pd.read_csv('task4data.csv')
        # Take the PRoduct Page URL from the datafile into queryresults list.
        queryresults = data['Product Page URL']
        queryresults = list(queryresults)
        for query in queryresults:
            # Finding the index for each query using Google Search Code.
            queryindex = data.loc[data['Product Page URL']==query].index
            # and creating a dictionary for each of them so that it can be passed on for required yield format.
            details = {'Brand':data['Brand'].iloc[queryindex],
               'Reference':data['Reference'].iloc[queryindex],
               'Google Search Code':data['Google Search Code'].iloc[queryindex],
               'Category':data['Category'].iloc[queryindex],
               'Name':data['Name'].iloc[queryindex],
               'Product Page URL':data['Product Page URL'].iloc[queryindex]}
            if query!="NOT FOUND":
                # Here if the link of product is FOUND on oneill then we pass
                #the details through meta argument and parse that page. 
                yield scrapy.Request(url=query,callback=self.parse,meta=details)
            else:
                # Else we append NA since link not found so can't get the price.
                self.pricelist.append("NA")
                
    def parse(self,response):
        # Getting price from response.
        price = response.xpath('/html/body/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div/div/span/span[2]/span').xpath('@content').extract_first()        
        # Getting other required data from meta tag.
        Brand = response.meta.get('Brand')
        Reference = response.meta.get('Reference')
        GoogleSearchCode = response.meta.get('Google Search Code')
        Category= response.meta.get('Category')
        Name = response.meta.get('Name')
        Url = response.meta.get('Product Page URL')
        
        # Zipping so as to get the required output format.
        d = zip(Brand,Reference,GoogleSearchCode,Category,Name,Url)
        for item in d:
            info = {'Brand':item[0],
                  'Reference': item[1],
                  'Google Search Code': item[2],
                  'Category': item[3],
                  'Name': item[4],
                  'Product Page URL': item[5],
                  'Price': price}
            yield info


    