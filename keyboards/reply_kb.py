from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

button_back = KeyboardButton('Назад⬅️')

# клавиатура команд мемов
def mem_start_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button1 = KeyboardButton('Смешные котики😹')
    button2 = KeyboardButton('Разные Мемы🤪')
    button3 = KeyboardButton('Мемы программиста🖥')
    kb.add(button1, button2, button3).add(button_back)
    return kb

# клавиатура команды курса рубля
def rates_keyboard():
    kb_rates = (ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add('💸 Курс рубля по отношению к 💸')
                .add('🇱🇷Юань', '🇱🇷Доллар', '🇰🇿Тенге').add('🇲🇽Песо', '🇮🇳Рупий'))
    return kb_rates

# клавиатуры команд магазины игр
def shop_menu_user_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button1 =KeyboardButton('🎮Список товаров')
    button2 = KeyboardButton('🛒Корзина')
    button3 = KeyboardButton('❓Обратиться в техподдержку')
    kb.add(button1, button2).add(button3).add(button_back)
    return kb

def shop_menu_admin_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button1 = KeyboardButton('🏪Добавить товар')
    button2 = KeyboardButton('🆘Просмотреть вопросы/жалобы')
    kb.add(button1, button2).add(button_back)
    return kb

