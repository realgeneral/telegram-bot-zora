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
    private_key = data.get("private_key")

    b1 = KeyboardButton("👝 Check balance")
    b2 = KeyboardButton("⛏ Mint nft")
    b3 = KeyboardButton("💸 Bridge")
    b4 = KeyboardButton("🆕 New keys")
    b5 = KeyboardButton("🔑 Check keys")

    buttons = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons.row(b1).row(b2, b3).row(b4, b5)

    await UserFollowing.choose_point.set()
    await message.answer(f"# Private key *{private_key[0:6]}...{private_key[-4:]}* \n"
                         f"Choose an action:", parse_mode=types.ParseMode.MARKDOWN,
                         reply_markup=buttons)
