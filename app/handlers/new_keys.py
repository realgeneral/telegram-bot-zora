from aiogram import types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from app.create_bot import dp, bot
from app.states import UserFollowing
from app.handlers import admin
from app.utils.Bridger import Bridger


@dp.message_handler(Text(equals=["🆕 New keys"]), state=UserFollowing.choose_point)
async def new_private_keys(message: types.Message):
    await UserFollowing.new_private.set()
    await message.answer("👝 *Submit your private key's* \n\n"
                         "_Free version_: up to 10 keys.\n "
                         "_Premium version_: up to 50 keys. \n"
                         "For access to the premium version, please contact us. \n\n"
                         "_The bot doesn't collect or store your personal data or "
                         "private keys. "
                         "Zora bot — fully open source project. \n\n "
                         "GitHub: https://github.com/realgeneral/telegram-bot-zora_",
                         parse_mode=types.ParseMode.MARKDOWN,
                         reply_markup=ReplyKeyboardRemove())


@dp.message_handler(state=UserFollowing.new_private)
async def get_new_private_keys(message: types.Message, state: FSMContext):
    wait_message = await message.answer("⏳ Getting private keys...", reply_markup=ReplyKeyboardRemove())

    random_amount = []

    if int(message.from_user.id) in admin.list_of_prem_users:
        private_keys = message.text.split('\n')[:50]
        message_response = "😌 *Keys saved successfully (max. 50) *"

        for _ in private_keys:
            random_amount.append(Bridger.choose_random_amount(0.009501, 0.01003))
    else:
        private_keys = message.text.split('\n')[:10]
        message_response = "😌 *Keys saved successfully (max. 10) *"

        for _ in private_keys:
            random_amount.append(Bridger.choose_random_amount(0.009501, 0.01003))

    await state.update_data(private_keys=private_keys)
    await state.update_data(random_amount=random_amount)

    await bot.delete_message(chat_id=wait_message.chat.id,
                             message_id=wait_message.message_id)
    buttons = [
        KeyboardButton(text="⬅ Go to menu"),
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard=[buttons],
                                       resize_keyboard=True)

    await UserFollowing.wallet_menu.set()
    await message.answer(message_response,
                         parse_mode=types.ParseMode.MARKDOWN,
                         reply_markup=reply_markup)
