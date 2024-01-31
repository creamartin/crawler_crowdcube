import scrapy
from scrapy.http import JsonRequest,FormRequest
from itemadapter import ItemAdapter
import json,pandas as pd

class FindProjectsSpider(scrapy.Spider):
    name = "retrieve_pitches"
    allowed_domains = ["crowdcube.eu"]
    
    def start_requests(self):
            for url in pd.read_json("./pitches_meta.json").url.values:
                yield scrapy.Request(url,callback=self.parse_company,meta={"src_url":url})

    def parse_company(self, response):
        try:
            s = response.css("script#__NEXT_DATA__::text").extract()[0]
            j=json.loads(s)
            props=j["props"]["pageProps"]
            assert props["initialState"]["opportunity"]["opportunity"]
            yield {"src_url":response.meta["src_url"], **props}
        except:
            with open("./failed.txt","a") as f:
                print(response.url,file=f)
