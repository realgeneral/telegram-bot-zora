from aiogram import types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from app.create_bot import dp, bot
from app.states import UserFollowing


@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    buttons = [
        KeyboardButton(text="🚀 Start"),
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard=[buttons], resize_keyboard=True)

    await UserFollowing.start_navigation.set()
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


@dp.message_handler(Text(equals="🚀 Start"), state=UserFollowing.start_navigation)
async def request_private_key(message: types.Message):
    await UserFollowing.get_private_keys.set()
    await message.answer("👝 *Submit your private key* \n\n"
                         "_The bot doesn't collect or store your personal data or private keys. "
                         "Zora bot — fully open source project. \n "
                         "GitHub: https://github.com/realgeneral/telegram-bot-zora_",
                         parse_mode=types.ParseMode.MARKDOWN,
                         reply_markup=ReplyKeyboardRemove())


@dp.message_handler(state=UserFollowing.get_private_keys)
async def private_keys(message: types.Message, state: FSMContext):
    api_key = message.text.strip()
    await state.update_data(api_key=api_key)

    buttons = [
        KeyboardButton(text="⬅ Go to menu"),
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard=[buttons],
                                       resize_keyboard=True)

    await UserFollowing.wallet_menu.set()
    await message.answer("😌 *Keys saved successfully*",
                         parse_mode=types.ParseMode.MARKDOWN,
                         reply_markup=reply_markup)



