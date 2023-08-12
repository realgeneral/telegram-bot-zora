from aiogram import types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from app.create_bot import dp, bot
from app.states import UserFollowing


@dp.message_handler(Text(equals=["👝 Check balance"]), state=UserFollowing.choose_point)
async def check_wallet_keys(message: types.Message, state: FSMContext):
    url_eth = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"

    data = await state.get_data()
    private_key = data.get("private_key")

    wait_1_message = await message.answer("⏳ Getting information about wallets ...")

    await bot.edit_message_text(chat_id=wait_1_message.chat.id,
                                message_id=wait_1_message.message_id,
                                text="⏳ Получаю информацию о кошельке 25%")

    buttons = [
        KeyboardButton(text="⬅ Go to menu"),
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard=[buttons],
                                       resize_keyboard=True)

    await bot.delete_message(chat_id=wait_1_message.chat.id,
                             message_id=wait_1_message.message_id)
    await UserFollowing.choose_point.set()
    await message.answer(f" 📊 <b> Баланс </b> \n\n"
                         f"<u>BNB</u>  = {}\n"
                         f"<u>MATIC</u> = {}\n"
                         f"<u>Core</u> = {}\n"
                         f"<u>Celo</u> = {}\n", parse_mode=types.ParseMode.HTML,
                         reply_markup=reply_markup)
