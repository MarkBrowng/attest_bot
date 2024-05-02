from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import CallbackQuery
from aiogram.utils import executor
from config import API_TOKEN

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


class States(StatesGroup):
    some_state = State()


# Callback handler для inline кнопки
@dp.callback_query_handler(lambda callback_query: True)
async def process_callback(callback_query: CallbackQuery, state: FSMContext):
    # Получаем данные, отправленные с inline кнопкой
    data = callback_query.data

    # В зависимости от данных изменяем состояние
    if data == 'button1':
        await state.update_data(state_value='value1')
    elif data == 'button2':
        await state.update_data(state_value='value2')

    # Отправляем сообщение об успешном изменении состояния
    await callback_query.answer(text="Состояние изменено")


# Функция для отправки сообщения с inline кнопками
async def send_inline_keyboard(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text="Кнопка 1", callback_data='button1')
    button2 = types.InlineKeyboardButton(text="Кнопка 2", callback_data='button2')
    keyboard.add(button1, button2)
    await message.reply("Выберите кнопку:", reply_markup=keyboard)


# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await States.some_state.set()
    await send_inline_keyboard(message)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)