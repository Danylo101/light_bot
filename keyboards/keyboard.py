from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

start = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, input_field_placeholder="Меню",
    keyboard=[
        [KeyboardButton(text="Параметри")],
        [KeyboardButton(text="Відключити/Включити повідомлення")]
])

settings = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Включити/виключити логування", callback_data="log")],
        [InlineKeyboardButton(text="Змінити IP адресу", callback_data="change_ip")],
])

add_ip = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Додати IP", callback_data="change_ip")],
    ]
)