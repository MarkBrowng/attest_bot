import requests
from aiogram import types, Bot, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup
from config import API_TOKEN
from keyboards.inline_kb import back_kb, start_kb
from keyboards.reply_kb import rates_keyboard
from loader import storage
from only_user.handlers.materials import PHOTO_START, TEXT_START

bot = Bot(token=API_TOKEN)
dp: Dispatcher = Dispatcher(bot, storage=storage)

class ExchangeRateStates(StatesGroup):
    rate_waiting = State()

async def start_exchange_rate(callback: types.CallbackQuery):
    await callback.message.answer(text='Выберите валюту перевода!', reply_markup=rates_keyboard())
    await ExchangeRateStates.rate_waiting.set()

async def start_exchange_rate1(message: types.Message):
    await message.answer(text='Выберите валюту перевода!', reply_markup=rates_keyboard())
    await ExchangeRateStates.rate_waiting.set()

async def exchange1(message: types.Message):
    data = requests.get('https://api.exchangerate-api.com/v4/latest/RUB').json()
    yuan_rate = data['rates']['CNY']
    await message.answer(f"🇱🇷Курс рубля по отношению к юаню: 1 рубль -> {yuan_rate} юань", reply_markup=back_kb())

async def exchange2(message: types.Message):
    data = requests.get('https://api.exchangerate-api.com/v4/latest/RUB').json()
    dollar_rate = data['rates']['USD']
    await message.answer(f"🇱🇷Курс рубля по отношению к доллару: 1 рубль -> {dollar_rate} доллара(-ов)", reply_markup=back_kb())

async def exchange3(message: types.Message):
    data = requests.get('https://api.exchangerate-api.com/v4/latest/RUB').json()
    tenge_rate = data['rates']['KZT']
    await message.answer(f"🇰🇿Курс рубля по отношению к тенге: 1 рубль -> {tenge_rate} тенге", reply_markup=back_kb())

async def exchange4(message: types.Message):
    data = requests.get('https://api.exchangerate-api.com/v4/latest/RUB').json()
    peso_rate = data['rates']['MXN']
    await message.answer(f"🇮🇳Курс рубля по отношению к песо: 1 рубль -> {peso_rate} песо", reply_markup=back_kb())

async def exchange5(message: types.Message):
    data = requests.get('https://api.exchangerate-api.com/v4/latest/RUB').json()
    rupiy_rate = data['rates']['INR']
    await message.answer(f"🇲🇽Курс рубля по отношению к рупию: 1 рубль -> {rupiy_rate} рупий", reply_markup=back_kb())

async def ne_tuda_nazhal(message: types.Message):
    keyboard = ReplyKeyboardMarkup().add('🇱🇷Юань', '🇱🇷Доллар', '🇰🇿Тенге').add('🇲🇽Песо', '🇮🇳Рупий')
    await message.reply(text='Выберите валюту!!!', reply_markup=keyboard)
    await ExchangeRateStates.rate_waiting.set()

async def back_cmd(message: types.Message, state: FSMContext):
    await bot.send_photo(message.from_user.id, photo= PHOTO_START, caption=TEXT_START, reply_markup=start_kb())
    await state.finish()

def register_handlers_exchange_rate(dp: Dispatcher):
    dp.register_callback_query_handler(start_exchange_rate, lambda callback: callback.data == 'exchange_rate')
    dp.register_message_handler(start_exchange_rate1, commands='exchange_rate')
    dp.register_message_handler(exchange1, Text(equals='🇱🇷Юань'), state=ExchangeRateStates.rate_waiting)
    dp.register_message_handler(exchange2, Text(equals='🇱🇷Доллар'), state=ExchangeRateStates.rate_waiting)
    dp.register_message_handler(exchange3, Text(equals='🇰🇿Тенге'), state=ExchangeRateStates.rate_waiting)
    dp.register_message_handler(exchange4, Text(equals='🇲🇽Песо'), state=ExchangeRateStates.rate_waiting)
    dp.register_message_handler(exchange5, Text(equals='🇮🇳Рупий'), state=ExchangeRateStates.rate_waiting)
    dp.register_message_handler(ne_tuda_nazhal, Text(equals='💸 Курс рубля по отношению к 💸'), state=ExchangeRateStates.rate_waiting)
