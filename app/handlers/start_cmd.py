from aiogram import types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from app.create_bot import dp, bot
from app.states import UserFollowing
from app.keyboards import check_sub_menu
from app.handlers import admin
from app.utils.Bridger import Bridger

CHANNEL_ID = -1001984019900
NOTSUB_MESSAGE = "Looks like you're not subscribed yet! 🙁 Subscribe now to access all the features"


@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    buttons = [
        KeyboardButton(text="🤿 Alright, let's dive in!"),
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard=[buttons], resize_keyboard=True)

    await UserFollowing.check_subscribe.set()
    await message.answer(f"Hey there, <b> {message.from_user.first_name} </b>, right place, right time! \n \n"
                         "Our Zora Bot benefits:\n \n"
                         "  • 🌐 Open source \n \n"
                         "  • 🆓 It's free \n \n"
                         "  • 😃 User-friendly \n \n"
                         "  • 🕔 Save your time \n \n"
                         "  • 💼 Do all important tasks  \n \n"
                         "  • 🔒 Has Anti-Sybil mode \n",
                         parse_mode=types.ParseMode.HTML,
                         reply_markup=reply_markup)


def check_sub_channel(chat_member):
    if chat_member["status"] != "left":
        return True
    return False


@dp.message_handler(Text(equals="🤿 Alright, let's dive in!"), state=UserFollowing.check_subscribe)
async def check_subscribe(message: types.Message):
    await UserFollowing.check_subscribe.set()
    await message.answer(
        "👋📢 Whoa, hold up! Haven't joined our <a href='https://t.me/trioinweb3'>channel</a> yet? \n\n"
        "We're dropping <b> crypto wisdom </b> and sharing our <b> know-how </b>. \n"
        "Your sub supports us to make <b> new retro-bots </b> for You! \n \n"
        "Hit that sub button below ⬇️, then <b> hit us back </b> with  <b> 'Done'</b>! ",
        parse_mode=types.ParseMode.HTML,
        reply_markup=check_sub_menu)


@dp.callback_query_handler(text="is_subscribe", state=UserFollowing.check_subscribe)
async def is_subscribe(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
    if check_sub_channel(await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=callback_query.from_user.id)):
        await UserFollowing.get_private_keys.set()
        await bot.send_message(callback_query.from_user.id, "<b> Load-up your private keys below ⬇️ </b>\n\n"
                                                            "<b>One line one wallet (press shift+enter to switch to "
                                                            "a new line)</b> \n\n"
                                                            "<a href='https://support.metamask.io/hc/en-us/articles/360015289632-How-to-export-an-account-s-private-key'>"
                                                            "<b>How to get private keys from the wallet guide</b></a>\n\n"
                                                            "<b>Example:</b>\n"
                                                            "0x0430000000000000000000000000000 \n"
                                                            "0x4349593453490203003050435043534 \n\n"
                                                            "<i><b> Free version  </b> </i>: up to 10 keys.\n"
                                                            "<i><b> Premium version </b> </i>: up to 50 keys. \n"
                                                            "<i> For access to the premium version, please "
                                                            "<a href='https://t.me/whatheshark'>contact us</a> </i> \n\n"
                                                            "<i><u>The bot doesn't collect or store your personal data or"
                                                            "private keys. Zora bot — fully open source project.</u> \n\n "
                                                            "GitHub: https://github.com/zemetsskiy/ZoraAutomatization "
                                                            "</i>",
                               parse_mode=types.ParseMode.HTML,
                               reply_markup=ReplyKeyboardRemove())
    else:
        await bot.send_message(callback_query.from_user.id, NOTSUB_MESSAGE, reply_markup=check_sub_menu)


@dp.message_handler(state=UserFollowing.get_private_keys)
async def private_keys(message: types.Message, state: FSMContext):
    random_amount = []

    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

    if int(message.from_user.id) in admin.list_of_prem_users:
        private_keys = message.text.split('\n')[:50]
        for _ in private_keys:
            random_amount.append(Bridger.choose_random_amount(0.009501, 0.01003))

        message_response = "😌 *Keys saved successfully (max. 50) *"
    else:
        private_keys = message.text.split('\n')[:10]
        for _ in private_keys:
            random_amount.append(Bridger.choose_random_amount(0.009501, 0.01003))

        message_response = "😌 *Keys saved successfully (max. 10) *"

    await state.update_data(private_keys=private_keys)
    await state.update_data(random_amount=random_amount)

    buttons = [
        KeyboardButton(text="⬅ Go to menu"),
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard=[buttons],
                                       resize_keyboard=True)

    await UserFollowing.wallet_menu.set(),
    await message.answer(message_response,
                         parse_mode=types.ParseMode.MARKDOWN,
                         reply_markup=reply_markup)
