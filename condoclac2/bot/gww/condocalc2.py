from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.relative_locator import locate_with
import pandas as pd
import time
import re


class Condocalc(webdriver.Chrome):

    def __init__(self, driver_path=webdriver.Chrome, teardown=False):
        self.driver_path = driver_path
        self.teardown = teardown
        options = webdriver.ChromeOptions()
        options.add_experimental_option("useAutomationExtension", False)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        # options.add_experimental_option('excludeSwitches', ['enable-logging'])  # win devtools supress
        # options.headless = True
        super(Condocalc, self).__init__(options=options)
        self.implicitly_wait(10)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def login_page(self, url):
        self.get(url)

    def login(self, login, passw):
        self.find_element(By.XPATH, "//input[@id='username' or @id='login']").send_keys(login)
        self.find_element(By.XPATH, "//input[@id='password']").send_keys(passw)
        self.find_element(By.XPATH, "//*[@type='submit' or @type='button']").click()

    def calc_gen(self):
        self.find_element(By.XPATH, "//label[contains(text(), 'Dom')]").click()

    def calc_war(self):
        self.find_element(By.XPATH, "//span[text()='Majątek']").click()
        self.find_element(By.XPATH, "//a[contains(text(), 'Sprzedaż')]").click()
        self.find_element(By.XPATH, "//span[text()='Mieszkaniowe']").click()

    def calc_wie(self, url):
        time.sleep(.2)
        self.get(url)

    def apk_gen(self):
        self.find_element(By.XPATH, "//*[@class='col-sm-3']//span[text()='TAK']").click()
        self.find_element(By.XPATH, "//*[@class='col-sm-3']/following::span[text()='NIE']").click()
        self.find_element(By.XPATH, "//*[@id='apkSection']/div[2]/div/div[1]/div[5]/div[2]/div/label[2]/span").click()
        self.find_element(By.XPATH,
                          "//span[@class='fe-loading-btn-next fe-readonlymode-active fe-no-policy-disable-send']"
                          ).click()

    def apk_war(self):
        self.find_element(By.ID, 'customer-needs-analysis-agentsOwnSystem-TAK').click()

    def _clear_box(self, box):
        if box == self.find_element(By.XPATH, f"//input[@id='city-propertyForm']"):
            self.find_element(By.XPATH, f"//div[@id='propertyPanel']").click()
        box.send_keys(Keys.CONTROL + 'a')
        box.send_keys(Keys.DELETE)

    def input_gen(self, data):
        data['domu'], data['lokalu'] = data.pop('Nr. ulicy'), data.pop('Nr. mieszkania')
        form = self.find_element(By.ID, 'houseCalculationDataForm').text
        for key in data:
            if item := re.search(key, form, re.I):
                re_key = item.group()
                box = self.find_element(By.XPATH, f"//label[contains(text(), '{re_key}')]/following::input")
                self._clear_box(box)
                box.send_keys(data[key])
        house = self.find_element(By.XPATH, "//input[@id='houseNumber-propertyForm']")
        self._clear_box(house)
        house.send_keys(data['lokalu'])
        flat = self.find_element(By.XPATH, "//input[@id='flatNumber-propertyForm']")
        self._clear_box(flat)
        flat.send_keys(data['domu'])

        if data['Rodzaj'].title() == 'Dom':
            self.find_element(By.XPATH, "//div[contains(text(), 'Dom')]").click()
        if data['Konstrukcja'].title() == 'Drewniana':
            self.find_element(By.XPATH, "//div[contains(text(), 'Drewniana')]").click()
        if data['Zabezpieczenia'][0] != '':
            self.find_element(By.XPATH, "//input[@class='select2-search__field']").click()
            self.find_element(By.XPATH, "//input[@class='select2-search__field']").click()
            for security in data['Zabezpieczenia']:
                self.find_element(By.XPATH, f"//span[text()='{security.capitalize()}']").click()

        data['Liczba szkód'] = 3 if int(data['Liczba szkód']) > 3 else int(data['Liczba szkód'])
        self.find_element(By.CSS_SELECTOR,
                          f"#last5YearsClaims > label:nth-child({int(data['Liczba szkód']) + 1})").click()

        for i in range(2, 7, 2):
            self.find_element(By.CSS_SELECTOR,
                              f'#agreementPanel > div:nth-child({i}) > div > div > label:nth-child(2)').click()

        self.find_element(By.XPATH, "//span[text()='Dalej']").click()

    def input_war(self, data):
        form = self.find_elements(By.XPATH, "//div[@class='col-md-12']")
        print(form)
        for text in form:
            print(text.text)
        for key in data:
            if item := re.search(key, form, re.I):
                re_key = item.group()
                box = self.find_element(By.XPATH, f"//span[contains(text(), '{re_key}')]/following::input")
                box.send_keys(data[key])

    def input_wie(self, data):
        time.sleep(.5)
        # period = self.find_element(By.XPATH, "//input[@ref='input']")
        period = WebDriverWait(self, 3).until(EC.presence_of_element_located((By.XPATH, "//input[@ref='input']")))

        period.click()
        period.send_keys(Keys.ENTER)
        self.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.find_element(By.XPATH, "//span[text()='Mieszkanie']").click()
        form = self.find_element(By.XPATH,
                                 "//div[@class='col-12 col-sm-12 col-md-12 col-lg-8 col-xl-9 intro_calculator_calculator']"
                                 ).text
        print(form)
        for key in data:
            if item := re.search(key, form, re.I):
                re_key = item.group()
                box = self.find_element(By.XPATH, f"//label[contains(text(), '{re_key}')]/following::input")
                box.send_keys(data[key])


    def wait(self):
        time.sleep(9999)

