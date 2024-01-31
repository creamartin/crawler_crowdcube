import scrapy

from bs4 import BeautifulSoup
from datetime import datetime,timedelta
import re,pandas as pd

def parse_date(date_str):
    try:

        # Parse date in the format '<time datetime="...">...</time>'
        time_match = re.search(r'<time datetime="([^"]+)">([^<]+)</time>', date_str)
        if time_match:
            return pd.to_datetime(time_match.group(1)) 
    except Exception as e:
        return None




class CrowdcubeSpider(scrapy.Spider):
    name = 'crowdcube_old'
    
    def start_requests(self):
        for url in pd.read_csv("./failed.txt",header=None).iloc[:,0].values:
            yield scrapy.Request(url)

    def parse(self, response):
        data = {}
        # Extracting attributes
        data['name'] = response.css("div.cc-pitch__col2 > div > h2::text").get()
        data['url'] = response.url
        data['description'] = response.css("div.pitch-tabs > div > p ::text").get()
        data['status'] = response.css('span.cc-btnTag.cc-btnTag--success::text').get()
        ###
        soup = BeautifulSoup(response.body, 'html.parser')
        dt_elements = soup.find_all('dt')
        dd_elements = soup.find_all('dd')
        attrs = {}
        for dt, dd in zip(dt_elements, dd_elements):
            key = dt.get_text()
            value = str(dd.contents[0]).strip()
            # Parse date if the value looks like a date
            parsed_date = parse_date(value)
            if parsed_date:
                value = parsed_date
            else:
                value = value.strip()
            attrs[key] = value
        data['investment.target'] = attrs["Target"]
        data['equity'] = attrs['Equity on offer']
        data['stats.investors.total'] = attrs["Investors so far"]
        data['stats.investors.last'] = attrs["Last investment"]
        data['stats.investments.largest'] = attrs["Largest"]
        yield data