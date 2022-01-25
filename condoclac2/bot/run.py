from guw.condocalc2 import Condocalc
import guw.constants as const
import concurrent.futures
import time


def gen():
    with Condocalc() as bot:
        bot.land_first_page(const.login['generali_url'])
        bot.login(const.login['generali_login'],
                  const.login['generali_password'])


def war():
    with Condocalc() as bot:
        bot.land_first_page(const.login['warta_url'])
        bot.login(const.login['warta_login'],
                  const.login['warta_password'])


def wie():
    with Condocalc() as bot:
        bot.land_first_page(const.login['wiener_url'])
        bot.login(const.login['wiener_login'],
                  const.login['wiener_password'])


calcs = [gen, war, wie]
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    for calc in calcs:
        executor.submit(calc)





