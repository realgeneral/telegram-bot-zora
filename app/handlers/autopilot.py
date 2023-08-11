import asyncio

from aiogram import types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from app.create_bot import dp
from app.states import UserFollowing


# @dp.message_handler(Text(equals=["⬅ Go to menu"]), state='*')
# async def go_menu(message: types.Message, state: FSMContext):
#     await UserFollowing.wallet_menu.set()
#     await send_menu(message, state)


# @dp.message_handler(Text(equals="💸 Tap 2 earn"), state=UserFollowing.wallet_menu)
# async def tap_to_earn(message: types.Message, state: FSMContext):
#     data = await state.get_data()
#     private_keys = list(data.get("private_keys"))
#     count_private_keys = len(private_keys)
#
#
#         # message_response = ""
#         await AdminMode.add_user.set()
#         await message.answer(message_response, reply_markup=ReplyKeyboardRemove())