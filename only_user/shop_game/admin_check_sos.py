from aiogram.dispatcher.filters import Text
from keyboards.inline_kb import back_to_adminshop_kb
from loader import db, dp
from aiogram import types, Dispatcher

from only_user.shop_game.callbacks import AdminOrUserStates


async def check_sos(message: types.Message):
    appeals = db.get_appeals()
    for appeal in appeals:
        await message.answer(text=f'ID пользователя: {appeal[0]}\n'
                                  f'Тип обращения: {appeal[1]}\n'
                                  f'Входящее обращение: {appeal[2]}')
    await message.answer('->Вернуться в меню<-', reply_markup=back_to_adminshop_kb())

def register_check_sos_handlers(dp: Dispatcher):
    dp.register_message_handler(check_sos, Text(equals='🆘Просмотреть вопросы/жалобы'),
                                state=AdminOrUserStates.admin_view)