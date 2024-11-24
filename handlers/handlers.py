from aiogram import F, Router, html
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

import asyncio

import keyboards.keyboard as kb
from handlers.check_router import check_router
from handlers.ip import is_valid_ip

router = Router()

user_ip = {}
notification = {}
logg = {}
active_tasks = {}

@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Привіт, {html.bold(message.from_user.full_name)}!\n"
                         f"Я створений щоб допомогти дізнатися чи є світло вбудинку💡 у цей важкий час",
                         reply_markup=kb.start)
    await message.answer("Введіть публічний IP вашого роутера:"
                         "\n\nЯкщо ви не знаєте як дізнатись свій IP натисніть /chek_ip", reply_markup=kb.add_ip)

@router.message(F.text == "/about")
async def about(message: Message):
    await message.answer("👋 Привіт! Я бот для перевірки доступності мережевих пристроїв. Ось що я можу зробити:\n\n"
                         "1️⃣ **Перевірка чи є світло** - Надішліть мені ваш публічний IP, і я перевірю доступність вашого роутера через пінг, HTTP та TCP порти.\n"
                         "2️⃣ **Інформація про роботу** - Ви можете дізнатися, чи є світло дома будучи на роботі.\n\n"
                         "💡 Для більш детальної допомоги або уточнень, звертайтесь із запитаннями!\n\n")

@router.message(F.text == "Параметри")
async def settings(message: Message):
    await message.answer("Ти в параметрах⚙️", reply_markup=kb.settings)

@router.callback_query(F.data == "change_ip")
async def change_ip(callback: CallbackQuery):
    await callback.message.answer("Введіть публічну IP адресу",)

@router.message(lambda message: message.text.count('.') == 3 and message.text.replace('.', '').isdigit())
async def record_ip(message: Message):
    user_id = message.from_user.id
    ip = message.text
    if not await is_valid_ip(ip):
        await message.answer(f"❌ Ви ввели некоректну IP-адресу {ip}. Перевірте її формат (наприклад, 192.168.1.1).")
        return

    user_ip[user_id] = ip
    await message.answer(f"✅ IP-адреса {user_ip[user_id]} успішно збережена!", reply_markup=kb.start)


@router.message(F.text == "Відключити/Включити повідомлення")
async def toggle_notification(message: Message):
    user_id = message.from_user.id
    if user_ip.get(user_id) is None:
        await message.answer("❌ Спочатку додайте свій IP!", reply_markup=kb.add_ip)
        return

    if notification.get(user_id, False):
        notification[user_id] = False
        await message.answer("Я вас не сповіщатиму про включення/відключення світла✉️")
    else:
        notification[user_id] = True
        await message.answer("Тільки но світло буде відключено/ввімкнено я вас сповіщу✉️")
        await check_light(message)

async def check_light(message: Message):
    user_id = message.from_user.id
    if user_id in active_tasks:
        return True

    active_tasks[user_id] = True
    try:
        previous_msg = ""
        while notification.get(user_id, False):
            current_msg = await check_router(user_ip[user_id], logg.get(user_id, False))
            if current_msg != previous_msg:
                await message.answer(text=current_msg)
                previous_msg = current_msg
            await asyncio.sleep(300)
    except asyncio.CancelledError:
        pass
    finally:
        active_tasks.pop(user_id, None)

@router.callback_query(F.data == "log")
async def log(callback: CallbackQuery):
    if logg.get(callback.from_user.id, False):
        logg[callback.from_user.id] = False
        await callback.message.answer("Відправка логів виключена✉️")
    else:
        logg[callback.from_user.id] = True
        await callback.message.answer("Відпрака логів включена✉️")

@router.message(F.text == "/chek_ip" )
async def chek_ip(message: Message):
    await message.answer("Перейдіть за посиланням https://api.ipify.org та скопіюйте результат.\n\nЯкщо цей IP не працює то вам потрібно відкрити web-сторінку вашого роутера\n(Переважно це http://192.168.0.1 або https://192.168.1.1) і скопіювати публічний IP\n\nЯкщо бот надалі пише що світла немає то ваш роутер не відповідає на зовнішні запити")

@router.message(F.text == "/help")
async def help_handler(message: Message):
    await message.answer( """
Якщо бот постійно повідомляє, що світла немає, ось кілька кроків, які варто виконати:

1. **Перевірте свій роутер**:
   - Упевніться, що він увімкнений і працює.
   - Перевірте, чи горять індикатори на роутері.

2. **Перевірте підключення до інтернету**:
   - Спробуйте підключитися до Wi-Fi або кабелю інтернету з іншого пристрою.
   - Перевірте доступність веб-сторінок.

3. **Перевірте IP-адресу**:
   - Переконайтеся, що ви вказали коректну IP-адресу роутера для бота.
   - Якщо IP-адреса динамічна, можливо, вона змінилася — уточніть її у налаштуваннях роутера.

4. **Увімкніть логування**:
   - Використовуйте команду `/log`, щоб увімкнути логування помилок.
   - Перегляньте повідомлення з логами для детальної інформації.

5. **Зверніться до провайдера**:
   - Якщо роутер працює, але інтернет недоступний, зв’яжіться зі своїм провайдером для уточнення деталей.

6. **Перезапустіть моніторинг**:
   - Використовуйте команду `/monitor_off`, щоб вимкнути моніторинг, а потім `/monitor_on`, щоб увімкнути його знову.

Якщо проблема не вирішується, напишіть розробнику бота.
        """)

@router.message()
async def msg(message: Message):
    await command_start_handler(message)
