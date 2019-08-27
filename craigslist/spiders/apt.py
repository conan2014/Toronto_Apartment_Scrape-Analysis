# -*- coding: utf-8 -*-
import scrapy
import numpy as np


class AptSpider(scrapy.Spider):
    name = 'apt'
    allowed_domains = ['toronto.craigslist.org']
    start_urls = ['https://toronto.craigslist.org/search/apa?hasPic=1&availabilityMode=0&sale_date=all+dates']

    def parse(self, response):
        listings = response.xpath('//*[@class="result-row"]')
        for listing in listings: 
        	title = listing.xpath('.//*[@class="result-title hdrlnk"]/text()').extract_first()
        	listing_url = listing.xpath('.//*[@class="result-title hdrlnk"]/@href').extract_first()
        	price = listing.xpath('.//*[@class="result-price"]/text()').extract_first().replace('$','')
        	time_posted = listing.xpath('.//*[@class="result-date"]/@datetime').extract_first()

        	housing_info = listing.xpath('.//*[@class="housing"]/text()').extract_first()
        	if housing_info and ('ft' in housing_info.split()[0]): 
        		num_bedrooms = np.nan
        		sqft = housing_info.split()[0][:-2]
        	elif housing_info and ('br' in housing_info.split()[0]) and len(housing_info.split()) == 2: 
        		num_bedrooms = housing_info.split()[0][:-2]
        		sqft = np.nan
        	elif housing_info and ('br' in housing_info.split()[0]) and len(housing_info.split()) > 2:
        		num_bedrooms = housing_info.split()[0][:-2]
        		sqft = housing_info.split()[2][:-2]
        	else: 
        		num_bedrooms = np.nan
        		sqft = np.nan

        	neighborhood_info = listing.xpath('.//*[@class="result-hood"]/text()').extract_first()
        	neighborhood = neighborhood_info.strip().strip('(').strip(')') if neighborhood_info else np.nan

        	yield scrapy.Request(
        		  				listing_url,
        		  				callback = self.parse_listing,
        		  				meta = {
        		  	     				'title': title, 
        		  	     				'listing_url': listing_url, 
        		  	     				'price': price,
        		  	     				'time_posted': time_posted,
        		  	     				'num_bedrooms': num_bedrooms,
        		  	     				'sqft': sqft,
        		  	     				'neighborhood': neighborhood
        		  						}
        						)

        relative_next_url = response.xpath('//*[@class="button next"]/@href').extract_first()
        absolute_next_url = response.urljoin(relative_next_url)
        if absolute_next_url: 
        	yield scrapy.Request(absolute_next_url, callback=self.parse)


    def parse_listing(self, response): 
    	title = response.meta.get('title')
    	listing_url = response.meta.get('listing_url')
    	price = response.meta.get('price')
    	time_posted = response.meta.get('time_posted')
    	num_bedrooms = response.meta.get('num_bedrooms')
    	sqft = response.meta.get('sqft')
    	neighborhood = response.meta.get('neighborhood')
    	latitude = response.xpath('//*[@id="map"]/@data-latitude').extract_first() if response.xpath('//*[@id="map"]/@data-latitude').extract_first() else np.nan
    	longitude = response.xpath('//*[@id="map"]/@data-longitude').extract_first() if response.xpath('//*[@id="map"]/@data-longitude').extract_first() else np.nan
    	description = "".join(line for line in response.xpath('//*[@id="postingbody"]/text()').extract())

    	yield {
    		  'title': title,
    		  'listing_url': listing_url,
    		  'price': price,
    		  'time_posted': time_posted,
    		  'num_bedrooms': num_bedrooms,
    		  'sqft': sqft,
    		  'neighborhood': neighborhood,
    		  'latitude': latitude,
    		  'longitude': longitude,
    		  'description': description
    	}





        
