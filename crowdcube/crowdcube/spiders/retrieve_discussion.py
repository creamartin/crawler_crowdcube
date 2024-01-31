import scrapy
from scrapy.selector import Selector
from scrapy.http import JsonRequest
import pandas as pd
from scrapy.loader import ItemLoader
from crowdcube.items import CommentItem 
from tqdm import tqdm

def extract_cookies(cookie_str):
    #cookies = 'ajs_anonymous_id=ad322b6c-ced1-4450-81c1-1ad094b8c3be; _hp2_props.25681358=%7B%22Browser%20languages%22%3A%22en%22%7D; cc_country=DE; OptanonAlertBoxClosed=2023-07-26T10:52:12.915Z; __stripe_mid=d243d6bc-2f44-4e1a-a44c-cbaf2c163cbc7155e6; ajs_user_id=Z1az33; user_marketing_preferences=1; _gid=GA1.2.298737321.1691400152; api_url=https%3A%2F%2Fapi.crowdcube.com; base_domain=.crowdcube.eu; ab.storage.deviceId.a726ae29-ef5c-4206-830b-2c64f0dee60d=%7B%22g%22%3A%22d98f673f-5bb1-12c0-c435-428c1887ad0e%22%2C%22c%22%3A1690555075660%2C%22l%22%3A1691596106277%7D; ab.storage.userId.a726ae29-ef5c-4206-830b-2c64f0dee60d=%7B%22g%22%3A%22Z1az33%22%2C%22c%22%3A1690555075663%2C%22l%22%3A1691596106277%7D; ln_or=eyI0NzA3MCI6ImQifQ%3D%3D; __stripe_sid=de75b60d-4161-46d3-b0c8-c2ed4faa2587ebf09d; _hp2_ses_props.25681358=%7B%22ts%22%3A1691596106492%2C%22d%22%3A%22www.crowdcube.eu%22%2C%22h%22%3A%22%2Fcompanies%2Fbasket%2Fpitches%2Fqr9vzb%2Fupdates%22%7D; craftSiteHandle=en-eu; CRAFT_CSRF_TOKEN=b3fe715d7517360782222f13e1307255b938fb45ce2a0f1eb1d0015768dcae2aa%3A2%3A%7Bi%3A0%3Bs%3A16%3A%22CRAFT_CSRF_TOKEN%22%3Bi%3A1%3Bs%3A40%3A%22toC71_KjdddygQa9bimWtjMTPEhw69gHQoZC8PWG%22%3B%7D; CROWDCUBE=1329pi6cr3sme3ftvd8o2o2j93; ab.storage.sessionId.a726ae29-ef5c-4206-830b-2c64f0dee60d=%7B%22g%22%3A%2291c92a3e-81cc-d9e5-273a-c06ea15fa40f%22%2C%22e%22%3A1691598750752%2C%22c%22%3A1691596106277%2C%22l%22%3A1691596950752%7D; _uetsid=efb181e0350311eebeb0f7d1785820bd; _uetvid=7427cc302ba211eeb40a29c61034fb42; _hp2_id.25681358=%7B%22userId%22%3A%222334451196550981%22%2C%22pageviewId%22%3A%222493360619708858%22%2C%22sessionId%22%3A%22313298452552960%22%2C%22identity%22%3A%22Z1az33%22%2C%22trackerVersion%22%3A%224.0%22%2C%22identityField%22%3Anull%2C%22isIdentified%22%3A1%7D; _ga_J56X72J1ZN=GS1.1.1691596106.37.1.1691596951.2.0.0; _ga=GA1.1.1026549676.1690368723; OptanonConsent=isGpcEnabled=0&datestamp=Wed+Aug+09+2023+17%3A02%3A32+GMT%2B0100+(Western+European+Summer+Time)&version=202303.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=4a6d4398-be0a-4e90-af3e-18ed6efc2f49&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1%2CC0005%3A1&geolocation=PT%3B15&AwaitingReconsent=false; auth_token=j2JA8XB4v3YLZbo0474svqogYwcdzKt7mkkmVOlG; explore_navigation=%7B%22token%22%3A%228f5282c7dff6e280bf1e08cb91957ac20e5cdf96e3b134d943111586b8885895%22%2C%22avatar%22%3A%22https%3A%5C%2F%5C%2Fimages.crowdcube.com%5C%2Funsafe%5C%2F40x40%5C%2Fhttps%3A%5C%2F%5C%2Flh3.googleusercontent.com%5C%2Fa%252FAGNmyxaiqI5D6O5yDNGRllzDYOFcZfUc-7xZ1iVrF6elpuA%253Ds100%253Fsz%253D1920%22%2C%22verified%22%3Atrue%2C%22has_pitch%22%3Afalse%2C%22logged_in_via_proxy%22%3Afalse%2C%22web_id%22%3A%22Z1az33%22%7D; cc_cached_session={"session":{"authenticated":"LI","userId":"Z1az33","username":"MK5390","email":"martin42koch@gmail.com","requiresEmailVerification":false,"hasEmailVerificationToken":true,"requiresAmlAction":false,"hasOpportunity":false,"avatar":"https://images.crowdcube.com/unsafe/fit-in/120x120/https://lh3.googleusercontent.com/a%2FAGNmyxaiqI5D6O5yDNGRllzDYOFcZfUc-7xZ1iVrF6elpuA%3Ds100%3Fsz%3D1920","locale":"en-EU","failedPayments":false,"failedPaymentCompany":"","requiresRecategorisation":false,"requiresAssessment":false},"timestamp":"Wed Aug 09 2023 17:03:10 GMT+0100 (Western European Summer Time)"}'
    d = {}
    for c in cookie_str.split(";"):
        s = c.split("=")
        d[s[0].strip()]=s[1].strip()
    return d


class FindProjectsSpider(scrapy.Spider):
    name = "retrieve_discussion"
    allowed_domains = ["crowdcube.eu"]
    headers = {"x-requested-with": "XMLHttpRequest"}
    # maybe required to manually reconstruct cookies e.g. with extract_cookies()
    cookies = {'ajs_anonymous_id': 'ad322b6c-ced1-4450-81c1-1ad094b8c3be', '_hp2_props.25681358': '%7B%22Browser%20languages%22%3A%22en%22%7D', 'cc_country': 'DE', 'OptanonAlertBoxClosed': '2023-07-26T10:52:12.915Z', '__stripe_mid': 'd243d6bc-2f44-4e1a-a44c-cbaf2c163cbc7155e6', 'ajs_user_id': 'Z1az33', 'user_marketing_preferences': '1', '_gid': 'GA1.2.298737321.1691400152', 'api_url': 'https%3A%2F%2Fapi.crowdcube.com', 'base_domain': '.crowdcube.eu', 'ab.storage.deviceId.a726ae29-ef5c-4206-830b-2c64f0dee60d': '%7B%22g%22%3A%22d98f673f-5bb1-12c0-c435-428c1887ad0e%22%2C%22c%22%3A1690555075660%2C%22l%22%3A1691596106277%7D', 'ab.storage.userId.a726ae29-ef5c-4206-830b-2c64f0dee60d': '%7B%22g%22%3A%22Z1az33%22%2C%22c%22%3A1690555075663%2C%22l%22%3A1691596106277%7D', 'ln_or': 'eyI0NzA3MCI6ImQifQ%3D%3D', '__stripe_sid': 'de75b60d-4161-46d3-b0c8-c2ed4faa2587ebf09d', '_hp2_ses_props.25681358': '%7B%22ts%22%3A1691596106492%2C%22d%22%3A%22www.crowdcube.eu%22%2C%22h%22%3A%22%2Fcompanies%2Fbasket%2Fpitches%2Fqr9vzb%2Fupdates%22%7D', 'craftSiteHandle': 'en-eu', 'CRAFT_CSRF_TOKEN': 'b3fe715d7517360782222f13e1307255b938fb45ce2a0f1eb1d0015768dcae2aa%3A2%3A%7Bi%3A0%3Bs%3A16%3A%22CRAFT_CSRF_TOKEN%22%3Bi%3A1%3Bs%3A40%3A%22toC71_KjdddygQa9bimWtjMTPEhw69gHQoZC8PWG%22%3B%7D', 'CROWDCUBE': '1329pi6cr3sme3ftvd8o2o2j93', 'ab.storage.sessionId.a726ae29-ef5c-4206-830b-2c64f0dee60d': '%7B%22g%22%3A%2291c92a3e-81cc-d9e5-273a-c06ea15fa40f%22%2C%22e%22%3A1691598750752%2C%22c%22%3A1691596106277%2C%22l%22%3A1691596950752%7D', '_uetsid': 'efb181e0350311eebeb0f7d1785820bd', '_uetvid': '7427cc302ba211eeb40a29c61034fb42', '_hp2_id.25681358': '%7B%22userId%22%3A%222334451196550981%22%2C%22pageviewId%22%3A%222493360619708858%22%2C%22sessionId%22%3A%22313298452552960%22%2C%22identity%22%3A%22Z1az33%22%2C%22trackerVersion%22%3A%224.0%22%2C%22identityField%22%3Anull%2C%22isIdentified%22%3A1%7D', '_ga_J56X72J1ZN': 'GS1.1.1691596106.37.1.1691596951.2.0.0', '_ga': 'GA1.1.1026549676.1690368723', 'OptanonConsent': 'isGpcEnabled', 'auth_token': 'j2JA8XB4v3YLZbo0474svqogYwcdzKt7mkkmVOlG', 'explore_navigation': '%7B%22token%22%3A%228f5282c7dff6e280bf1e08cb91957ac20e5cdf96e3b134d943111586b8885895%22%2C%22avatar%22%3A%22https%3A%5C%2F%5C%2Fimages.crowdcube.com%5C%2Funsafe%5C%2F40x40%5C%2Fhttps%3A%5C%2F%5C%2Flh3.googleusercontent.com%5C%2Fa%252FAGNmyxaiqI5D6O5yDNGRllzDYOFcZfUc-7xZ1iVrF6elpuA%253Ds100%253Fsz%253D1920%22%2C%22verified%22%3Atrue%2C%22has_pitch%22%3Afalse%2C%22logged_in_via_proxy%22%3Afalse%2C%22web_id%22%3A%22Z1az33%22%7D', 'cc_cached_session': '{"session":{"authenticated":"LI","userId":"Z1az33","username":"MK5390","email":"martin42koch@gmail.com","requiresEmailVerification":false,"hasEmailVerificationToken":true,"requiresAmlAction":false,"hasOpportunity":false,"avatar":"https://images.crowdcube.com/unsafe/fit-in/120x120/https://lh3.googleusercontent.com/a%2FAGNmyxaiqI5D6O5yDNGRllzDYOFcZfUc-7xZ1iVrF6elpuA%3Ds100%3Fsz%3D1920","locale":"en-EU","failedPayments":false,"failedPaymentCompany":"","requiresRecategorisation":false,"requiresAssessment":false},"timestamp":"Wed Aug 09 2023 17:03:10 GMT+0100 (Western European Summer Time)"}'}            
    
    def start_requests(self):
            urls = pd.read_json("/Users/martin/Documents/__HIWI/23:07 crowdcube/data/cc_min.json").url.dropna().astype(str).values
            #urls = ["https://www.crowdcube.eu/companies/brewdog-plc-1/pitches/lKADKb"]
            for url in tqdm(urls): 
                #yield JsonRequest(f"{url}/discussions",cookies=self.cookies, headers=self.headers ,callback=self.json_posts)
                yield JsonRequest(f"{url}/updates",cookies=self.cookies, headers=self.headers ,callback=self.json_posts)

    def json_posts(self, response):
        j = response.json()
        # the *_ordering is required because the date value is ambiguous for older entries
        last_i = response.meta.get("post_ordering",-1)
        discussions = Selector(text=j["posts"]).css('a.cc-discussion::attr(href)').getall()
        for i,discussion_href in enumerate(discussions,start=last_i+1):
            url = f"https://www.crowdcube.eu{discussion_href}"
            meta = {"post_ordering":i}
            yield scrapy.Request(url,cookies=self.cookies,meta=meta,callback=self.html_post,dont_filter=True)
        #follow meta
        if j["meta"]["cursor"]["next"]:
            next_url = f"{response.url.split('?')[0]}?cursor={j['meta']['cursor']['next']}"
            yield JsonRequest(next_url,cookies=self.cookies, headers=self.headers,meta=meta, callback=self.json_posts,dont_filter=True)    

    def html_post(self, response):
        post_loader = ItemLoader(item=CommentItem(), selector=response.css('div.cc-discussionHeader'))
        id = response.url.split("/")[-1]
        post_loader.add_value('id', id)
        post_loader.add_value('parent', response.url.split("/")[-1])
        post_loader.add_value('pitch', response.url.split("/discussions")[0])
        post_loader.add_css('title', 'h3.cc-discussionHeader__title ::text')
        post_loader.add_css('author', 'span.cc-discussionHeader__meta--listItem:nth-child(1)::text')
        post_loader.add_css('date', 'span.cc-discussionHeader__meta--listItem:nth-child(2)::text')
        post_loader.add_css('replies', 'span.cc-discussionHeader__meta--replies::text',re=r'\d+')
        post_loader.add_css('content', 'div.cc-post__content ::text')
        meta = {
            "id":id,
            "post_ordering":response.meta["post_ordering"],
            "reply_ordering" : -1,
        }
        yield meta | dict(post_loader.load_item())
        yield JsonRequest(response.request.url,cookies=self.cookies, headers=self.headers,meta=meta, callback=self.json_replies,dont_filter=True)    
    
    def json_replies(self,response):
        j = response.json()
        #extract comments
        previous_i = response.meta.get("reply_ordering",-1)
        replies = Selector(text=j["comments"]).css('div.cc-post')
        for i,reply in enumerate(replies,start=previous_i+1):
            reply_loader = ItemLoader(item=CommentItem(), selector=reply)
            reply_loader.add_css('id', 'div::attr(id)')
            reply_loader.add_value("parent", response.meta["id"])
            reply_loader.add_value('pitch', response.url.split("/discussions")[0])
            reply_loader.add_css('author', 'span.cc-post__metaListItem:nth-child(1)::text')
            reply_loader.add_css('date', 'span.cc-post__metaListItem:nth-child(2)::text')
            reply_loader.add_css('content','div.cc-post__content p ::text')
            meta = {
                "id":response.meta["id"],
                "post_ordering":response.meta["post_ordering"],
                "reply_ordering" : i,
            }
            yield meta | dict(reply_loader.load_item())
        #follow meta
        if j["meta"]["cursor"]["next"]:
            next_url = f"{response.url.split('?')[0]}?cursor={j['meta']['cursor']['next']}"
            yield JsonRequest(next_url,cookies=self.cookies, headers=self.headers,meta=meta, callback=self.json_replies)