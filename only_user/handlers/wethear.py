import requests
import datetime
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import API_TOKEN, WEATHER_API
from aiogram import Bot, Dispatcher, types
from keyboards.inline_kb import back_kb
from loader import storage

class WeatherStates(StatesGroup):
    weather_waiting = State()

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)

async def start_weather(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text='Чтобы узнать погоду Введи название города.')
    await state.update_data(state_value=callback.data)
    await WeatherStates.weather_waiting.set()

async def cmd_start_weather(message: types.Message):
    await message.answer(text='Чтобы узнать погоду Введи название города.')
    await WeatherStates.weather_waiting.set()

async def get_weather(message: types.Message, state: FSMContext):
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Ясно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }
    try:
        #запрашиваем погоду
        r = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={WEATHER_API}&units=metric')
        data = r.json()

        city = data['name']
        cur_waether = data['main']['temp']

        weather_description = data['weather'][0]['main']
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = 'Посмотри в окно сам'

        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        sunrise_tenpstamp = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        sunset_timedtamp = datetime.datetime.fromtimestamp(data['sys']['sunset'])
        lenght_of_the_day = sunset_timedtamp - sunrise_tenpstamp
        wind = data['wind']['speed']

        await message.answer(f'{datetime.datetime.now().strftime("%d.%m.%Y %H:%M")}\n'
                            f'Погода в городе: {city}\n🌡Температура: {cur_waether} C - {wd}\n'
                            f'🌅Восход солнца: {sunrise_tenpstamp}\n'
                            f'🌄Закат солнца: {sunset_timedtamp}\n'
                            f'🔅Продолжительность дня: {lenght_of_the_day}\n'
                            f'🗻Давление: {pressure} hPa\n💧Влажность: {humidity} %\n'
                            f'💨Скорость ветра: {wind} м/с', reply_markup=back_kb())

    except Exception as eer:
        await message.reply('Пожалуйста, проверьте название города')
    finally:
        await state.finish()

def register_weather_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(start_weather, lambda callback: callback.data == 'weather')
    dp.register_message_handler(cmd_start_weather, commands='weather')
    dp.register_message_handler(get_weather, state=WeatherStates.weather_waiting)
