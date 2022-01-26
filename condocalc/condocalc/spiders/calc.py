import scrapy
from scrapy_splash import SplashRequest
from scrapy.crawler import CrawlerProcess
from scrapy.http import Request
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
import time
import pandas as pd
import json
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from scrapy.selector import Selector


import scrapy.spiders
print(scrapy.spiders.__file__)


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
    allowed_domains = ['portal.generali.pl']
    start_urls = [
        'https://portal.generali.pl/auth/login',
                  # 'https://portal.generali.pl/auth/login?service=https%3A%2F%2Fportal.generali.pl%2Flogin%2Fcas',
                # 'https://portal.generali.pl/frontend/'
                  ]


    def parse(self, response):
        # print(response.request.meta['driver'].title)
        url = 'https://portal.generali.pl/auth/login'
        headers = {
            "Connection": "keep-alive",
            "Cache-Control": "max-age=0",
            "sec-ch-ua": "\" Not;A Brand\";v=\"99\", \"Google Chrome\";v=\"97\", \"Chromium\";v=\"97\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Linux\"",
            "Upgrade-Insecure-Requests": "1",
            "Origin": "https://portal.generali.pl",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document",
            "Referer": "https://portal.generali.pl/auth/login",
            "Accept-Language": "en-US,en;q=0.9"
        }

        cookies = {
            "JSESSIONID": "34B5412D413876B1604394E2E95DCEBC",
            "_ga": "GA1.3.1234009803.1641743650",
            "NSC_JOzvrmclejkrmuacaf5zxmeqm5pnbdE": "14b5a3d944667550c217c97f381dc3e805456bef57d91243775bafaf4ea6b81b11e818f7",
            "NSC_PVU.WJQ.QPSUBM.TTM_QPSUBM.BVUI": "14b5a3d9d92a5c18582d4d9822fe3aa442fb4e5397eb62526c5b939c0cff118583416472",
            "NSC_JOnilpxsdjux53zdxv2lagbrewlxmeU": "14b5a3d9a2fd2a13afd85c623d2f207703413e1fa4bef70631cf49e7b02c334af2082e6f",
            "_gid": "GA1.3.4286743.1642214773",
            "_gat_UA-81625846-2": "1"
        }

        body = 'username=magrou&password=F***Y**&lt=&execution=e1b293ab-d383-476d-aa73-a985a30fb9a0_ZXlKaGJHY2lPaUpJVXpVeE1pSXNJblI1Y0NJNklrcFhWQ0o5Lmh5b080VHZ4RnpuSEU2YVA5U0VXOHhqMEJQMzR4c1phTElBUURkU1lMck56SEJVRUdTTTNrd2tuOTd3eVRmdi85S3UyU0I3dG4vbjZCSHQ4MUU2ckFReFpRZzBWaDVDUjcycURnY21rUnlnaFhiSFZPREtLTWRXekxwRmZoYmhlcU5BeTBOM29pdFlWQ2FSTExkeURZdmU1dTV2ZSt0SXJMdC9EdU1JT3hsaXNHZzRsUnpXSGZ4Q0EvSnhtRHIrR0RFUXp3ODVDWlpQU291ODZxZzJWOGcrRW5rRXVTc0twN3ZXcDI0eUUwbDVNM0Q1c2VtaDBtTEExdWpDajVFS1BkdkV3U0tGbmR5VzZJQVhxY1E2N0lNejNNVlRSczJpWjI2UGI4VzdIY2RJZmtseVNoQm9TUlErVWcxTnRRWWJjV1huVnZpTjlwU3dMOThxdmZQdUY4VXl4U3ZFV1NHK0pyYm1DRmtHOG55b0dwdzNxNVVsbndtTVU2akdLdHhYQ2hIZDV5cnV1Z2JBSExoOGRvbVE1dkdsL2hSa0VKcmxxNEZzZjFWVnorUmRaanR2SmJuaDFhMmRJTVd3RkdjSFJDWDVsOTl1VVM4eENCOEttdC90QldicW5Mc01SYm8va0U1NEIrNU91UUdkV04zOG85NHkvOWtVT3VHcEZPMjJTRC9NWmtCdUE1RVZmT3VFZlc5ZmgyS29XK09iaFdiV0Uyb2dKd2EzdURxUWU4T0x3YWZ6RVNTWlRhdHhnbVBSVEE3SXBqUEErVkRwOEJyaGR3cDBjb0FRUWxuQ2FlWitFUjRVWG1NZjcvSUNoK3VkdXJVbGpiREs2NHBHd1ZsQ2Nzakxta2RCUnJyVW9ZS2YrWEY3c0YzSFJ4d0taN3RrYXV1KzNZdkk3RFpFa015eUozWXU3Q0F1WUF5Y2tFb0ZtRUdLMXdOdEJLOHN5cUZLZXZwQ2V0dnBxa3IyMGlpNk5DT3E5aU9SVmpmbFNvaXRqcjd4L0xraWx6NHRTcjNqUlh2QmFDQWI3d2l1aitOdWFzZitmWFNKcE4yUUk5d0ZpcWgzZFJmV0V6R1YyaGVEMTh5blFDb2JTUm1pTzAxcVlpbnU2b3BLTk1DeUdKeGkva3ZCUUdCWG9qOTMwdVJYbUdGbEF3SHhpMjd5K3lQYzk5K010dmZKdFY0ejk3MjgzWC9KdUhzUnhESnZscEJWdHpSWTc3N092U1FZTWtNT1VkUVk5VWg4aW1aKzUvTklBRzhyOVVXSkgwN1JGaU1PeDIwcTNDNnRvSDQvclFIanBaZmpNS1NpdzVpbTFIZWpHRVpkN0FtbGpPQlJtVXRzNmJhV2x4S1orU3RNT094bk9obmNFdngyR0FzYlQ4UWZvSFZuelpSdmhqVThRYWlMZFk5QVJCTWJhVExYRURuaEtwdHpTUjBTU0dWZEovck93L2hFRWlDWDdjZmduYytkaEswWlNCV1MxcGczY0xXYmdPZ3VjY0dpMFdndnMxVzVHNTJyUFBMSlpQSnJTb2lhM2MzWWFWZVpRVVZQa0ovMnliL3lkNWcyckVIN28yc0k5VnVGczNmTVhvRmljWkJ6ZVV5N0ZqVGx6anpsK284WEZ1UmhFYVNLY3ZsVDV3dTlvNHVqVjRsa2lFMzh0WVBmNUxBVjdxZWNjMmYwPS43UTRhWjVaSjdrSVFpZ0NNQ2NnbFpfbXg0M1VhOFluUm1DUTdXd1FzZk1HUjVpUHNlSmNSVzJrLWhUV2RwdkhkNDFZdVRzc294dzlKRVJyVGtyTHF5UQ%3D%3D&_eventId=submit&geolocation=&g-recaptcha-token='

        yield FormRequest.from_response(response,
            # url=url,
            formdata={'username': 'magrou', 'password': 'F***Y**'},
            method='POST',
            dont_filter=True,
            cookies=cookies,
            headers=headers,
            body=body,
            meta={'dont_redirect': True, "handle_httpstatus_list": [302, 401]},
                                        callback=self.parse_result
        )

        # yield SeleniumRequest(url=self.start_urls[0],
        #                       screenshot=True,
        #                       callback=self.parse_result,
        #                       )

    def parse_result(self, response):
        def get_web_element_from_dict(driver: webdriver, element_to_check_for_dict):
            if type(element_to_check_for_dict) is dict:
                first_element_value = list(element_to_check_for_dict.values())[0]
                element_to_check_for_dict = driver.create_web_element(element_id=first_element_value)
            return element_to_check_for_dict

        # webdriver.
        self.driver = webdriver.Chrome()
        self.driver.get('https://portal.generali.pl/auth/login')
        print(self.driver)

        login = self.driver.find_element(By.ID, "username")
        get_web_element_from_dict(self.driver, login).send_keys('magrou')

        password = self.driver.find_element(By.ID, "password")
        get_web_element_from_dict(self.driver, password).send_keys('Gru*24_L#d^kN')

        button = self.driver.find_element(By.XPATH, "//*[@type='submit']")
        get_web_element_from_dict(self.driver, button).click()

        click_dom = self.driver.find_element_by_xpath('//*[text()="Dom/Mieszkanie"]')
        get_web_element_from_dict(self.driver, click_dom).click()

        click_dom = WebDriverWait(self.driver, 9).until(EC.presence_of_element_located((By.XPATH, '//*[@id="chat"]/i')))
        get_web_element_from_dict(self.driver, click_dom).click()


        sel = Selector(text=self.driver.page_source)
        content = sel.xpath('/html').extract_first()

        print(content)


        # yield content


        # open_in_browser(response)
        time.sleep(500)


process = CrawlerProcess(settings={
    "FEEDS": {
        "items.json": {"format": "json"},
    },
})

process.crawl(Calculator)
print(process.start())




