from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time


class Condocalc(webdriver.Chrome):

    def __init__(self, driver_path=webdriver.Chrome, teardown=False):
        self.driver_path = driver_path
        self.teardown = teardown
        options = webdriver.ChromeOptions()
        options.add_experimental_option("useAutomationExtension", False)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        # options.add_experimental_option('excludeSwitches', ['enable-logging'])  # win devtools supress
        # options.add_argument('--headless')
        super(Condocalc, self).__init__(options=options)
        self.implicitly_wait(10)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def land_first_page(self, url):
        self.get(url)

    def login(self, login, passw):
        self.find_element(By.XPATH, "//input[@id='username' or @id='login']").send_keys(login)
        self.find_element(By.XPATH, "//input[@id='password']").send_keys(passw)
        self.find_element(By.XPATH, "//*[@type='submit' or @type='button']").click()

    def calc(self):
        self.find_element(By.XPATH, "//label[contains(text(), 'Dom')]").click()

    def apk(self):
        self.find_element(By.XPATH, "//*[@class='col-sm-3']//span[text()='TAK']").click()
        apk_text = self.find_element(By.XPATH, "//span[text()='2.']/following::span[1]")
        print('\n' + apk_text.text)

        decision = input('\nNaciśnij "t" jeżeli TAK, "n" jeżeli NIE i enter: ')
        if decision == 't':
            self.find_element(By.XPATH, "//*[@class='col-sm-3']/following::span[text()='TAK']").click()
        elif decision == 'n':
            self.find_element(By.XPATH, "//*[@class='col-sm-3']/following::span[text()='NIE']").click()
        else:
            self.apk()


        # for question in apk_text:
        #     print(question.text)
        #     if question.text.startswith('2'):
        #         print(question.text)
        time.sleep(9999)
        return apk_text
        # self.find_element(By.XPATH, "//span[@class='fe-radio-btn-label']").click()

