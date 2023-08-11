from aiogram import types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text

from app.create_bot import dp
from app.states import AdminMode

ADMIN_ID = ""
list_of_prem_users = []


@dp.message_handler(Text(equals=["⬅ Go to admin menu"]), state=AdminMode.admin_menu)
async def go_admin_menu(message: types.Message):
    await send_admin_menu(message)


@dp.message_handler(commands=['admin'], state='*')
async def send_admin_menu(message: types.Message):
    if int(message.from_user.id) == 420881832:
        message_response = "# *ADMIN MODE* \n"

        b1 = KeyboardButton("Add premium user")
        b2 = KeyboardButton("List premium users")
        b3 = KeyboardButton("⬅ Go to menu")
        buttons = ReplyKeyboardMarkup(resize_keyboard=True)
        buttons.row(b1).row(b2).row(b3)
        await AdminMode.admin_menu.set()
        await message.answer(message_response, parse_mode=types.ParseMode.MARKDOWN, reply_markup=buttons)


@dp.message_handler(Text(equals="Add premium user"), state=AdminMode.admin_menu)
async def add_prem_user(message: types.Message):
    message_response = "Send user telegream_id"

    await AdminMode.add_user.set()
    await message.answer(message_response, reply_markup=ReplyKeyboardRemove())


@dp.message_handler(state=AdminMode.add_user)
async def save_prem_user(message: types.Message):
    telegram_id = message.text
    list_of_prem_users.append(int(telegram_id))

    message_response = "Saved"
    buttons = [
        KeyboardButton(text="⬅ Go to admin menu"),
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard=[buttons], resize_keyboard=True)

    await AdminMode.admin_menu.set()
    await message.answer(message_response, reply_markup=reply_markup)


@dp.message_handler(Text(equals="List premium users"), state=AdminMode.admin_menu)
async def send_list_prem_user(message: types.Message):
    message_response = "# LIST # \n \n"
    for i in range(len(list_of_prem_users)):
        message_response += f"{i+1}. {list_of_prem_users[i]} \n"
    await message.answer(message_response, parse_mode=types.ParseMode.MARKDOWN)
