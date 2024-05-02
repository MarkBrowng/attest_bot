from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from keyboards.inline_kb import user_or_admin_kb, back_kb
from keyboards.reply_kb import shop_menu_user_kb, shop_menu_admin_kb
from loader import bot, dp
from config import ADMINS

TEXT_MENU = ('Добро пожаловать в магазин игр "GameShop"🎮 \n'
             'В нашем ассортименте есть игры разных жанров. Среди них:\n'
             ' 🕹 Стратегии\n 🕹 Шутеры\n 🕹 РПГ\n 🕹 Выживание\n')
PHOTO = 'https://kartinki.pics/uploads/posts/2021-07/1625725215_28-kartinkin-com-p-dzhoistik-art-art-krasivo-28.jpg'

class AdminOrUserStates(StatesGroup):
    admin_view = State()
    admin_add_product = State()
    user_view = State()
    user_catalog = State()
    user_cart = State()
    user_choose_type_sos = State()
    user_write_sos = State()

async def admin_or_user_callback(callback: types.CallbackQuery):
    await callback.message.answer('Для продолжения работы мне нужно знать, кем Вы являетесь😉',
                                  reply_markup=user_or_admin_kb())

async def admin_or_user_cmd(message: types.Message):
    await message.answer('Для продолжения работы мне нужно знать, кем Вы являетесь😉',
                                  reply_markup=user_or_admin_kb())
async def start_menu_user(callback: types.CallbackQuery):
    await AdminOrUserStates.user_view.set()
    await bot.send_photo(callback.from_user.id, photo=PHOTO, caption=TEXT_MENU, reply_markup=shop_menu_user_kb())

async def start_menu_admin(callback: types.CallbackQuery):
    if callback.from_user.id in ADMINS:
        await AdminOrUserStates.admin_view.set()
        await bot.send_photo(callback.from_user.id, photo=PHOTO, caption=TEXT_MENU, reply_markup=shop_menu_admin_kb())
    else:
        await callback.answer('Вы не являетесь админом!')

async def back_to_menu_user(callback: types.CallbackQuery):
    await AdminOrUserStates.user_view.set()
    await bot.send_photo(callback.from_user.id, photo=PHOTO, caption=TEXT_MENU, reply_markup=shop_menu_user_kb())

async def back_to_menu_admin(callback: types.CallbackQuery):
    await AdminOrUserStates.admin_view.set()
    await bot.send_photo(callback.from_user.id, photo=PHOTO, caption=TEXT_MENU, reply_markup=shop_menu_admin_kb())

def register_callbacks_shopgame(dp: Dispatcher):
    dp.register_callback_query_handler(admin_or_user_callback, lambda callback: callback.data == 'gameshop')
    dp.register_message_handler(admin_or_user_cmd, commands='gameshop')
    dp.register_callback_query_handler(start_menu_user, lambda callback: callback.data == 'user', state='*')
    dp.register_callback_query_handler(start_menu_admin, lambda callback: callback.data == 'admin', state='*')
    dp.register_callback_query_handler(back_to_menu_user, lambda callback: callback.data == 'back_shop_user', state='*')
    dp.register_callback_query_handler(back_to_menu_admin, lambda callback: callback.data == 'back_shop_admin', state='*')

