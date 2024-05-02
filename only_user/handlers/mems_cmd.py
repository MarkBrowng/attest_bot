import random
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup, State
from keyboards.inline_kb import mems_kb_answer_it, mems_kb_answer_cats, mems_kb_answer_other, mem_start_kb

from loader import bot, dp
from only_user.handlers.materials import MEMS_IT, MEMS_CATS, MEMS_OTHER

TEXT = 'Хотите еще мемов?'

class MemsStates(StatesGroup):
    mem_answer = State()
    mem_answer1 = State()
    mem_answer2 = State()
async def start_mems(callback: types.CallbackQuery):
    await callback.message.answer('На какую тему тебе скинуть МЭМ?', reply_markup=mem_start_kb())
    await MemsStates.mem_answer.set()

async def send_mem_it(callback: types.CallbackQuery):
    await bot.send_photo(callback.from_user.id, photo=random.choice(MEMS_IT), caption=TEXT,
                         reply_markup=mems_kb_answer_it())
    await MemsStates.mem_answer1.set()

async def answer_yes_mem_it(callback: types.CallbackQuery):
    await bot.send_photo(callback.from_user.id, photo=random.choice(MEMS_IT), caption=TEXT,
                         reply_markup=mems_kb_answer_it())
    await MemsStates.mem_answer.set()

async def send_mem_cats(callback: types.CallbackQuery):
    await bot.send_photo(callback.from_user.id, photo=random.choice(MEMS_CATS), caption=TEXT,
                         reply_markup=mems_kb_answer_cats())
    await MemsStates.mem_answer1.set()

async def answer_yes_mem_cats(callback: types.CallbackQuery):
    await bot.send_photo(callback.from_user.id, photo=random.choice(MEMS_CATS), caption=TEXT,
                         reply_markup=mems_kb_answer_cats())
    await MemsStates.mem_answer.set()

async def send_mem_other(callback: types.CallbackQuery):
    await bot.send_photo(callback.from_user.id, photo=random.choice(MEMS_OTHER), caption=TEXT,
                         reply_markup=mems_kb_answer_other())
    await MemsStates.mem_answer1.set()

async def answer_yes_mem_other(callback: types.CallbackQuery):
    await bot.send_photo(callback.from_user.id, photo=random.choice(MEMS_OTHER), caption=TEXT,
                         reply_markup=mems_kb_answer_other())
    await MemsStates.mem_answer.set()

def register_mems_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(start_mems, lambda callback: callback.data == 'mem')
    dp.register_callback_query_handler(send_mem_it,
                                       lambda callback: callback.data == 'mem_it' or callback.data == 'yes_mem_it',
                                       state=MemsStates.mem_answer)
    dp.register_callback_query_handler(answer_yes_mem_it,
                                       lambda callback: callback.data == 'yes_mem_it',
                                       state=MemsStates.mem_answer1)
    dp.register_callback_query_handler(send_mem_cats,
                                       lambda callback: callback.data == 'mem_cats' or callback.data == 'yes_mem_cats',
                                       state=MemsStates.mem_answer)
    dp.register_callback_query_handler(answer_yes_mem_cats, lambda callback: callback.data == 'yes_mem_cats',
                                       state=MemsStates.mem_answer1)
    dp.register_callback_query_handler(send_mem_other,
                                       lambda callback: callback.data == 'mem_other' or callback.data == 'yes_mem_other',
                                       state=MemsStates.mem_answer)
    dp.register_callback_query_handler(answer_yes_mem_other, lambda callback: callback.data == 'yes_mem_other',
                                       state=MemsStates.mem_answer1)