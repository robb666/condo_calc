import pandas as pd


PATH = '/run/user/1000/gvfs/smb-share:server=192.168.1.12,share=e/Agent baza/Login_Hasło.xlsx'

login = {}
df = pd.read_excel(PATH)
login['generali_url'] = 'https://' + df.iloc[8, 3]
login['generali_login'] = df.iloc[8, 5]
login['generali_password'] = df.iloc[8, 6]
login['uniqa_url'] = 'https://' + df.iloc[38, 3]
login['uniqa_login'] = df.iloc[41, 5]
login['uniqa_password'] = df.iloc[40, 6]
login['warta_url'] = 'https://' + df.iloc[42, 3]
login['warta_login'] = df.iloc[42, 5]
login['warta_password'] = df.iloc[42, 6]
# print(login)