import scrapy


class CountrycodeSpider(scrapy.Spider):
    name = "countrycode"
    allowed_domains = ["www.crowdcube.com"]
    start_urls = ["https://www.crowdcube.com"]
    def should_abort_request(request):
        return (
            request.resource_type == "image"
            or ".jpg" in request.url
        )

    custom_settings = {
        "DOWNLOAD_HANDLERS": {
            "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        },
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        "PLAYWRIGHT_ABORT_REQUEST" : should_abort_request,
        "LOG_LEVEL":"ERROR"
    
    }
    countrylist = [[1.0, 'https://www.crowdcube.eu/companies/cutbox-barbers/pitches/lKnKBq'],
                   [16.0, 'https://www.crowdcube.eu/companies/playerhunter/pitches/qrrBkq'],
                   [23.0, 'https://www.crowdcube.eu/companies/cowboy/pitches/lR0g0b'],
                   [40.0, 'https://www.crowdcube.eu/companies/plantx-life-inc/pitches/bwGRob'],
                   [42.0, 'https://www.crowdcube.eu/companies/nothing/pitches/bdp0jb'],
                   [60.0, 'https://www.crowdcube.eu/companies/ooono/pitches/lRo6gZ'],
                   [69.0, 'https://www.crowdcube.eu/companies/bolt/pitches/lmX7Rq'],
                   [75.0, 'https://www.crowdcube.eu/companies/ismo/pitches/q4MW6l'],
                   [82.0, 'https://www.crowdcube.eu/companies/clue/pitches/l8a3kZ'],
                   [84.0,
                    'https://www.crowdcube.eu/companies/digital-asset-management-dam/pitches/Z1X5gl'],
                   [106.0, 'https://www.crowdcube.eu/companies/innov8-creative/pitches/bLPrpb'],
                   [122.0, 'https://www.crowdcube.eu/companies/mintos/pitches/qDJxrZ'],
                   [129.0, 'https://www.crowdcube.eu/companies/governance-com/pitches/b0erBq'],
                   [156.0, 'https://www.crowdcube.eu/companies/baqme/pitches/qD03Wq'],
                   [166.0, 'https://www.crowdcube.eu/companies/kitemill/pitches/bk8kGq'],
                   [178.0,
                    'https://www.crowdcube.eu/companies/goparity-impact-finance/pitches/qaED5q'],
                   [198.0, 'https://www.crowdcube.eu/companies/arival-bank/pitches/Z5nARb'],
                   [205.0,
                    'https://www.crowdcube.eu/companies/vegan-food-club-s-l/pitches/bvLzVl'],
                   [211.0, 'https://www.crowdcube.eu/companies/hooked-foods/pitches/bJ1kdZ'],
                   [212.0, 'https://www.crowdcube.eu/companies/yasai/pitches/lR0JYb'],
                   [231.0, 'https://www.crowdcube.eu/companies/upflex-inc/pitches/lz9BWq']]

    


    def start_requests(self):
        for cc, url in self.countrylist:
            yield scrapy.Request(url, self.parse, meta={"cc": int(cc), "playwright": True})

    def parse(self, response):
        try:
            yield({response.css('span[data-analytics="country"]::text').get():response.meta["cc"]})
        except:
            pass