import scrapy
from scrapy_splash import SplashRequest
from scrapy.crawler import CrawlerProcess
import pandas as pd


pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)
pd.set_option('display.max_columns', None)


def log_data():
    login = {}
    df = pd.read_excel('/run/user/1000/gvfs/smb-share:server=192.168.1.12,share=e/Agent baza/Login_Hasło.xlsx')

    login['generali_url'] = df.iloc[8, 3]
    login['generali_login'] = df.iloc[8, 5]
    login['generali_password'] = df.iloc[8, 6]

    login['uniqa_url'] = 'https://serwis.uniqa.pl/partner'
    login['uniqa_login'] = df.iloc[41, 5]
    login['uniqa_password'] = df.iloc[40, 6]

    login['warta_url'] = df.iloc[42, 3]
    login['warta_login'] = df.iloc[42, 5]
    login['warta_password'] = df.iloc[42, 6]

    return login


class Calculator(scrapy.Spider):
    name = 'calc'

    def start_requests(self):
        logmein = log_data()
        url = logmein['uniqa_url']
        # yield SplashRequest(url=url, callback=self.parse)
        yield scrapy.Request(url)


    def parse(self, response):
        r = response.css('div').getall()
        print(r)

        # for item in r.getall():
    #
    #         # id =username
    #         # id =password

        yield r




process = CrawlerProcess(settings={
    "FEEDS": {
        "items.json": {"format": "json"},
    },
})

process.crawl(Calculator)
process.start()




