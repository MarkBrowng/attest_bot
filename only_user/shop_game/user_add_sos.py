from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ContentType
from loader import db, dp
from keyboards.inline_kb import choose_type_sos_kb, back_to_usershop_kb
from only_user.shop_game.callbacks import AdminOrUserStates

async def choose_type_sos(message: types.Message):
    await AdminOrUserStates.user_choose_type_sos.set()
    await message.answer('С какой целью обращаетесь к админу?', reply_markup=choose_type_sos_kb())

async def write_question(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['type'] = callback.data
    await callback.message.answer('Напишите свой вопрос')
    await AdminOrUserStates.user_write_sos.set()

async def add_question(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    async with state.proxy() as data:
        data['question'] = message.text
        db.add_question(user_id=user_id, type=data['type'], appeal=data['question'])
        await message.answer('Спасибо за обращение!\nАдмин в скором времени свяжется с Вами🙂', reply_markup=back_to_usershop_kb())
    await state.finish()

async def write_complaint(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['type'] = callback.data
    await callback.message.answer('Напишите свою жалобу')
    await AdminOrUserStates.user_write_sos.set()

async def add_complaint(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    async with state.proxy() as data:
        data['complaint'] = message.text
        db.add_question(user_id=user_id, type=data['type'], appeal=data['complaint'])
        await message.answer('Спасибо за обращение!\nАдмин в скором времени свяжется с Вами🙂', reply_markup=back_to_usershop_kb())
    await state.finish()

def register_add_sos_handlers(dp: Dispatcher):
    dp.register_message_handler(choose_type_sos, Text(equals='❓Обратиться в техподдержку'), state=AdminOrUserStates.user_view)
    dp.register_callback_query_handler(write_question, lambda callback: callback.data == 'question',
                                       state=AdminOrUserStates.user_choose_type_sos)
    dp.register_message_handler(add_question, content_types=ContentType.TEXT, state=AdminOrUserStates.user_write_sos)
    dp.register_callback_query_handler(write_complaint, lambda callback: callback.data == 'complaint',
                                       state=AdminOrUserStates.user_choose_type_sos)
    dp.register_message_handler(add_complaint, content_types=ContentType.TEXT, state=AdminOrUserStates.user_write_sos)



