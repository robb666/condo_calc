from selenium import webdriver
import pandas as pd


class Condocalc(webdriver.Chrome):
    login = {}
    df = pd.read_excel('/run/user/1000/gvfs/smb-share:server=192.168.1.12,share=e/Agent baza/Login_Hasło.xlsx')

    login['generali_url'] = 'https://' + df.iloc[8, 3]
    login['generali_login'] = df.iloc[8, 5]
    login['generali_password'] = df.iloc[8, 6]
    login['uniqa_url'] = 'https://' + df.iloc[40, 3]
    login['uniqa_login'] = df.iloc[41, 5]
    login['uniqa_password'] = df.iloc[40, 6]
    login['warta_url'] = 'https://' + df.iloc[42, 3]
    login['warta_login'] = df.iloc[42, 5]
    login['warta_password'] = df.iloc[42, 6]
    print(login)

    def __init__(self, driver_path=webdriver.Chrome, teardown=False):
        self.driver_path = driver_path
        self.teardown = teardown
        super(Condocalc, self).__init__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def land_first_page(self):
        self.get(self.login['uniqa_url'])

