from aiogram import F, Router, html
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

import asyncio

import keyboards.keyboard as kb
from handlers.check_router import check_router

router = Router()

user_ip = {}
notification = {}

@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Привіт, {html.bold(message.from_user.full_name)}!\n"
                         f"Я створений щоб допомогти дізнатися чи є світло вбудинку💡 у цей важкий час",
                         reply_markup=kb.start)

@router.message(F.text == "/help")
async def help_handlers(message: Message):
    await message.answer("👋 Привіт! Я бот для перевірки доступності мережевих пристроїв. Ось що я можу зробити:\n\n"
                         "1️⃣ **Перевірка чи є світло** - Надішліть мені ваш публічний IP, і я перевірю доступність вашого роутера через пінг, HTTP та TCP порти.\n"
                         "2️⃣ **Інформація про роботу** - Ви можете дізнатися, чи є світло дома будучи на роботі.\n\n"
                         "💡 Для більш детальної допомоги або уточнень, звертайтесь із запитаннями!")

@router.message(F.text == "Параметри")
async def settings(message: Message):
    await message.answer("Ти в параметрах!", reply_markup=kb.settings)

@router.callback_query(F.data == "change_ip")
async def change_ip(callback: CallbackQuery):
    await callback.message.answer("Введіть публічний IP",)

@router.message(lambda message: message.text.count('.') == 3 and message.text.replace('.', '').isdigit())
async def record_ip(message: Message):
    user_id = message.from_user.id
    ip = message.text
    user_ip[user_id] = ip
    await message.answer(f"Ви ввели {user_ip[user_id]}", reply_markup=kb.start)

@router.message(F.text == "Відключити/Включити повідомлення")
async def toggle_notification(message: Message):
    user_id = message.from_user.id
    if user_ip.get(user_id) is None:
        await message.answer("Спочатку додайте свій IP!", reply_markup=kb.add_ip)
        return

    if notification.get(user_id, False):
        notification[user_id] = False
        await message.answer("Я вас не сповіщатиму про включення/відключення світла")
    else:
        notification[user_id] = True
        await message.answer("Тільки но світло буде відключено/ввімкнено я вас сповіщу")
        await check_light(message)

async def check_light(message: Message):
    if notification.get(message.from_user.id, False):
        previous_msg = ""
        while True:
            current_msg = await check_router(user_ip[message.from_user.id])
            if current_msg != previous_msg:
                await message.answer(text=current_msg)
                previous_msg = current_msg
            await asyncio.sleep(300)

@router.callback_query(F.data == "start_kb")
async def start_kb(callback: CallbackQuery):
    pass
