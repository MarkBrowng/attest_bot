import uuid
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ContentType
from filters import IsAdmin
from keyboards.inline_kb import back_to_adminshop_kb, add_game_kb
from loader import dp, bot, db
from only_user.shop_game.callbacks import AdminOrUserStates

class AddProductStates(StatesGroup):
    name = State()
    photo = State()
    description = State()
    price = State()

async  def add_product(message: types.Message):
    await AdminOrUserStates.admin_add_product.set()
    await message.answer('Для добавления игры нажмите еще раз на кнопку)))', reply_markup=add_game_kb())

async def start_add_product(callback: types.CallbackQuery):
    await callback.message.answer('Введите название игры', reply_markup=back_to_adminshop_kb())
    await AddProductStates.name.set()

async def add_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await AddProductStates.next()
    await message.answer('Отправьте фото игры', reply_markup=back_to_adminshop_kb())

async def add_photo(message: types.Message, state: FSMContext):
    fileID = message.photo[-1].file_id
    file_info = await bot.get_file(fileID)
    downloaded_file = (await bot.download_file(file_info.file_path)).read()
    await AddProductStates.next()
    async with state.proxy() as data:
        data['photo'] = downloaded_file
    await message.answer('Введите описание игры', reply_markup=back_to_adminshop_kb())

async def add_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    await AddProductStates.next()
    await message.answer('Введите цену товара', reply_markup=back_to_adminshop_kb())

async def add_price(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Пожалуйста, введите целое число для цены товара.")
        return
    async with state.proxy() as data:
        data['price'] = message.text
        product_id = str(uuid.uuid4())
        db.add_product(product_id=product_id, name=data['name'], photo=data['photo'], description=data['description'],
                       price=data['price'])
        await message.answer('Игра успешно добавлена в каталог!', reply_markup=back_to_adminshop_kb())
    await state.finish()


def register_add_product_handlers(dp: Dispatcher):
    dp.register_message_handler(add_product, IsAdmin(), Text(equals='🏪Добавить товар'),
                                state=AdminOrUserStates.admin_view)
    dp.register_callback_query_handler(start_add_product, IsAdmin(), lambda callback: callback.data == 'add_game',
                                       state= AdminOrUserStates.admin_add_product)
    dp.register_message_handler(add_name, IsAdmin(), content_types=ContentType.TEXT,
                                state=AddProductStates.name)
    dp.register_message_handler(add_photo, IsAdmin(), content_types=ContentType.PHOTO,
                                state=AddProductStates.photo)
    dp.register_message_handler(add_description, IsAdmin(), content_types=ContentType.TEXT,
                                state=AddProductStates.description)
    dp.register_message_handler(add_price, IsAdmin(), content_types=ContentType.TEXT,
                                state=AddProductStates.price)
