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
    await send_menu(message)


@dp.message_handler(state=UserFollowing.wallet_menu)
async def send_menu(message: types.Message):

    message_response = "🫡 Waiting for your instructions...\n " \
                        "🔽 Choose the button below 🔽"

    # b1 = KeyboardButton("👝 Check balance")
    b2 = KeyboardButton("⛽️ Check GWEI")
    b3 = KeyboardButton("💸 Start script")
    b4 = KeyboardButton("➕ Load new wallets")
    # b5 = KeyboardButton("🔑 Check keys")
    b6 = KeyboardButton("ℹ️ FAQ")

    buttons = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons.row(b3).row(b2, b4).row(b6)

    await UserFollowing.choose_point.set()
    await message.answer(message_response, parse_mode=types.ParseMode.MARKDOWN,
                         reply_markup=buttons)
