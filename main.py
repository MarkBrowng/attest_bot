from aiogram import executor
import logging
from aiogram.dispatcher.filters.state import StatesGroup, State
from only_user.handlers.basic_cmd import register_handlers_basic_cmd
from only_user.handlers.exchange_rate import register_handlers_exchange_rate
from loader import dp
from only_user.handlers.mems_cmd import register_mems_handlers
from only_user.handlers.wethear import register_weather_handlers
from only_user.shop_game.add_products import register_add_product_handlers
from only_user.shop_game.admin_check_sos import register_check_sos_handlers
from only_user.shop_game.callbacks import register_callbacks_shopgame
from only_user.shop_game.cart import register_cart_handlers
from only_user.shop_game.catalog import register_catalog_handlers
from only_user.shop_game.user_add_sos import register_add_sos_handlers

logging.basicConfig(level=logging.INFO)

class WeatherStates(StatesGroup):
    weather_waiting = State()

def main():
    register_callbacks_shopgame(dp)
    register_add_product_handlers(dp)
    register_catalog_handlers(dp)
    register_cart_handlers(dp)
    register_add_sos_handlers(dp)
    register_check_sos_handlers(dp)
    register_handlers_exchange_rate(dp)
    register_handlers_basic_cmd(dp)
    register_weather_handlers(dp)
    register_mems_handlers(dp)
    executor.start_polling(dp, skip_updates=True)

if __name__ == '__main__':
    main()
