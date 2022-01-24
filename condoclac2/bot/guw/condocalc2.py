from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import guw.constants as const


class Condocalc(webdriver.Chrome):

    def __init__(self, driver_path=webdriver.Chrome, teardown=False):
        self.driver_path = driver_path
        self.teardown = teardown
        super(Condocalc, self).__init__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def land_first_page(self):
        self.get(const.login['generali_url'])

    def login(self):
        self.find_element(By.XPATH, "//input[@id='username']").send_keys(const.login['generali_login'])
        self.find_element(By.XPATH, "//input[@id='password']").send_keys(const.login['generali_password'])

