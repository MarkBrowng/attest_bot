from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from keyboards.inline_kb import add_to_cart_kb, back_to_usershop_kb
from loader import db, dp
from only_user.shop_game.callbacks import AdminOrUserStates

async def show_products(message: types.Message):
    await AdminOrUserStates.user_catalog.set()
    products = db.get_all_products()
    for product in products:
        product_message = f"{product[1]}\n{product[3]}\nЦена: {product[4]} рублей"
        await message.answer_photo(photo=product[2], caption=product_message, reply_markup=add_to_cart_kb(product[0]))
    await message.answer('->Вернуться в меню<-', reply_markup=back_to_usershop_kb())

def register_catalog_handlers(dp: Dispatcher):
    dp.register_message_handler(show_products, Text(equals='🎮Список товаров'), state=AdminOrUserStates.user_view)
