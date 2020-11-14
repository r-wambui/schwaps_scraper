import json
import os

import pandas as pd
import scrapy
from scrapy.http import FormRequest

from cookcounty.items import CountyV2Item


class CountyPropertyV2(scrapy.Spider):

    name = "property_v2"

    custom_settings = {
        'FEED_EXPORT_FIELDS': ['PARCEL_NUMBER', 'Address', 'City', 'Neighborhood_code', 'Lot_size', 'Office_Area', 'Exterior_Height',
                               'No_of_Units', 'Overhead_Doors', 'Concrete_SF', 'Asphalt_SF', 'Building_Class', 'Construction',
                               'Effective_Year_Built',  'Gross_Building_Area', 'Photograph', 'Improvement_sketch', 'land_2020',
                               'Improve_2020',  'total_2020', 'type_2020', 'Tax_rate_2020', 'Tax_amount_2020', 'Tax_code_2020',
                               'Est_Market_value_2020', 'land_2019', 'Improve_2019', 'total_2019', 'type_2019', 'Tax_rate_2019',
                               'Tax_amount_2019', 'Tax_code_2019', 'Est_Market_value_2019', 'land_2018', 'Improve_2018', 'total_2018',
                               'type_2018', 'Tax_rate_2018', 'Tax_amount_2018', 'Tax_code_2018', 'Est_Market_value_2018', 'land_2017',
                               'Improve_2017', 'total_2017', 'type_2017', 'Tax_rate_2017', 'Tax_amount_2017', 'Tax_code_2017', 'Est_Market_value_2017'

                               ],
    }


    def start_requests(self):
        start_url = "http://www.addisontownship.com/webdb/sd/addison/assessordb/Search.aspx"

        yield scrapy.Request(url=start_url, callback=self.get_parcels)

    def get_parcels(self, response):
        data_types = {"PARCEL_NUMBER": str}
        parcel_csv = pd.read_csv("./data/ADDISON_PINS.csv", dtype=data_types)
        parcel_numbers = parcel_csv["PARCEL_NUMBER"].tolist()

        file_size = os.path.getsize("Addison_Township.csv")
        if file_size is not 0:
            crawled_data = pd.read_csv(
                "Addison_Township.csv", dtype=data_types)
            crawled_parcels = crawled_data["PARCEL_NUMBER"].tolist()
        else:
            crawled_parcels = []

        for parcel_no in parcel_numbers:
            if not parcel_no in crawled_parcels:

                formdata = {}
                formdata['__VIEWSTATE'] = "/wEPDwUJODk1NTE5MjQ1D2QWAmYPZBYCAgEPZBYCAgUPZBYCAgEPDxYEHgRUZXh0BWBUaGUgcGFyY2VsIG51bWJlciB5b3UgZW50ZXJlZCB3YXMgbm90IHRoZSBjb3JyZWN0IGZvcm1hdCwgcGxlYXNlIGVudGVyIHRoZSBlbnRpcmUgcGFyY2VsIG51bWJlci4eB1Zpc2libGVnZGRktmG3enmYFzCD3HMKqHFaFYzAEh0Gp7I54x+26SvTQaA="
                formdata["__VIEWSTATEGENERATOR"] = "48342B02"
                formdata["__EVENTVALIDATION"] = "/wEdAAhAPZIoVuYsOwOAbhiR1FnzFR16WwdBD2qWVwL1JOEmgMonuYpv+PCKmBZneAHoivME9USfqaycyVYTwgOmP1tSNQ6lykZafP/XyOK1gGuKqjmkXSBHMXLHgVAoxJlrFW+i8Gnx7b0L5rWWHjjEIowms8RKQ9aYfHMIjir6xbggD2gbDTAnJYyWb8TwOrM5rAmdaqjom9gla0FFw/9erbuf"
                formdata["ctl00$contentPageContent$txtParcelNumber"] = parcel_no
                formdata["ctl00$contentPageContent$txtStreetDir"] = ""
                formdata["ctl00$contentPageContent$txtStreetName"] = ""
                formdata["ctl00$contentPageContent$txtCity"] = ""
                formdata["ctl00$contentPageContent$cmdSearch"] = ""
                formdata["ctl00$contentPageContent$cmdSearch"] = "Search"

                meta = {"parcel": parcel_no}

                yield scrapy.FormRequest(url=response.url, method="POST", formdata=formdata, meta=meta, dont_filter=True, callback=self.get_property_details)

    def get_property_details(self, response):
        item = CountyV2Item()
        item["PARCEL_NUMBER"] = response.xpath(
            "//span[@id='contentPageContent_lblParcelNumberValue']/text()").extract()[0].replace("-", "")
        address = response.xpath(
            "//span[@id='contentPageContent_lblAddressValue']/text()").extract()
        if address:
            item["Address"] = address[0].strip()
        item["City"] = response.xpath(
            "//span[@id='contentPageContent_lblCityValue']/text()").extract()
        item["Neighborhood_code"] = response.xpath(
            "//span[@id='contentPageContent_lblNBHDCodeValue']/text()").extract()

        # land data
        item["Lot_size"] = response.xpath(
            "//span[@id='contentPageContent_lblLotDimensionsValue']/text()").extract()

        # Physical characteristics
        item["Office_Area"] = response.xpath(
            "//span[@id='contentPageContent_lblOfficeAreaValue']/text()").extract()
        item["Exterior_Height"] = response.xpath(
            "//span[@id='contentPageContent_lblExtHeightValue']/text()").extract()
        item["No_of_Units"] = response.xpath(
            "//span[@id='contentPageContent_lblNumberOfUnitsValue']/text()").extract()
        item["Overhead_Doors"] = response.xpath(
            "//span[@id='contentPageContent_lblOverHeadDoorsValue']/text()").extract()
        item["Concrete_SF"] = response.xpath(
            "//span[@id='contentPageContent_lblConcreteSFValue']/text()").extract()
        item["Asphalt_SF"] = response.xpath(
            "//span[@id='contentPageContent_lblAsphaltSFValue']/text()").extract()
        item["Building_Class"] = response.xpath(
            "//span[@id='contentPageContent_lblBuildingClassValue']/text()").extract()
        item["Construction"] = response.xpath(
            "//span[@id='contentPageContent_lblConstructionCommValue']/text()").extract()
        item["Effective_Year_Built"] = response.xpath(
            "//span[@id='contentPageContent_lblYearBuiltComValue']/text()").extract()
        item["Gross_Building_Area"] = response.xpath(
            "//span[@id='contentPageContent_lblGrossBldgAreaValue']/text()").extract()

        # photograph
        item["Photograph"] = response.xpath(
            "//img[@id='contentPageContent_imgPhotograph']/@src").extract()

        # Improvement sketch
        item["Improvement_sketch"] = response.xpath(
            "//img[@id='contentPageContent_imgSketch']/@src").extract()

        # assessment
        # 2020
        table = response.xpath("//table[@class='resulttable']")
        tr_2020 = table.xpath(".//tr[2]")
        item["land_2020"], item["Improve_2020"], item["total_2020"], item["type_2020"], item["Tax_rate_2020"], item[
            "Tax_amount_2020"], item["Tax_code_2020"], item["Est_Market_value_2020"] = CountyPropertyV2.get_assessment_per_year(tr_2020)

        # 2019
        tr_2019 = table.xpath(".//tr[3]")
        item["land_2019"], item["Improve_2019"], item["total_2019"], item["type_2019"], item["Tax_rate_2019"], item[
            "Tax_amount_2019"], item["Tax_code_2019"], item["Est_Market_value_2019"] = CountyPropertyV2.get_assessment_per_year(tr_2019)

        # 2018
        tr_2018 = table.xpath(".//tr[4]")
        item["land_2018"], item["Improve_2018"], item["total_2018"], item["type_2018"], item["Tax_rate_2018"], item[
            "Tax_amount_2018"], item["Tax_code_2018"], item["Est_Market_value_2018"] = CountyPropertyV2.get_assessment_per_year(tr_2018)

        # 2017
        tr_2017 = table.xpath(".//tr[5]")
        item["land_2017"], item["Improve_2017"], item["total_2017"], item["type_2017"], item["Tax_rate_2017"], item[
            "Tax_amount_2017"], item["Tax_code_2017"], item["Est_Market_value_2017"] = CountyPropertyV2.get_assessment_per_year(tr_2017)

        yield item

    @staticmethod
    def get_assessment_per_year(year_row):
        land = year_row.xpath(".//td[2]/text()").extract()[0].strip()
        improve = year_row.xpath(".//td[3]/text()").extract()[0].strip()
        total = year_row.xpath(".//td[4]/text()").extract()[0].strip()
        Type = year_row.xpath(".//td[5]/text()").extract()[0].strip()
        Tax_rate = year_row.xpath(".//td[6]/text()").extract()[0].strip()
        Tax_amount = year_row.xpath(".//td[7]/text()").extract()[0].strip()
        Tax_code = year_row.xpath(".//td[8]/text()").extract()[0].strip()
        Est_Market_value = year_row.xpath(
            ".//td[9]/text()").extract()[0].strip()

        return (land, improve, total, Type, Tax_rate, Tax_amount, Tax_code, Est_Market_value)
