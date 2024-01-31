import scrapy
from scrapy.http import JsonRequest
import pandas as pd

class FindProjectsSpider(scrapy.Spider):
    name = "find_pitches"
    allowed_domains = ["crowdcube.eu"]
    
    def start_requests(self):
            return [JsonRequest(url="https://www.crowdcube.eu/companies",headers = {"x-requested-with": "XMLHttpRequest"})]

    def parse(self, response):
        j = response.json()
        body = scrapy.Selector(text=j["companies"])
        for company in body.css("a.cc-card__link[href^='/companies']::attr(href)").extract():
            yield scrapy.Request(f"https://www.crowdcube.eu{company}",callback=self.follow_pitches,errback=self.eb)
        next = j["cursor"]["next"]
        if next:
            yield JsonRequest(url=f"https://www.crowdcube.eu/companies?cursor={next}",headers = {"x-requested-with": "XMLHttpRequest"})
    
    def follow_pitches(self, response):
        html = response.css("div.cc-panel > table").get()
        df = pd.read_html(html,extract_links="body")[0]
        df.columns = [*df.columns[:-1],"url"]
        df = df.applymap(lambda x:[_ for _ in x if _][-1])
        for i,pitch in df.iterrows():
            yield {"company":response.url,**pitch.to_dict()}


