# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 17:24:22 2020

@author: eternal_demon
"""
# Importing required libraries
import scrapy
import time

class task1(scrapy.Spider):
    #Defining name of spider, starturls, count i and baseurl
    name = "task1"
    # Start url is the url for men shoes at farfetch
    start_urls=["https://www.farfetch.com/de/shopping/men/shoes-2/items.aspx"]
    i=95
    baseurl = "https://www.farfetch.com/de/shopping/men/shoes-2/items.aspx"
    def parse(self,response):
        # Getting names of required products
        name = response.css('li>a>div>img').xpath('@alt').extract()
        # Getting further needed values for the data
        brand = response.css('ul>li>a>div>h3::text').getall()
        price = response.css('li>a>div>div>meta').xpath('@content').extract()[1::2]
        imageurl = response.css('li>a>meta').xpath('@content').extract()
        producturl = response.css('li>a[class="_5ce6f6"]').xpath('@href').extract()

        # Zipping the required values so as to yield in the asked form.
        data = zip(name,brand,price,imageurl,producturl)
        
        for item in data:
            # Processing producturl and completing it
            purl = "https://www.farfetch.com" + str(item[4])
            result = {'Name':item[0],
                      'Brand':item[1],
                      'Price':item[2],
                      'Image URL':item[3],
                      'Product URL':purl}
            yield result
         
        # Code which checks if next page exists, if so it gets parsed.    
        p1= "?page="
        p2 ="&view=180&scale=282"
        nextpage = self.baseurl + p1 + str(self.i) + p2
        if nextpage is not None and self.i>=1:
            self.i = self.i - 1
            #time.sleep(1)
            yield response.follow(nextpage,callback= self.parse)
            