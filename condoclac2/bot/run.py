import time
from gww.condocalc2 import Condocalc
import gww.constants as const
from gww.variables import customer_data
import concurrent.futures
from pprint import pprint


def gen(data):
    with Condocalc() as bot:
        bot.login_page(const.login['generali_url'])
        bot.login(const.login['generali_login'],
                  const.login['generali_password'])
        bot.calc_gen()
        bot.apk_gen()
        bot.input_translate_gen(data)
        bot.input_follow_gen()
        bot.input_prop_type_gen()
        bot.input_construction_type_gen()
        bot.input_security_gen()
        bot.input_declarations_gen()
        bot.input_next_gen()

        bot.wait()


def war(data):
    with Condocalc() as bot:
        bot.login_page(const.login['warta_url'])
        bot.login(const.login['warta_login'],
                  const.login['warta_password'])
        bot.calc_war()
        bot.apk_war()
        bot.input_translate_war(data)
        bot.input_personal_war()
        bot.input_prop_type_war()
        bot.input_address_war()
        bot.input_construction_year_war()
        bot.input_floor_war()
        bot.input_area_war()
        bot.input_finish_war()
        bot.input_construction_type_war()
        bot.input_declarations_war()
        bot.input_popup_war()
        bot.input_next_war()

        bot.wait()


def wie(data):
    with Condocalc() as bot:
        bot.login_page(const.login['wiener_url'])
        bot.login(const.login['wiener_login'],
                  const.login['wiener_password'])
        bot.calc_wie(const.WIE_CALC)
        bot.input_translate_wie(data)
        bot.input_period_wie()
        bot.input_follow_wie()
        bot.input_property_wie()
        bot.input_age_wie()
        bot.input_next_wie()

        bot.wait()


if __name__ == '__main__':

    pprint(customer_data(const.DATA_PATH))

    # calcs = [gen, war, wie]
    calcs = [war]
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        for calc in calcs:
            data = customer_data(const.DATA_PATH)
            executor.submit(calc, data)
        time.sleep(9999)
