from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

start = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, input_field_placeholder="Меню",
    keyboard=[
        [KeyboardButton(text="Параметри")],
        [KeyboardButton(text="Відключити/Включити повідомлення")]
])

settings = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Включити логування", url="http://test.com")],
        [InlineKeyboardButton(text="Змінити IP адресу", callback_data="change_ip")],
        [InlineKeyboardButton(text="Назад", callback_data="start_kb")],
])

add_ip = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Додати IP", callback_data="change_ip")],
    ]
)