from gww.condocalc2 import Condocalc
import gww.constants as const
from gww.variables import customer_data
import concurrent.futures


data = customer_data(const.DATA_PATH)


# def gen():
#     with Condocalc() as bot:
#         bot.login_page(const.login['generali_url'])
#         bot.login(const.login['generali_login'],
#                   const.login['generali_password'])
#         bot.calc_gen()
#         bot.apk_gen()
#         bot.input_gen(data)
#
#         bot.wait()


def war():
    with Condocalc() as bot:
        bot.login_page(const.login['warta_url'])
        bot.login(const.login['warta_login'],
                  const.login['warta_password'])
        bot.calc_war()
        bot.apk_war()
        bot.input_war(data)

        bot.wait()


# def wie():
#     with Condocalc() as bot:
#         bot.login_page(const.login['wiener_url'])
#         bot.login(const.login['wiener_login'],
#                   const.login['wiener_password'])
#         bot.calc_wie(const.WIE_CALC)
#         bot.input_wie(data)
#
#         bot.wait()


# calcs = [gen, war, wie]
# with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
#     for calc in calcs:
#         executor.submit(calc)




war()
