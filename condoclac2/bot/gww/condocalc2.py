import logging
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
# from selenium.webdriver.support.relative_locator import locate_with
import pandas as pd
import time
import re
import inspect
from datetime import datetime
from dateutil.relativedelta import relativedelta


class Condocalc(webdriver.Chrome):

    # def __init__(self, driver_path=webdriver.Chrome, teardown=False):
    def __init__(self, driver_path=os.getcwd() + '\chromedriver.exe', teardown=False):

        self.driver_path = driver_path
        self.teardown = teardown
        self.data_gen = None
        self.data_war = None
        self.data_wie = None
        self.body_el = None
        options = webdriver.ChromeOptions()
        options.add_argument("--window-size=1280,1080")
        options.add_experimental_option("excludeSwitches", ['enable-logging'])  # win devtools supress (order!)
        options.add_experimental_option("useAutomationExtension", False)
        options.add_experimental_option("excludeSwitches", ['enable-automation'])
        options.add_experimental_option('prefs', {"credentials_enable_service": False,
                                        'profile': {"profile.password_manager_enabled": False}})
        options.add_experimental_option("detach", True)
        # options.headless = True
        super(Condocalc, self).__init__(options=options)
        self.implicitly_wait(6)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def login_page(self, url):
        self.get(url)

    def login(self, login, passw):
        WebDriverWait(self, 9).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@id='username' or @id='login']"))).send_keys(login)
        time.sleep(.1)
        self.find_element(By.XPATH, "//input[@id='password']").send_keys(passw)
        self.find_element(By.XPATH, "//*[@type='submit' or @type='button']").click()

    def calc_gen(self):
        self.find_element(By.XPATH, "//label[contains(text(), 'Dom')]").click()

    def calc_war(self):
        self.find_element(By.XPATH, "//*[@class='modal-header__close ng-scope']").click()

        self.find_element(By.XPATH, "//span[text()='Majątek']").click()
        self.find_element(By.XPATH, "//a[contains(text(), 'Sprzedaż')]").click()
        self.find_element(By.XPATH, "//span[text()='Mieszkaniowe']").click()

    def calc_wie(self, url):
        time.sleep(.35)
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
        current = Condocalc.input_address_war.__name__
        call_stack = inspect.stack()
        returned_name = call_stack[1][3]

        if returned_name != current and box == self.find_element(By.XPATH,
                                                                    f"//input[@id='city-propertyForm' or "       # gen
                                                                           f"text()='Miejsce ubezpieczenia']"):  # wie
            self.find_element(By.XPATH, f"//div[@id='propertyPanel']").click()
        box.send_keys(Keys.CONTROL + 'a')
        box.send_keys(Keys.DELETE)

    def input_translate_gen(self, data):
        data['nr domu'], data['lokalu'] = data.pop('Nr. ulicy'), data.pop('Nr. mieszkania')
        self.data_gen = data

    def input_follow_gen(self):
        form = self.find_element(By.ID, 'houseCalculationDataForm').text
        for key in self.data_gen:
            if item := re.search(key, form, re.I):
                re_key = item.group()
                box = self.find_element(By.XPATH, f"//label[contains(text(), '{re_key}')]/following::input")
                self._clear_box(box)
                box.send_keys(self.data_gen[key])
                if key == 'Kod': time.sleep(.1)

        house = self.find_element(By.XPATH, "//input[@id='houseNumber-propertyForm']")
        self._clear_box(house)
        house.send_keys(self.data_gen['nr domu'])
        flat = self.find_element(By.XPATH, "//input[@id='flatNumber-propertyForm']")
        self._clear_box(flat)
        flat.send_keys(self.data_gen['lokalu'])

    def input_prop_type_gen(self):
        if self.data_gen['Rodzaj'].lower() == 'dom':
            self.find_element(By.XPATH, "//div[contains(text(), 'Dom')]").click()

    def level_gen(self):
        if self.data_gen['Kondygnacja'].lower() == 'parter':
            self.find_elements(By.XPATH, "//label[@class='btn fe-radio-btn']")[0].click()
        if self.data_gen['Kondygnacja'].lower() in ('ostatnie', 'ostatnia'):
            self.find_elements(By.XPATH, "//label[@class='btn fe-radio-btn']")[1].click()

    def input_construction_type_gen(self):
        if self.data_gen['Konstrukcja'].lower() == 'drewniana':
            self.find_element(By.XPATH, "//div[contains(text(), 'Drewniana')]").click()

    def input_security_gen(self):
        if self.data_gen['Zabezpieczenia'][0] not in ('', 'brak'):
            self.find_element(By.XPATH, "//input[@class='select2-search__field']").click()
            self.find_element(By.XPATH, "//input[@class='select2-search__field']").click()
            for security in self.data_gen['Zabezpieczenia']:
                self.find_element(By.XPATH, f"//option[text()='{security.capitalize()}']").click()
            self.body_el = self.find_element(By.XPATH, "//*[contains(text(), 'Zabezpieczenia')]")
            self._click_into_body(self.body_el)

    def input_declarations_gen(self):
        self.data_gen['Liczba szkód'] = 3 if int(self.data_gen['Liczba szkód']) > 3 else int(self.data_gen['Liczba szkód'])
        self.find_element(By.CSS_SELECTOR,
                          f"#last5YearsClaims > label:nth-child({int(self.data_gen['Liczba szkód']) + 1})").click()
        for i in range(2, 7, 2):
            self.find_element(By.CSS_SELECTOR,
                              f'#agreementPanel > div:nth-child({i}) > div > div > label:nth-child(2)').click()

    def input_next_gen(self):
        self.find_element(By.XPATH, "//span[text()='Dalej']").click()

    @staticmethod
    def _click_into_body(body_el):
        body_el.click()
        # time.sleep(.8)
        time.sleep(.4)

    def input_translate_war(self, data):
        data['Nr domu'], data['Nr lokalu'] = data.pop('Nr. ulicy'), data.pop('Nr. mieszkania')
        self.data_war = data

    def input_personal_war(self):
        self.body_el = self.find_element(By.XPATH, '//*[@id="houseInsured"]/div[2]/house-single-insured/div[1]/span[1]')
        self._click_into_body(self.body_el)
        self.find_element(By.XPATH, '//*[@id="insured-identity-0"]').send_keys(self.data_war['Pesel'])
        self._click_into_body(self.body_el)
        time.sleep(.7)
        self.find_element(By.XPATH, '//*[@id="insured-name-0"]').clear()
        time.sleep(.3)
        self.find_element(By.XPATH, '//*[@id="insured-name-0"]').send_keys(self.data_war['Nazwisko'])
        self._click_into_body(self.body_el)

        # WebDriverWait(self, 9).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#insured-first-name-0-search'))).clear()

        self.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # time.sleep(.35)

        customer_name = WebDriverWait(self, 9).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#insured-first-name-0-search')))

        customer_name.send_keys(self.data_war['Imię'])
        customer_name.send_keys(Keys.ARROW_DOWN)
        self._click_into_body(self.body_el)

    def input_prop_type_war(self):
        self.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        if self.data_war['Rodzaj'].title() == 'Dom':
            self.find_elements(By.XPATH, "//div[contains(text(), 'Dom Jednorodzinny')]")[0].click()
        if self.data_war['Rodzaj'].title() == 'Mieszkanie':
            self.find_element(By.XPATH, "//div[contains(text(), 'Lokal Mieszkalny')]").click()

    def input_address_war(self):
        self.body_el = self.find_element(By.XPATH, '//*[contains(text(), "Adres miejsca ubezpieczenia")]')
        zip = self.find_element(By.CSS_SELECTOR, '#estate-pri-zip-code')
        zip.clear()
        time.sleep(.2)
        zip.send_keys(self.data_war['Kod'])
        self._click_into_body(self.body_el)
        self._clear_box(self.find_element(By.CSS_SELECTOR, '#estate-pri-city-search'))
        self.find_element(By.CSS_SELECTOR, '#estate-pri-city-search').send_keys(self.data_war['Miejscowość'])
        self._click_into_body(self.body_el)
        self._clear_box(self.find_element(By.CSS_SELECTOR, '#estate-pri-street-search'))
        self.find_element(By.CSS_SELECTOR, '#estate-pri-street-search').send_keys(self.data_war['Ulica'])
        self._click_into_body(self.body_el)
        self.find_element(By.XPATH, "//*[@id='estate-address']/div/div/div[1]").click()
        self._click_into_body(self.body_el)
        self._clear_box(self.find_element(By.XPATH, "//*[@id='estate-pri-street-no']"))
        self.find_element(By.XPATH, "//*[@id='estate-pri-street-no']").send_keys(self.data_war['Nr domu'])
        self._click_into_body(self.body_el)
        if self.data_war['Nr lokalu']:
            self._clear_box(self.find_element(By.XPATH, "//*[@id='estate-pri-flat-no']"))
            self.find_element(By.XPATH, "//*[@id='estate-pri-flat-no']").send_keys(self.data_war['Nr lokalu'])
            self._click_into_body(self.body_el)

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

        if self.data_war['Kondygnacja']:
            self.find_element(By.XPATH, '//*[@id="house-floors-select-search"]').click()
        time.sleep(.4)
        if self.data_war['Kondygnacja'].title() == 'Parter':
            action_box.send_keys(Keys.ARROW_DOWN)
            action_box.send_keys(Keys.ENTER)
            action_box.perform()
        elif self.data_war['Kondygnacja'].title() in ('Pośrednia', 'Pośrednie', 'Środkowa', 'Środkowe'):
            action_box.send_keys(Keys.ARROW_UP)
            action_box.send_keys(Keys.ARROW_DOWN)
            action_box.send_keys(Keys.ENTER)
            action_box.perform()
        elif self.data_war['Kondygnacja'].title() in ('Ostatnia', 'Ostatnie'):
            action_box.send_keys(Keys.ARROW_UP)
            action_box.send_keys(Keys.ENTER)
            action_box.perform()


    def input_area_war(self):
        if re.search('Mieszkanie', self.data_war['Rodzaj'], re.I):
            self.body_el = self.find_element(By.XPATH, '//*[contains(text(), "Charakterystyka lokalu mieszkalnego")]')
        self._click_into_body(self.body_el)
        m2 = self.find_element(By.XPATH, "//*[@id='estate-pri-area']")
        time.sleep(.4)
        m2.send_keys(self.data_war['Powierzchnia'])
        self._click_into_body(self.body_el)

    def input_finish_war(self):
        action_box = ActionChains(self)
        if self.data_war['Rodzaj'] in ('Dom', 'dom'):
            self.find_element(By.XPATH, '//*[@id="estate-pri-const-end-year"]').send_keys(self.data_war['Rok'])
        # time.sleep(.2)
        # action_box.send_keys(Keys.ARROW_UP)
        # time.sleep(.2)
        # action_box.send_keys(Keys.ENTER)
        # action_box.perform()

    def input_construction_type_war(self):
        self._click_into_body(self.body_el)
        if self.data_war['Konstrukcja'].title() == 'Drewniana':
            WebDriverWait(self, 9).until(
                EC.element_to_be_clickable((
                    By.XPATH, '//span[@dynatrace-name="house-estate-details-flammability-replacement"]'))).click()

    def input_declarations_war(self):
        self.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.body_el = self.find_element(By.XPATH, '//*[text()="Konfiguracja dodatkowa"]')
        self._click_into_body(self.body_el)
        self.find_element(
            By.XPATH, f"//span[contains(text(), 'Liczba szkód')]/following::input"
        ).send_keys(self.data_war['Liczba szkód'])

        self._click_into_body(self.body_el)
        self.find_element(
            By.XPATH, f"//span[contains(text(), 'Liczba powodzi')]/following::input").send_keys('0')
        self._click_into_body(self.body_el)

    def input_popup_war(self):
        try:
            self.implicitly_wait(1)
            self.find_element(
                By.XPATH, f"//span[contains(text(), 'Liczba lat bezszkodowej kontynuacji')]/following::input"
            ).send_keys('0')
            self._click_into_body(self.body_el)
        except NoSuchElementException as e:
            print(e)
            self.implicitly_wait(10)

    def input_next_war(self):
        try:
            self.implicitly_wait(1)
            self.find_element(By.XPATH, '//div[@class="ui-notification__inner__close"]').click()
        except NoSuchElementException as e:
            self.implicitly_wait(10)
        time.sleep(1.2)
        self.find_element(By.XPATH, '//button[@id="footer-button-show-next"]').click()

    def input_translate_wie(self, data):
        self.data_wie = data

    def input_period_wie(self):
        time.sleep(.9)
        try:
            popup = self.find_element(By.XPATH, "//label[contains(text(), 'Zamknij')]/following::input")
            popup.click()
            time.sleep(.9)
        except:
            pass

        period = WebDriverWait(self, 1).until(EC.element_to_be_clickable((By.XPATH, "//input[@ref='input']")))

        period.click()
        period.send_keys(Keys.ENTER)

    def input_follow_wie(self):
        if self.data_wie['Nr. mieszkania']:
            self.find_element(By.XPATH, "//span[text()='Mieszkanie']").click()
        else:
            self.find_element(By.XPATH, "//*[text()='Budynek mieszkalny']").click()

        form = self.find_element(By.XPATH, "//div[@class='col-12 col-sm-12 col-md-12 col-lg-8 col-xl-9 intro_calculator_calculator']")

        kod_poczt = self.find_element(By.XPATH, "//label[contains(text(), 'Kod')]/following::input")
        kod_poczt.send_keys(self.data_wie['Kod'])
        form.click()

        miejsc = self.find_element(By.XPATH, "//label[contains(text(), 'Miejscowość')]/following::input")
        time.sleep(.1)
        miejsc.send_keys(self.data_wie['Miejscowość'])

        ulica = self.find_element(By.XPATH, "//label[contains(text(), 'Ulica')]/following::input")
        for letter in self.data_wie['Ulica']:
            ulica.send_keys(Keys.END, letter)

        nr_ulicy = self.find_element(By.XPATH, "//label[contains(text(), 'budynku')]/following::input")
        nr_ulicy.send_keys(self.data_wie['Nr. ulicy'] )

        if self.data_wie.get('Nr. mieszkania'):
            nr_mieszkania = self.find_element(By.XPATH, "//label[contains(text(), 'mieszkania')]/following::input")
            nr_mieszkania.send_keys(self.data_wie['Nr. mieszkania'])

        rok_budowy = self.find_element(By.XPATH, "//label[contains(text(), 'Rok budowy')]/following::input")
        rok_budowy.send_keys(self.data_wie['Rok'])
        form.click()

        powierzchnia = self.find_element(By.XPATH, "//label[contains(text(), 'Powierzchnia użytkowa')]/following::input")
        powierzchnia.send_keys(self.data_wie['Powierzchnia'])

        if not self.data_wie['Nr. mieszkania']:
            self.find_elements(By.XPATH, "//property-data/*//radio-btn-in[2]/label")[1].click()
            self.find_elements(By.XPATH, "//property-data/*//radio-btn-in[1]/label")[2].click()
            self.find_elements(By.XPATH, "//property-data/*//radio-btn-in[2]/label")[3].click()
            self.find_elements(By.XPATH, "//property-data/*//radio-btn-in[1]/label")[4].click()

    def input_property_wie(self):
        self.find_elements(By.XPATH, "//property-data/*//radio-btn-in[2]/label")[0].click()  # Na stałe
        self.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        if self.data_wie.get('Kondygnacja').lower() == 'parter':
            self.find_elements(By.XPATH, "//property-data/*//radio-btn-in[1]/label")[1].click()
        if self.data_wie.get('Kondygnacja').lower() in ('pośrednie', 'pośrednia', 'środkowa', 'środkowe'):
            self.find_elements(By.XPATH, "//property-data/*//radio-btn-in[2]/label")[1].click()
        if self.data_wie.get('Kondygnacja').lower() in ('ostatnie', 'ostatnia'):
            self.find_element(By.XPATH, "//property-data/*//radio-btn-in[3]/label").click()

    def input_age_wie(self):
        time.sleep(.1)
        if pesel := self.data_wie.get('Pesel'):
            if pesel.startswith('0') and pesel[2] in ('2', '3'):
                year, month, day = pesel[:2], str(int(pesel[2:4]) - 20).zfill(2), pesel[4:]
                pesel = year + month + day

            birth_date = datetime.strptime(pesel[:6], '%y%m%d').date()
            today = datetime.today().date()

            if birth_date > today and not str(birth_date).startswith('0'):
                birth_date -= relativedelta(years=100)

            age = relativedelta(today, birth_date)

            self.find_element(By.XPATH,
                              "//label[contains(text(), 'Wiek ubezpieczon')]/following::input").send_keys(age.years)
        self.find_element(By.XPATH,
                          "//label[contains(text(), 'Wiek ubezpieczon')]/following::input").send_keys('40')

    def input_next_wie(self):
        self.find_element(By.XPATH, "//button[text()='Następny krok']").click()

    @staticmethod
    def wait():
        time.sleep(9999)
