from aiogram import types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from app.create_bot import dp
from app.states import UserFollowing


@dp.message_handler(Text(equals=["⬅ Go to menu"]), state='*')
async def go_menu(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == UserFollowing.tap_to_earn.state:
        await state.update_data(stop_flag=True)

    data = await state.get_data()
    private_keys = data.get("private_keys")

    if private_keys is None:
        private_keys = ["-"]
        await state.update_data(private_keys=private_keys)

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
    b2 = KeyboardButton("⛽️ Check GWEI")
    b3 = KeyboardButton("💸 Tap 2 earn")
    b4 = KeyboardButton("🆕 New keys")
    b5 = KeyboardButton("🔑 Check keys")

    buttons = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons.row(b3).row(b1, b2).row(b4, b5)

    await UserFollowing.choose_point.set()
    await message.answer(message_response, parse_mode=types.ParseMode.MARKDOWN,
                         reply_markup=buttons)
