from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import ContentType

from config import UKASSA_TOKEN
from keyboards.inline_kb import back_to_usershop_kb, cart_kb
from loader import dp, db, bot
from only_user.shop_game.callbacks import AdminOrUserStates


async def add_to_cart(callback: types.CallbackQuery):
    product_id = callback.data.split('_')[-1]
    db.move_to_cart(product_id)
    await callback.message.answer('Игра успешно добавлена в корзину!')

async def show_games_in_cart(message: types.Message):
    await AdminOrUserStates.user_cart.set()
    products = db.get_all_products_in_cart()
    for product in products:
        product_message = f"{product[1]}\n{product[3]}\nЦена: {product[4]} рублей"
        await message.answer_photo(photo=product[2], caption=product_message, reply_markup=cart_kb(product[0]))
    await message.answer('->Вернуться в меню<-', reply_markup=back_to_usershop_kb())

async def buy_game_cmd(callback: types.CallbackQuery):
    product_id = callback.data.split('_')[-1]
    product = db.select_product_in_cart(product_id)
    await bot.send_invoice(chat_id=callback.from_user.id, title=f'Покупка игры {product[1]}',
                           description=product[3], payload='payment', provider_token=UKASSA_TOKEN,
                           currency='RUB', start_parameter='test_bot', prices=[{'label': 'Руб', 'amount': int(str(product[4]) + '00')}])
    db.move_to_products(product_id)

async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

async def process_pay(message: types.Message):
    if message.successful_payment.invoice_payload == 'payment':
        await bot.send_message(message.from_user.id, text='Поздравляю с покупкой игры!', reply_markup=back_to_usershop_kb())
def register_cart_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(add_to_cart, lambda callback: callback.data.startswith('add_to_cart'),
                                       state=AdminOrUserStates.user_catalog)
    dp.register_message_handler(show_games_in_cart, Text(equals='🛒Корзина'), state=AdminOrUserStates.user_view)
    dp.register_callback_query_handler(buy_game_cmd, lambda callback: callback.data.startswith('buy_'),
                                       state=AdminOrUserStates.user_cart)
    dp.register_pre_checkout_query_handler(process_pre_checkout_query, state='*')
    dp.register_message_handler(process_pay, content_types=ContentType.SUCCESSFUL_PAYMENT, state='*')
