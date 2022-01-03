import scrapy
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


class PostsSpider(scrapy.Spider):
    name = 'posts'
    logmein = log_data()

    start_urls = [
        logmein['generali_url'],
        logmein['uniqa_url'],
        logmein['warta_url']
    ]


    def parse(self, response):
        page = response.url
        return page

gen_spider = PostsSpider

print(gen_spider.start_urls)