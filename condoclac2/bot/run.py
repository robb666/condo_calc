from guw.condocalc2 import Condocalc
import guw.constants as const
import concurrent.futures


def gen():
    with Condocalc() as bot:
        bot.login_page(const.login['generali_url'])
        bot.login(const.login['generali_login'],
                  const.login['generali_password'])
        bot.calc()
        bot.apk_gen()

def war():
    with Condocalc() as bot:
        bot.login_page(const.login['warta_url'])
        bot.login(const.login['warta_login'],
                  const.login['warta_password'])


def wie():
    with Condocalc() as bot:
        bot.login_page(const.login['wiener_url'])
        bot.login(const.login['wiener_login'],
                  const.login['wiener_password'])


calcs = [gen, war, wie]
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    for calc in calcs:
        executor.submit(calc)




# gen()
