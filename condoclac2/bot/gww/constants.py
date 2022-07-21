import pandas as pd
import os

WIE_CALC = 'https://wienet.pl/#/household?calculatorRoute=household'

DATA_PATH = os.getcwd() + r'\formularz mieszkaniowy.txt'

JAREK_PATH = r'C:\LiH\HASŁA A.xlsx'

PATH = r'M:\Agent baza\Login_Hasło.xlsm'


login = {}
if os.path.exists(JAREK_PATH):
    PATH = JAREK_PATH

    df = pd.read_excel(PATH)

    login['generali_url'] = 'https://portal.generali.pl'
    login['generali_login'] = df.iloc[0, 1]
    login['generali_password'] = df.iloc[0, 2]

    login['warta_url'] = 'https://eagent.warta.pl'
    login['warta_login'] = df.iloc[1, 1]
    login['warta_password'] = df.iloc[1, 2]

    login['wiener_url'] = 'https://wienet.pl/#/login'
    login['wiener_login'] = df.iloc[2, 1]
    login['wiener_password'] = df.iloc[2, 2]


else:
    df = pd.read_excel(PATH)

    login['generali_url'] = 'https://' + df.iloc[8, 3]
    login['generali_login'] = df.iloc[8, 5]
    login['generali_password'] = df.iloc[8, 6]

    login['warta_url'] = 'https://' + df.iloc[42, 3]
    login['warta_login'] = df.iloc[42, 5]
    login['warta_password'] = df.iloc[42, 6]

    login['wiener_url'] = 'https://' + df.iloc[52, 3]
    login['wiener_login'] = df.iloc[52, 5]
    login['wiener_password'] = df.iloc[52, 6]

