from aiogram import types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from app.create_bot import dp, bot
from app.states import UserFollowing
from app.keyboards import check_sub_menu
from app.handlers import admin

CHANNEL_ID = -1001984019900
NOTSUB_MESSAGE = "Looks like you're not subscribed yet! 🙁 Subscribe now to access all the features"


@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    buttons = [
        KeyboardButton(text="🚀 Start"),
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard=[buttons], resize_keyboard=True)

    await UserFollowing.check_subscribe.set()
    await message.answer("Welcome to the <b>Zora Automatization</b> bot! 🤖👋 \n\n"
                         # "📍 Рекомендую ознакомиться с <a href='https://t.me/trioinweb3/13'>гайдом</a> 📍\n\n"
                         "The bot execute:\n",
                         # "<u> 1. Минт nft: </u> \n"
                         # "  🔘 <i> Greenfield Testnet </i> (на BNB Chain) \n"
                         # "  🔘 <i> ZkLightClient </i> (на BNB Chain) \n"
                         # "  🔘 <i> ZkBridge on opBNB </i> (на BNB Chain) \n"
                         # "  🔘 <i> Mainnet Alpha </i> (на Core) \n"
                         # "  🔘 <i> Pandra </i> (на BNB Chain, Polygon, Core, Celo) \n\n"
                         # "<u> 2. Кроссчейн nft сендер (zknft): </u> \n"
                         # '  🔘 <i> ZkLightClient nft </i> из BSC в opBNB \n'
                         # '  🔘 <i> ZkBridge on opBNB nft </i> из BSC в opBNB \n'
                         # '  🔘 <i> Mainnet Alpha nft </i> из Core в Polygon \n'
                         # '  🔘 <i> CodeConqueror (Pandra) nft </i> из BSC в Core \n'
                         # '  🔘 <i> PixelProwler (Pandra) nft </i> из Polygon в BSC \n'
                         # '  🔘 <i> MelodyMaven (Pandra) nft </i> из Core в Polygon \n'
                         # '  🔘 <i> EcoGuardian (Pandra) nft </i> из Celo в BSC \n\n'
                         # '<u> 3. Отправка сообщений (zkMessenger): </u> \n'
                         # '  🔘 <i> из BSC в Polygon </i> \n\n'
                         # ''
                         # '<u>Необходимое количество токенов для оплаты газа </u> \n'
                         # ' BNB = <i>0.02065</i> \n'
                         # ' Matic = <i>3.1</i> \n'
                         # ' Core = <i>2.5</i> \n'
                         # ' Celo = <i>5</i>',
                         parse_mode=types.ParseMode.HTML,
                         reply_markup=reply_markup)


def check_sub_channel(chat_member):
    if chat_member["status"] != "left":
        return True
    return False


@dp.message_handler(Text(equals="🚀 Start"), state=UserFollowing.check_subscribe)
async def check_subscribe(message: types.Message):

    await UserFollowing.check_subscribe.set()
    await message.answer("👋📢 To enjoy the full features of our bot, kindly subscribe to our "
                         "<a href='https://t.me/trioinweb3'>channel</a> first",
                         parse_mode=types.ParseMode.HTML,
                         reply_markup=check_sub_menu)


@dp.callback_query_handler(text="is_subscribe", state=UserFollowing.check_subscribe)
async def is_subscribe(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
    if check_sub_channel(await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=callback_query.from_user.id)):
        await UserFollowing.get_private_keys.set()
        await bot.send_message(callback_query.from_user.id, "👝 *Submit your private key's* \n\n"
                                                            "_Free version_: up to 10 keys.\n "
                                                            "_Premium version_: up to 50 keys. \n"
                                                            "For access to the premium version, please contact us. \n\n"
                                                            "_The bot doesn't collect or store your personal data or "
                                                            "private keys. "
                                                            "Zora bot — fully open source project. \n\n "
                                                            "GitHub: https://github.com/realgeneral/telegram-bot-zora_",
                               parse_mode=types.ParseMode.MARKDOWN,
                               reply_markup=ReplyKeyboardRemove())
    else:
        await bot.send_message(callback_query.from_user.id, NOTSUB_MESSAGE, reply_markup=check_sub_menu)


@dp.message_handler(state=UserFollowing.get_private_keys)
async def private_keys(message: types.Message, state: FSMContext):
    if int(message.from_user.id) in admin.list_of_prem_users:
        private_keys = message.text.split('\n')[:50]
        message_response = "😌 *Keys saved successfully (max. 50) *"
    else:
        private_keys = message.text.split('\n')[:10]
        message_response = "😌 *Keys saved successfully (max. 10) *"
    await state.update_data(private_keys=private_keys)

    buttons = [
        KeyboardButton(text="⬅ Go to menu"),
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard=[buttons],
                                       resize_keyboard=True)

    await UserFollowing.wallet_menu.set(),
    await message.answer(message_response,
                         parse_mode=types.ParseMode.MARKDOWN,
                         reply_markup=reply_markup)
