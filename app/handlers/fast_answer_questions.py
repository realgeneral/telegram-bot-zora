import asyncio

import httpx

from aiogram import types
from aiogram.dispatcher.filters import Text

from app.create_bot import dp, bot
from app.states import UserFollowing
from app.keyboards import faq_buttons


@dp.message_handler(Text(equals=["ℹ️ FAQ"]), state=UserFollowing.choose_point)
async def faq_handler(message: types.Message):
    reply_message = "ℹ️ FAQ"

    await UserFollowing.choose_point.set()
    await message.answer(reply_message, parse_mode=types.ParseMode.MARKDOWN,
                         reply_markup=faq_buttons)


@dp.message_handler(Text(equals=["🧐 What can bot do?"]), state=UserFollowing.choose_point)
async def what_can_bot_do(message: types.Message):
    reply_message = "*Bot's superpowers: * \n \n" \
                    "• 📩 Bridge to Zora Mainnet from ETH Mainnet \n\n" \
                    "• 🀄️ Create NFTs  \n\n" \
                    "• 🖼 Mint important NFTs (updated list)  \n\n" \
                    "• 🏋️‍♂️ Wallet warm-up (simulation of real human actions)  \n\n" \
                    "• ⛽️ GWEI downgrade mode - literally lowers the fees to zero \n\n"

    await UserFollowing.choose_point.set()
    await message.answer(reply_message, parse_mode=types.ParseMode.MARKDOWN,
                         reply_markup=faq_buttons)


@dp.message_handler(Text(equals=["⛽️ What is GWEI ?"]), state=UserFollowing.choose_point)
async def what_can_bot_do(message: types.Message):
    reply_message = "*What is GWEI?* \n\n" \
                    '*GWEI* -  is a unit of payment for "*gas*", which is the fee required to make transactions or ' \
                    " ⛽️ Gas in Ethereum can be like the fuel for a car. \n\n" \
                    '🚘 Just as a *car* needs fuel to run, transactions and smart contracts in Ethereum require "*gas*" to operate.   \n\n' \
                    '⛽️ *GWEI* is similar to the quantification of fuel in liters or gallons - it\'s a unit of measurement for "*gas*".   \n\n' \
                    "💸 The higher the *GWEI*, the higher the *transaction fee*.  \n\n" \
                    "🔎 *To check the current GWEI tap on «⛽️Check GWEI» button in the main menu.* \n\n"

    await UserFollowing.choose_point.set()
    await message.answer(reply_message, parse_mode=types.ParseMode.MARKDOWN,
                         reply_markup=faq_buttons)


@dp.message_handler(Text(equals=["💎 Premium version"]), state=UserFollowing.choose_point)
async def premium_version(message: types.Message):
    reply_message = "<b>Premium version</b>\n\n" \
                    "To set-up more wallets in the bot, you need to become a premium memeber.  \n\n" \
                    "<i>- The ability to load up to 50 wallets into the bot </i>\n" \
                    "<i>- Be among the first to get access to our latest developments</i>\n"\
                    "<i>- Your tasks bot will perform in high priority </i>\n" \
                    "<i>- You will give us the motivation to make the software even better for you</i>\n\n" \
                    "<b> <a href='https://t.me/whatheshark'>DM</a> for price</b>\n"

    await UserFollowing.choose_point.set()
    await message.answer(reply_message, parse_mode=types.ParseMode.HTML,
                         reply_markup=faq_buttons)


@dp.message_handler(Text(equals=["🗺 How to get started?"]), state=UserFollowing.choose_point)
async def premium_version(message: types.Message):
    reply_message = "<b> How the hell do I get started? </b>\n\n" \
                    '1. Upload your private keys in the "➕ <b> New keys </b>" tab\n' \
                    ' <a href="https://support.metamask.io/hc/en-us/articles/360015289632-How-to-export-an-account-s-private-key">How to get private keys from the wallet guide</a> )\n\n' \
                    '2. Click on the "👝 <b> Check Balance </b>" button. Based on the GWEI values, we will select the exact deposit amount to make all Zora activities.\n\n' \
                    '3. Send the quoted ETH from your CEX to your wallet in Ethereum Mainnet Chain\n ' \
                    '( ❗️be sure to send it with <b> CEX </b> )\n\n' \
                    '4. Be bullish and click on the "💸 <b> 💸 Start script </b>" button in the main menu\n\n' \
                    '5. Follow the instructions you will receive from the Bot'

    await UserFollowing.choose_point.set()
    await message.answer(reply_message, parse_mode=types.ParseMode.HTML,
                         reply_markup=faq_buttons)