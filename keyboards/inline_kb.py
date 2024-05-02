from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

button_back = InlineKeyboardButton('Назад⬅️', callback_data='back')
button_back_shop_user = InlineKeyboardButton('Назад⬅️', callback_data='back_shop_user')
button_back_shop_admin = InlineKeyboardButton('Назад⬅️', callback_data='back_shop_admin')

'---------------------------------------------Клавиатуры базовых команд------------------------------------------------'
def start_kb():
    kb = InlineKeyboardMarkup(row_width=2)
    button1 = InlineKeyboardButton('🌤Погода🌧', callback_data='weather')
    button2 = InlineKeyboardButton('🎮Магазин игр🎮', callback_data='gameshop')
    button3 = InlineKeyboardButton('💸Курс рубля💸', callback_data='exchange_rate')
    button4 = InlineKeyboardButton('🤣Мемчик🤣', callback_data='mem')
    kb.add(button1, button2).add(button3, button4)
    return kb

def back_kb():
    kb = InlineKeyboardMarkup(row_width=2).add(button_back)
    return kb

'-----------------------------------------------Клавиатуры команд МЕМОВ------------------------------------------------'
def mem_start_kb():
    kb = InlineKeyboardMarkup(row_width=2)
    button1 = InlineKeyboardButton('Смешные котики😹', callback_data='mem_cats')
    button2 = InlineKeyboardButton('Мемы программиста🖥', callback_data='mem_it')
    button3 = InlineKeyboardButton('Разные Мемы🤪', callback_data='mem_other')
    kb.add(button1, button2, button3).add(button_back)
    return kb

def mems_kb_answer_it():
    kb = InlineKeyboardMarkup(row_width=2)
    button1 = InlineKeyboardButton('Да!', callback_data='yes_mem_it')
    kb.add(button1, button_back)
    return kb

def mems_kb_answer_cats():
    kb = InlineKeyboardMarkup(row_width=2)
    button1 = InlineKeyboardButton('Да!', callback_data='yes_mem_cats')
    kb.add(button1, button_back)
    return kb

def mems_kb_answer_other():
    kb = InlineKeyboardMarkup(row_width=2)
    button1 = InlineKeyboardButton('Да!', callback_data='yes_mem_other')
    kb.add(button1, button_back)
    return kb

'--------------------------------------------Клавиатуры команд магазины игр--------------------------------------------'
def user_or_admin_kb():
    kb = InlineKeyboardMarkup(row_width=2)
    button1 = InlineKeyboardButton('🤓Пользователь', callback_data='user')
    button2 = InlineKeyboardButton('😎Админ', callback_data='admin')
    kb.add(button1, button2)
    return kb

def back_to_usershop_kb():
    kb = InlineKeyboardMarkup(row_width=2).add(button_back_shop_user)
    return kb

def back_to_adminshop_kb():
    kb = InlineKeyboardMarkup(row_width=2).add(button_back_shop_admin)
    return kb

def add_to_cart_kb(product_id):
    kb = InlineKeyboardMarkup()
    button = InlineKeyboardButton(text="Добавить в корзину", callback_data=f"add_to_cart_{product_id}")
    kb.add(button)
    return kb

def cart_kb(product_id):
    kb = InlineKeyboardMarkup(row_width=2)
    button1 = InlineKeyboardButton('Удалить с корзины', callback_data=f'remove_{product_id}')
    button2 = InlineKeyboardButton('Купить игру', callback_data=f'buy_{product_id}')
    kb.add(button1).add(button2)
    return kb

def add_game_kb():
    kb = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(
        '✅Добавить игру', callback_data='add_game'), button_back_shop_admin)
    return kb

def choose_type_sos_kb():
    kb = InlineKeyboardMarkup(row_width=2)
    button1 = InlineKeyboardButton('😡Жалоба', callback_data='complaint')
    button2 = InlineKeyboardButton('🤔Вопрос', callback_data='question')
    kb.add(button1, button2).add(button_back_shop_user)
    return kb