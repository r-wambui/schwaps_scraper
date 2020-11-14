import csv
import re
import os

import pandas as pd
import scrapy

from cookcounty.items import CookcountyItem

class CookCountyProperty(scrapy.Spider):

    name = "property"

    custom_settings = {

    'FEED_EXPORT_FIELDS': ['ItemID', 'PIN', 'property_location', 'city', 'township', 'propertyclass', 
                        'squarefootage', 'neighboorhood', 'taxcode', 'description', 'age', 'buildingsquarefootage', 
                        'assessmentphase','latest_landav_2020_assessor_valuation', 'latest_buildingav_2020_assessor_valuation',
                        'latest_totalav_2020_assessor_valuation', 'prior_landav_2019_Board_of_Review_Certified', 
                        'prior_buildingav_2019_Board_of_Review_Certified', 'prior_totalav_2019_Board_of_Review_Certified',
                        'estimated_latest_marketvalue', 'estimated_prior_marketvalue',
                         ]
    }
    

    def start_requests(self):
        start_url = "https://www.cookcountyassessor.com/"

        yield scrapy.Request(url=start_url, callback=self.get_pins)

    def get_pins(self, response):
        # Read the csv file containing urls and pins
        collection = pd.read_csv(
            "./data/Elkgrove-township-pin-url-collection-Default - Elkgrove-township-pin-url-collection-Default.csv.csv")

        collection_dict = dict(zip(collection.ItemID, collection.PIN))
        
        file_size = os.path.getsize("Elkgrove_Township.csv")
        if  file_size is not 0:
            crawled_data = pd.read_csv("Elkgrove_Township.csv")
            crawled_pins = crawled_data["PIN"].tolist()
        else:
            crawled_pins = []

        for item_id, pin in collection_dict.items():
            if not pin in crawled_pins:
                property_url = response.url + "pin/{}/print".format(pin)
                yield scrapy.Request(url=property_url, meta={"ItemID": item_id}, callback=self.get_property_details)
                
    def get_property_details(self, response):
        item = CookcountyItem()
        item["ItemID"] = response.meta["ItemID"]
        item["PIN"] = re.search("[\d]+", response.url).group(0)
        location = response.xpath(
            "//div[@class='address']/span/text()").extract()[0].split("●")
        item["property_location"] = location[0]
        item["city"] = location[1].split(",")[0]
        item["township"] = location[2]

        details = response.xpath(
            "//div[@class='property-details-info']/div[@class='detail-row']")
        item["propertyclass"] = details.xpath(
            "./span[@class='detail-row--detail']/text()")[0].extract()
        item["squarefootage"] = details.xpath(
            "./span[@class='detail-row--detail']/text()")[1].extract().replace(",", "")
        item["neighboorhood"] = details.xpath(
            "./span[@class='detail-row--detail']/text()")[2].extract()
        item["taxcode"] = details.xpath(
            "./span[@class='detail-row--detail']/text()")[3].extract()

        item["description"] = response.xpath(
            "//*[normalize-space(text()) = 'Description']/following-sibling::span/text()").extract()
        item["age"] = response.xpath(
            "//*[normalize-space(text()) = 'Age']/following-sibling::span/text()").extract()
        item["buildingsquarefootage"] = response.xpath(
            "//*[text() = 'Building Square Footage']/following-sibling::span/text()").extract()[0].replace(",", "")
        item["assessmentphase"] = response.xpath(
            "//*[text() = 'Assessment Phase']/following-sibling::span/text()").extract()

        # Assessed Valuation
        latest_landav = response.xpath(
            "//*[text() = 'Land Assessed Value']/following-sibling::span[1]/text()").extract()
        if latest_landav:
            item["latest_landav_2020_assessor_valuation"] = latest_landav[0].replace(
                "$", "").replace(",", "")
        
        latest_buildingav = response.xpath(
            "//*[text() = 'Building Assessed Value']/following-sibling::span[1]/text()").extract()
        if latest_buildingav:
            item["latest_buildingav_2020_assessor_valuation"] = latest_buildingav[0].replace(
                "$", "").replace(",", "")

        latest_totalav = response.xpath(
            "//*[text() = 'Total Assessed Value']/following-sibling::span[1]/text()").extract()
        if latest_totalav:
            item["latest_totalav_2020_assessor_valuation"] = latest_totalav[0].replace(
                "$", "").replace(",", "")

        prior_landav = response.xpath(
            "//*[text() = 'Land Assessed Value']/following-sibling::span[2]/text()").extract()
        if prior_landav:
            item["prior_landav_2019_Board_of_Review_Certified"] = prior_landav[0].replace(
                "$", "").replace(",", "")

        prior_buildingav = response.xpath(
            "//*[text() = 'Building Assessed Value']/following-sibling::span[2]/text()").extract()
        if prior_buildingav:
            item["prior_buildingav_2019_Board_of_Review_Certified"] = prior_buildingav[0].replace(
                "$", "").replace(",", "")

        prior_totalav = response.xpath(
            "//*[text() = 'Total Assessed Value']/following-sibling::span[2]/text()").extract()
        if prior_totalav:
            item["prior_totalav_2019_Board_of_Review_Certified"] = prior_totalav[0].replace(
                "$", "").replace(",", "")

        latest_marketvalue = response.xpath(
            "//*[text() = 'Total Estimated Market Value']/following-sibling::span[1]/text()").extract()
        if latest_marketvalue:
            item["estimated_latest_marketvalue"] = latest_marketvalue[0].replace(
                "$", "").replace(",", "")
        
        prior_marketvalue = response.xpath(
            "//*[text() = 'Total Estimated Market Value']/following-sibling::span[2]/text()").extract()
        if prior_marketvalue:
            item["estimated_prior_marketvalue"] = prior_marketvalue[0].replace(
                "$", "").replace(",", "")
        print(item)

        yield item
