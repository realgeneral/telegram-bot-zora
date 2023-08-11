from aiogram import types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from app.create_bot import dp
from app.states import UserFollowing


@dp.message_handler(Text(equals=["⬅ Go to menu"]), state='*')
async def go_menu(message: types.Message, state: FSMContext):
    await UserFollowing.wallet_menu.set()
    await send_menu(message, state)


@dp.message_handler(state=UserFollowing.wallet_menu)
async def send_menu(message: types.Message, state: FSMContext):
    data = await state.get_data()
    private_keys = list(data.get("private_keys"))
    message_response = "# *Private key`s* \n"
    for i in range(len(private_keys)):
        message_response += f"{i+1}. *{private_keys[i][0:6]}...{private_keys[i][-4:]}* \n"
    message_response += "\n Choose an action:"

    b1 = KeyboardButton("👝 Check balance")
    b2 = KeyboardButton("💸 Tap 2 earn")
    b3 = KeyboardButton("🆕 New keys")
    b4 = KeyboardButton("🔑 Check keys")

    buttons = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons.row(b1).row(b2, b4).row(b3)

    await UserFollowing.choose_point.set()
    await message.answer(message_response, parse_mode=types.ParseMode.MARKDOWN,
                         reply_markup=buttons)
