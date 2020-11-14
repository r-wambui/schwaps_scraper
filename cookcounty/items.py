# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

from collections import OrderedDict

class OrderedItem(scrapy.Item):
    def __init__(self, *args, **kwargs):
        self._values = OrderedDict()
        if args or kwargs:  # avoid creating dict for most common case
            for k, v in six.iteritems(dict(*args, **kwargs)):
                self[k] = v


class CookcountyItem(scrapy.Item):
    # define the fields for your item here like:
    
    ItemID = scrapy.Field()
    PIN = scrapy.Field()
    property_location = scrapy.Field()
    city = scrapy.Field()
    township = scrapy.Field()
    propertyclass = scrapy.Field()
    squarefootage = scrapy.Field()
    neighboorhood = scrapy.Field()
    taxcode = scrapy.Field()
    description = scrapy.Field()
    age = scrapy.Field()
    buildingsquarefootage=scrapy.Field()
    assessmentphase = scrapy.Field()
    estimated_latest_marketvalue =scrapy.Field()
    estimated_prior_marketvalue = scrapy.Field()
    latest_totalav_2020_assessor_valuation=scrapy.Field()
    prior_totalav_2019_Board_of_Review_Certified=scrapy.Field()
    latest_landav_2020_assessor_valuation=scrapy.Field()
    prior_landav_2019_Board_of_Review_Certified=scrapy.Field()
    latest_buildingav_2020_assessor_valuation=scrapy.Field()
    prior_buildingav_2019_Board_of_Review_Certified=scrapy.Field()


class CountyV2Item(OrderedItem):
    PARCEL_NUMBER = scrapy.Field()
    Address = scrapy.Field()
    City = scrapy.Field()
    Neighborhood_code = scrapy.Field()
    Lot_size = scrapy.Field()
    Office_Area = scrapy.Field()
    Exterior_Height = scrapy.Field()
    No_of_Units = scrapy.Field()
    Overhead_Doors = scrapy.Field()
    Concrete_SF = scrapy.Field()
    Asphalt_SF = scrapy.Field()
    Building_Class =scrapy.Field()
    Construction = scrapy.Field()
    Effective_Year_Built = scrapy.Field()
    Gross_Building_Area = scrapy.Field()
    Photograph = scrapy.Field()
    Improvement_sketch = scrapy.Field()
    land_2020 = scrapy.Field()
    Improve_2020 = scrapy.Field()
    total_2020 = scrapy.Field()
    type_2020 = scrapy.Field()
    Tax_rate_2020 = scrapy.Field()
    Tax_amount_2020 = scrapy.Field()
    Tax_code_2020 = scrapy.Field()
    Est_Market_value_2020 = scrapy.Field()
    land_2019 = scrapy.Field()
    Improve_2019 = scrapy.Field()
    total_2019 = scrapy.Field()
    type_2019 = scrapy.Field()
    Tax_rate_2019 = scrapy.Field()
    Tax_amount_2019 = scrapy.Field()
    Tax_code_2019 = scrapy.Field()
    Est_Market_value_2019 = scrapy.Field()
    land_2018 = scrapy.Field()
    Improve_2018 = scrapy.Field()
    total_2018 = scrapy.Field()
    type_2018 = scrapy.Field()
    Tax_rate_2018 = scrapy.Field()
    Tax_amount_2018 = scrapy.Field()
    Tax_code_2018 = scrapy.Field()
    Est_Market_value_2018 = scrapy.Field()
    land_2017 = scrapy.Field()
    Improve_2017 = scrapy.Field()
    total_2017 = scrapy.Field()
    type_2017 = scrapy.Field()
    Tax_rate_2017 = scrapy.Field()
    Tax_amount_2017 = scrapy.Field()
    Tax_code_2017 = scrapy.Field()
    Est_Market_value_2017 = scrapy.Field()

class CalendarItem(scrapy.Item):
    url = scrapy.Field()
    html = scrapy.Field()
    township =scrapy.Field()
    reassessment_mail_date = scrapy.Field()
    last_date_appeals = scrapy.Field()
    date_a_roll_certified = scrapy.Field()
    date_a_roll_published = scrapy.Field()
    board_of_review_filling_dates = scrapy.Field()
    review_pass = scrapy.Field()

