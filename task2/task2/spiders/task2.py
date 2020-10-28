# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 14:53:25 2020

@author: eternal_demon(Bhanu)
"""
##############################################################################
'''
The showed results on website for all genders around 3199.
But without repetition it is less than that. 
Please do keep this in mind while checking the code.
'''
##############################################################################
#Importing required Libraries and Frameworks
import scrapy

class task2(scrapy.Spider):
    #Start url is taken by applying all genders in the filter column.
    start_urls = ["https://www.blue-tomato.com/de-DE/products/categories/Snowboard+Shop-00000000/gender/boys--girls--men--women/"]
    name  = "task2"
    i = 2
    #baseurl ="https://www.blue-tomato.com/de-AT/products/categories/Snowboard+Shop-00000000/gender/boys--girls--men--women/?page="
    baseurl = "https://www.blue-tomato.com"
    #Parse function for parsing the page
    def parse(self,response):
        # Get the data for name
        name = response.css('#productList > ul>li>span>a').xpath('@data-productname').extract()
        # Get the data for price
        price =  response.xpath('//ul/li/span/span[@class="price"]//text()').extract()
        #Creating a pricelist for prices by removing \n, whitespaces and other unused characters for price data.
        pricelist = list()
        # Get the data for image url
        imageurl = response.css('#productList > ul>li>span.productimage>img').xpath('@data-src').extract()
        # Get the data for product url
        producturl = response.css('#productList > ul>li>span.productdesc>a').xpath('@href').extract()
        # Removing characters from each price string and creating a new pricelist
        for p in price:
            p = str(p)
            p = p.split()
            p = "".join(p)
            p = p[1:].replace(',','.')
            pricelist.append(p)
        
        # Zipping the data so as to yield according to required format
        data = zip(name,pricelist,imageurl,producturl)
        
        for item in data:
            name = item[0]
            # Taking the brand name from product name itself.
            brand = str(name).split(' ')[0]
            # Adding www.blue-tomato.com before each producturl link to complete the url.
            producturl = "www.blue-tomato.com" + item[3]
            result = {'Name':item[0],
                      'Brand':brand,
                      'Price':item[1],
                      'Image Url':item[2],
                      'Product Url': producturl}
            
            yield result
            
        # Parsing the next page by checking whether it is empty or not.
        nextpage = response.css('section.filter>div.pagination>nav>ul>li.next.browse>a').xpath('@href').extract_first()
        
        if nextpage is not None:
            nextpage = self.baseurl + nextpage
            yield response.follow(url = nextpage,callback = self.parse)
                