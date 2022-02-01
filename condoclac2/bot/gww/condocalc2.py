from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.support.relative_locator import locate_with
import pandas as pd
import time
import re


class Condocalc(webdriver.Chrome):

    def __init__(self, driver_path=webdriver.Chrome, teardown=False):
        self.driver_path = driver_path
        self.teardown = teardown
        self.data_war = None
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
        time.sleep(.1)
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
        if box == self.find_element(By.XPATH, f"//input[@id='city-propertyForm']|"  # gen
                                              f"//h3[text()='Miejsce ubezpieczenia']"):  # wie
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
        house.send_keys(data['domu'])
        flat = self.find_element(By.XPATH, "//input[@id='flatNumber-propertyForm']")
        self._clear_box(flat)
        flat.send_keys(data['lokalu'])

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

    @staticmethod
    def _click_into_body(body_el):
        body_el.click()
        time.sleep(.26)

    def input_translate_war(self, data):
        data['Nr domu'], data['Nr lokalu'] = data.pop('Nr. ulicy'), data.pop('Nr. mieszkania')
        self.data_war = data

    def input_personal_war(self):
        body_el = self.find_element(By.XPATH, '//*[@id="houseInsured"]/div[2]/house-single-insured/div[1]/span[1]')
        self._click_into_body(body_el)
        self.find_element(By.XPATH, '//*[@id="insured-identity-0"]').send_keys(self.data_war['Pesel'])
        self._click_into_body(body_el)
        time.sleep(.2)
        self.find_element(By.XPATH, '//*[@id="insured-name-0"]').send_keys(self.data_war['Nazwisko'])
        self._click_into_body(body_el)
        self.find_element(By.XPATH, '//*[@id="insured-first-name-0"]').send_keys(self.data_war['Imię'])
        self._click_into_body(body_el)

    def input_prop_type(self):
        self.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        if self.data_war['Rodzaj'].title() == 'Dom':
            self.find_elements(By.XPATH, "//div[contains(text(), 'Dom Jednorodzinny')]")[0].click()
        if self.data_war['Rodzaj'].title() == 'Mieszkanie':
            self.find_element(By.XPATH, "//div[contains(text(), 'Lokal Mieszkalny')]").click()

    def input_address_war(self):
        body_el = self.find_element(By.XPATH, "//*[@id='estate-address']/div/div/div[1]")
        self.find_element(By.CSS_SELECTOR, '#estate-pri-zip-code').send_keys(self.data_war['Kod'])
        self._click_into_body(body_el)
        self.find_element(By.XPATH, "//*[@id='estate-address']/div/div/div[1]").click()
        self._click_into_body(body_el)
        self.find_element(By.XPATH, "//*[@id='estate-pri-street-no']").send_keys(self.data_war['Nr domu'])
        self._click_into_body(body_el)
        self.find_element(By.XPATH, "//*[@id='estate-pri-flat-no']").send_keys(self.data_war['Nr lokalu'])
        self._click_into_body(body_el)

    def _prop_year_war(self, decades):
        action_box = ActionChains(self)
        for _ in range(decades):
            action_box.send_keys(Keys.ARROW_DOWN)
        time.sleep(.26)
        action_box.send_keys(Keys.ENTER)
        action_box.perform()

    def input_construction_year_war(self):
        self.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.find_element(By.XPATH, '//*[@id="estate-details-construction-year-period-select-search"]').click()
        time.sleep(.3)
        if int(self.data_war['Rok']) > 2010:
            self._prop_year_war(1)
        elif int(self.data_war['Rok']) > 2000:
            self._prop_year_war(2)
        elif int(self.data_war['Rok']) > 1990:
            self._prop_year_war(3)
        elif int(self.data_war['Rok']) > 1980:
            self._prop_year_war(4)
        elif int(self.data_war['Rok']) > 1970:
            self._prop_year_war(5)
        elif int(self.data_war['Rok']) > 1960:
            self._prop_year_war(6)
        elif int(self.data_war['Rok']) > 1950:
            self._prop_year_war(7)
        elif int(self.data_war['Rok']) > 1940:
            self._prop_year_war(8)
        elif int(self.data_war['Rok']) > 1930:
            self._prop_year_war(9)
        elif int(self.data_war['Rok']) > 1920:
            self._prop_year_war(10)
        elif int(self.data_war['Rok']) < 1920:
            self._prop_year_war(11)

    def input_floor_war(self):
        action_box = ActionChains(self)

        self.find_element(By.XPATH, '//*[@id="house-floors-select-search"]').click()
        time.sleep(.2)
        if self.data_war['Kondygnacja'].title() == 'Parter':
            action_box.send_keys(Keys.ARROW_DOWN)
            action_box.send_keys(Keys.ENTER)
            action_box.perform()
        if self.data_war['Kondygnacja'].title() == 'Środkowa':
            action_box.send_keys(Keys.ARROW_UP)
            action_box.send_keys(Keys.ARROW_DOWN)
            action_box.send_keys(Keys.ENTER)
            action_box.perform()
        if self.data_war['Kondygnacja'].title() == 'Ostatnia':
            action_box.send_keys(Keys.ARROW_UP)
            action_box.send_keys(Keys.ENTER)
            action_box.perform()

    def input_area_war(self):
        body_el = self.find_element(By.XPATH, '//*[@id="housePrimaryEstate"]/div[2]/div[4]')
        self._click_into_body(body_el)
        self.find_element(By.XPATH, "//*[@id='estate-pri-area']").send_keys(self.data_war['Powierzchnia'])
        self._click_into_body(body_el)

    def input_finish_war(self):
        action_box = ActionChains(self)

        self.find_element(By.XPATH, '//*[@id="finish-standards-select-search"]').click()
        time.sleep(.2)
        action_box.send_keys(Keys.ARROW_UP)
        time.sleep(.2)
        action_box.send_keys(Keys.ENTER)
        action_box.perform()

    def input_construction_type_war(self):
        body_el = self.find_element(By.XPATH, '//*[contains(text(), "Charakterystyka lokalu mieszkalnego")]')
        self._click_into_body(body_el)
        if self.data_war['Konstrukcja'].title() == 'Drewniana':
            WebDriverWait(self, 9).until(
                EC.element_to_be_clickable((
                    By.XPATH, '//span[@dynatrace-name="house-estate-details-flammability-replacement"]'))).click()


    def input_declarations_war(self):
        self.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        body_el = self.find_element(By.XPATH, '//*[text()="Konfiguracja dodatkowa"]')
        self._click_into_body(body_el)
        self.find_element(
            By.XPATH, f"//span[contains(text(), 'Liczba szkód')]/following::input").send_keys(self.data_war['Liczba szkód'])

        self._click_into_body(body_el)
        self.find_element(
            By.XPATH, f"//span[contains(text(), 'Liczba powodzi')]/following::input").send_keys('0')

        self._click_into_body(body_el)
        self.find_element(
            By.XPATH, f"//span[contains(text(), 'Liczba lat bezszkodowej kontynuacji ')]/following::input").send_keys('0')
        self._click_into_body(body_el)

    def input_next_war(self):
        try:
            self.find_element(By.XPATH, '//div[@class="ui-notification__inner__close"]').click()
        except Exception as e:
            print(e)
        self.find_element(By.XPATH, '//button[@id="footer-button-show-next"]').click()






    def input_wie(self, data):
        """Pierwsze linijki redefiniują słownik."""
        # TODO dorobić kontygnację
        data['Numer budynku'], data['Numer mieszkania'] = data.pop('Nr. ulicy'), data.pop('Nr. mieszkania')
        time.sleep(.4)
        period = self.find_element(By.XPATH, "//input[@ref='input']")
        # period = WebDriverWait(self, 3).until(EC.presence_of_element_located((By.XPATH, "//input[@ref='input']"))) ???
        period.click()
        period.send_keys(Keys.ENTER)
        self.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.find_element(By.XPATH, "//span[text()='Mieszkanie']").click()
        form = self.find_element(By.XPATH,
                                 "//div[@class='col-12 col-sm-12 col-md-12 col-lg-8 col-xl-9 intro_calculator_calculator']"
                                 ).text
        # print(form)
        for key in data:
            if item := re.search(key, form, re.I):
                re_key = item.group()
                box = self.find_element(By.XPATH, f"//label[contains(text(), '{re_key}')]/following::input")
                self._clear_box(box)
                box.send_keys(data[key])

        self.find_elements(By.XPATH, "//property-data/*//radio-btn-in[2]/label")[0].click()

        if data['Kondygnacja'].title() == 'Parter':
            self.find_elements(By.XPATH, "//property-data/*//radio-btn-in[1]/label")[1].click()
        if data['Kondygnacja'].title() == 'Środkowa':
            self.find_elements(By.XPATH, "//property-data/*//radio-btn-in[2]/label")[1].click()
        if data['Kondygnacja'].title() == 'Ostatnie':
            self.find_element(By.XPATH, "//property-data/*//radio-btn-in[3]/label").click()

        self.find_element(By.XPATH, "//*[@id='uniqueId_4']").send_keys('30')
        self.find_element(By.XPATH, "//button[text()='Następny krok']").click()




    def wait(self):
        print('time.sleep(9999)')
        time.sleep(9999)

