import pandas as pd


PATH = 'M:\Agent baza\Login_Hasło.xlsx'


login = {}
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


WIE_CALC = 'https://wienet.pl/#/household?calculatorRoute=household'

DATA_PATH = r'C:\Users\PipBoy3000\Desktop\formularz mieszkaniowy.txt'
