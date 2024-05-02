from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram import Bot, types, Dispatcher
from aiogram.dispatcher.filters import Text
from config import API_TOKEN
from only_user.handlers.materials import *
from keyboards.inline_kb import start_kb

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

async def cmd_start(message: types.Message, state: FSMContext):
    await bot.send_photo(message.from_user.id, photo= PHOTO_START, caption=TEXT_START, reply_markup=start_kb())
    await state.finish()

async def cmd_help(message: types.Message, state: FSMContext):
    await message.answer(text=TEXT_HELP)
    await state.finish()

async def cmd_back(callback: types.CallbackQuery, state: FSMContext):
    await bot.send_photo(callback.from_user.id, photo=PHOTO_START, caption=TEXT_START, reply_markup=start_kb())
    await state.finish()

async def cmd_back_reply(message: types.Message, state: FSMContext):
    await bot.send_photo(message.from_user.id, photo=PHOTO_START, caption=TEXT_START, reply_markup=start_kb())
    await state.finish()

def register_handlers_basic_cmd(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands='start', state='*')
    dp.register_message_handler(cmd_help, commands='help', state='*')
    dp.register_callback_query_handler(cmd_back, lambda callback: callback.data == 'back', state='*')
    dp.register_message_handler(cmd_back_reply, Text(equals='Назад⬅️'), state='*')