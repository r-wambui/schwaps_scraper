import scrapy
import os

from cookcounty.items import CalendarItem


try:
    os.remove("Calendar.csv")
except OSError:
    pass

class Calendar(scrapy.Spider):
    
    name = "calendar"

    custom_settings = {
        'FEED_EXPORT_FIELDS' : ["township", "reassessment_mail_date", "last_date_appeals", "date_a_roll_certified",
                                "date_a_roll_published", "board_of_review_filling_dates", "review_pass"]
    }

    def start_requests(self):

        start_url  = "https://www.cookcountyassessor.com/assessment-calendar-and-deadlines"

        yield scrapy.Request(url=start_url, callback=self.get_dates)

    def get_dates(self, response):
        item = CalendarItem()
        item['url'] = response.url
        item['html'] = response.body
        tables = response.xpath("//figure[@class='fig-table']/table")
        for table in tables:
            for row in table.xpath(".//tbody/tr"):

                item["township"] = row.xpath("./td[1]//strong/text()|./td[1]//b/text()").extract()
                item["reassessment_mail_date"] = row.xpath("./td[2]/text()").extract()
                item["last_date_appeals"] = row.xpath("./td[3]/text()").extract()
                item["date_a_roll_certified"] = row.xpath("./td[4]/text()").extract()[0].strip()
                item["date_a_roll_published"] = row.xpath("./td[5]/text()").extract()[0].strip()
                item["board_of_review_filling_dates"]  = row.xpath("./td[6]//text()").extract()[0].strip()
                item["review_pass"] = row.xpath("./td[7]//text()").extract()
                
                yield item
