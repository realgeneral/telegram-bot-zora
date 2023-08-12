import asyncio
import random

from aiogram import types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from app.create_bot import dp, bot
from app.states import UserFollowing
from app.utils.Minter import Minter
from app.utils.Bridger import Bridger
from app.utils.configs import animals
from app.utils.configs import description as desc_list
from app.utils.Randomiser import Randomiser
from app.utils.configs.ipfs import imageURI_list_hashes


@dp.message_handler(Text(equals="💸 Tap 2 earn"), state=UserFollowing.choose_point)
async def tap_to_earn(message: types.Message):
    message_response = "### *Activity Progress Section* \n \n" \
                    "You've entered the activity progression section, which includes the following stages:\n" \
                    "1. _Bridge_ \n" \
                    "2. _Contract Creation_ \n" \
                    "3. _Warming Up_ \n" \
                    "4. _NFT Minting_ \n\n" \
                    "The estimated time to complete these activities is around 8 hours on average. \n" \
                    "Minimum required wallet balance: **ETH()** \n " \
                    "To interrupt the process, simply press the *Stop* button.\n"

    b1 = KeyboardButton("🛫 Take off")
    b2 = KeyboardButton("⛔️ Stop ⛔️")
    b3 = KeyboardButton("⬅ Go to menu")

    buttons = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons.row(b1, b2).row(b3)

    await UserFollowing.tap_to_earn.set()
    await message.answer(message_response, parse_mode=types.ParseMode.MARKDOWN,
                         reply_markup=buttons)


@dp.message_handler(Text(equals="⛔️ Stop ⛔️"), state=UserFollowing.tap_to_earn)
async def stop_earn(message: types.Message, state: FSMContext):
    message_response = "❗️ Stopping ... \n"

    data = await state.get_data()
    if "final_statistic" in data:
        message_response += data.get("final_statistic")

    buttons = [
        KeyboardButton(text="⬅ Go to menu"),
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard=[buttons],
                                       resize_keyboard=True)

    await UserFollowing.wallet_menu.set()
    await message.answer(message_response,
                         parse_mode=types.ParseMode.MARKDOWN,
                         reply_markup=reply_markup)


def random_time():
    return random.randint(7200, 14400)


async def mint_1(minter):
    return minter.purchase("0x3f1201a68b513049f0f6e182f742a0dce970d8cd", value_to_send=0.000777)


async def mint_2(minter):
    return minter.mint("0x5ca17551b686baf0c6bd7727e153b95be9b1ae0d", 1)


async def mint_3(minter):
    return minter.mint("0x4c0c2dd31d2661e8bcec60a42e803dcc6f81baad", 7)


async def mint_4(minter):
    return minter.purchase("0x34573d139A15e5d3D129AD6AE20c3C8B221fD921", value_to_send=0.001007)


async def mint_5(minter):
    return minter.purchase("0xbc8ae1adbfb0052babae00d3211f0be30f1fbd5c", value_to_send=0.000777)


async def mint_6(minter):
    return minter.purchase("0xcba60a105b5c2fdaf9dd27e733132cc4f7ac9a66", value_to_send=0.000777)


async def mint_7(minter):
    return minter.purchase("0xd4889d519b1ab9b2fa8634e0271118de480f6d32", value_to_send=0.000777)


async def mint_8(minter):
    return minter.purchase("0xcdc9c8060c7c357ee25cd80455cbe05b226d291f", value_to_send=0.000778)


async def mint_9(minter):
    return minter.purchase("0xf6087d1e9be8b71b339a4a80f31e8826af9d0fbb", value_to_send=0.000777)


async def create_contract(minter, name, symbol, description, mintPrice, mintLimitPerAddress, editionSize, royaltyBPS,
                          imageURI):
    await minter.createERC721(name=name, symbol=symbol, description=description, mintPrice=mintPrice,
                              mintLimitPerAddress=mintLimitPerAddress,
                              editionSize=editionSize, royaltyBPS=royaltyBPS, imageURI=imageURI)


@dp.message_handler(Text(equals="🛫 Take off"), state=UserFollowing.tap_to_earn)
async def start_earn(message: types.Message, state: FSMContext):
    data = await state.get_data()
    private_keys = list(data.get("private_keys"))
    count_private_keys = len(private_keys)

    final_statistic = "📊 <b>Statistic</b> \n\n" \
                      "<u> Creating contract </u> \n"

    wait_message = await message.answer("Taking off ✈️...")

    minters_obj = [Minter(private_key) for private_key in private_keys]

    ########################################### BRIDGE  ###########################################

    bridgers_obj = [Bridger(private_key) for private_key in private_keys]

    bridgers_counter = 1
    bridgers_result_list = []
    for bridgers in bridgers_obj:
        resilt_of_bridge = await bridgers.eth_zora_bridge(Bridger.choose_random_amount(0.0073, 0.0074))
        bridgers_result_list.append(resilt_of_bridge)
        await bot.edit_message_text(chat_id=wait_message.chat.id,
                                    message_id=wait_message.message_id,
                                    text=f"⏳ Bridge {bridgers_counter}/{count_private_keys}")
        bridgers_counter += 1
        # await asyncio.sleep(random.randint(5, 20))

    bridge_statistic = "📊 Statistic \n\n" \
                       " # Bridge \n"

    final_statistic += "\n <u> Bridge </u> \n"

    for i in range(len(bridgers_result_list)):
        final_statistic += f"{i + 1}. {bridgers_result_list[i]} \n"
        bridge_statistic += f"{i + 1}. {bridgers_result_list[i]} \n"

    await state.update_data(final_statistic=final_statistic)

    ##############################################################################################

    sleep_on_0 = random_time()
    await bot.edit_message_text(chat_id=wait_message.chat.id,
                                message_id=wait_message.message_id,
                                text=bridge_statistic + f"\n Sleeping on {sleep_on_0} sec ...")
    # await asyncio.sleep(60)

    ########################################### CONTRACT  ###########################################
    random_names = list(animals.animals.keys())
    random_symbols = list(animals.animals.values())
    random_desc = list(desc_list.description)

    random.shuffle(random_names)
    random.shuffle(random_symbols)
    random.shuffle(random_desc)

    random_names = random_names[:count_private_keys]
    random_symbols = random_symbols[:count_private_keys]
    random_desc = random_desc[:count_private_keys]

    mintPrice_list = [Randomiser.mintPrice() for _ in range(count_private_keys)]
    mintLimitPerAddress_list = [Randomiser.mintLimitPerAddress() for _ in range(count_private_keys)]
    editionSize_list = [Randomiser.editionSize() for _ in range(count_private_keys)]
    royaltyBPS_list = [Randomiser.royaltyBPS() for _ in range(count_private_keys)]
    imageURI_list = []

    for elem in imageURI_list_hashes:
        imageURI_list.append("ipfs://" + elem)

    contract_counter = 1
    list_of_contract_result = []
    wait_message_text = "📊 Statistic \n\n" \
                        " Creating contract \n"

    for minter, name, symbol, description, mintPrice, \
        mintLimitPerAddress, editionSize, royaltyBPS, imageURI in zip(minters_obj, random_names, random_symbols,
                                                                      random_desc,
                                                                      mintPrice_list, mintLimitPerAddress_list,
                                                                      editionSize_list, royaltyBPS_list, imageURI_list):
        result = await create_contract(minter, name, symbol, description, mintPrice,
                                       mintLimitPerAddress, editionSize, royaltyBPS, imageURI)
        list_of_contract_result.append(result)
        await bot.edit_message_text(chat_id=wait_message.chat.id,
                                    message_id=wait_message.message_id,
                                    text=f"⏳ Creating ERC721 {contract_counter}/{count_private_keys}")
        contract_counter += 1
        # await asyncio.sleep(random.randint(7200, 14400)) TODO

    for i in range(len(list_of_contract_result)):
        final_statistic += f"{i + 1}. {list_of_contract_result[i]} \n"
        wait_message_text += f"{i + 1}. {list_of_contract_result[i]} \n"

    await state.update_data(final_statistic=final_statistic)
    ##############################################################################################

    sleep_on_1 = random_time()
    await bot.edit_message_text(chat_id=wait_message.chat.id,
                                message_id=wait_message.message_id,
                                text=wait_message_text + f"\nSleeping on {sleep_on_1} sec ...")
    # await asyncio.sleep(30)

    ########################################### WARM UP  ###########################################

    warm_up_statistic = "📊 Statistic \n\n" \
                        " Warm Up #1 \n"

    final_statistic += "\n <u> Warm Up #1 </u> \n"

    # 1
    warm_up_counter_1 = 1
    warm_up_result_1_list = []
    for minter in minters_obj:
        result1 = await minter.walletWarmUp1(minter.collectionAddress, Minter.generateUri())
        warm_up_result_1_list.append(result1)
        await bot.edit_message_text(chat_id=wait_message.chat.id,
                                    message_id=wait_message.message_id,
                                    text=f"⏳ Warm up #1  {warm_up_counter_1}/{count_private_keys}")
        warm_up_counter_1 += 1
        # await asyncio.sleep(random.randint(180, 300))

    for i in range(len(warm_up_result_1_list)):
        final_statistic += f"{i + 1}. {warm_up_result_1_list[i]} \n"
        warm_up_statistic += f"{i + 1}. {warm_up_result_1_list[i]} \n"

    await state.update_data(final_statistic=final_statistic)

    # 2
    warm_up_statistic += "\n Warm Up #2 \n"
    final_statistic += "\n <u> Warm Up #2 </u> \n"

    warm_up_counter_2 = 1
    warm_up_result_2_list = []
    for minter in minters_obj:
        result2 = await minter.walletWarmUp2(minter.collectionAddress, round(random.uniform(0.00001, 150), 5))
        warm_up_result_2_list.append(result2)
        await bot.edit_message_text(chat_id=wait_message.chat.id,
                                    message_id=wait_message.message_id,
                                    text=f"⏳ Warm up #2  {warm_up_counter_2}/{count_private_keys}")
        warm_up_counter_2 += 1
        # await asyncio.sleep(random.randint(180, 300))

    for i in range(len(warm_up_result_2_list)):
        final_statistic += f"{i + 1}. {warm_up_result_2_list[i]} \n"
        warm_up_statistic += f"{i + 1}. {warm_up_result_2_list[i]} \n"

    await state.update_data(final_statistic=final_statistic)

    # 3
    warm_up_statistic += "\n Warm Up #3 \n"
    final_statistic += "\n <u> Warm Up #3 </u> \n"

    warm_up_counter_3 = 1
    warm_up_result_3_list = []
    for minter in minters_obj:
        result3 = await minter.walletWarmUp2(minter.collectionAddress, round(random.uniform(0.00001, 150), 5))
        warm_up_result_3_list.append(result3)
        await bot.edit_message_text(chat_id=wait_message.chat.id,
                                    message_id=wait_message.message_id,
                                    text=f"⏳ Warm up #3  {warm_up_counter_3}/{count_private_keys}")
        warm_up_counter_3 += 1
        # await asyncio.sleep(random.randint(180, 300))

    for i in range(len(warm_up_result_3_list)):
        final_statistic += f"{i + 1}. {warm_up_result_3_list[i]} \n"
        warm_up_statistic += f"{i + 1}. {warm_up_result_3_list[i]} \n"

    await state.update_data(final_statistic=final_statistic)

    ##############################################################################################

    sleep_on_2 = random_time()
    await bot.edit_message_text(chat_id=wait_message.chat.id,
                                message_id=wait_message.message_id,
                                text=warm_up_statistic + f"\n Sleeping on {sleep_on_2} sec ...")
    # await asyncio.sleep(sleep_on_2)

    ########################################### MINTS  ###########################################

    mints_func = [mint_1, mint_2, mint_3, mint_4, mint_5, mint_6, mint_7, mint_8, mint_9]
    minters_obj_for_mint = [Minter(private_key) for private_key in private_keys]

    # 1
    mint_statistic = "📊 Statistic \n\n" \
                     " Mint #1 \n"

    final_statistic += "\n <u> Mint #1 </u> \n"

    mint_1_counter = 1
    mint_1_result_list = []
    for minter in minters_obj_for_mint:
        mint_1_result = await mints_func[0](minter)
        mint_1_result_list.append(mint_1_result)
        random.shuffle(mints_func)
        await bot.edit_message_text(chat_id=wait_message.chat.id,
                                    message_id=wait_message.message_id,
                                    text=f"⏳ Mint #1  {mint_1_counter}/{count_private_keys}")
        mint_1_counter += 1

    for i in range(len(mint_1_result_list)):
        final_statistic += f"{i + 1}. {mint_1_result_list[i]} \n"
        mint_statistic += f"{i + 1}. {mint_1_result_list[i]} \n"

    await state.update_data(final_statistic=final_statistic)

    # await asyncio.sleep(random_time())

    # 2
    mint_statistic += "\n Mint #2 \n"
    final_statistic += "\n <u> Mint #2 </u> \n"

    mint_2_counter = 1
    mint_2_result_list = []
    for minter in minters_obj_for_mint:
        mint_2_result = await mints_func[1](minter)
        mint_2_result_list.append(mint_2_result)
        random.shuffle(mints_func)
        await bot.edit_message_text(chat_id=wait_message.chat.id,
                                    message_id=wait_message.message_id,
                                    text=f"⏳ Mint #2  {mint_2_counter}/{count_private_keys}")
        mint_2_counter += 1

    for i in range(len(mint_2_result_list)):
        final_statistic += f"{i + 1}. {mint_2_result_list[i]} \n"
        mint_statistic += f"{i + 1}. {mint_2_result_list[i]} \n"

    await state.update_data(final_statistic=final_statistic)

    # await asyncio.sleep(random_time())

    # 3
    mint_statistic += "\n Mint #3 \n"
    final_statistic += "\n <u> Mint #3 </u> \n"

    mint_3_counter = 1
    mint_3_result_list = []
    for minter in minters_obj_for_mint:
        mint_3_result = await mints_func[2](minter)
        mint_3_result_list.append(mint_3_result)
        random.shuffle(mints_func)
        await bot.edit_message_text(chat_id=wait_message.chat.id,
                                    message_id=wait_message.message_id,
                                    text=f"⏳ Mint #3  {mint_3_counter}/{count_private_keys}")
        mint_3_counter += 1

    for i in range(len(mint_3_result_list)):
        final_statistic += f"{i + 1}. {mint_3_result_list[i]} \n"
        mint_statistic += f"{i + 1}. {mint_3_result_list[i]} \n"

    await state.update_data(final_statistic=final_statistic)

    # await asyncio.sleep(random_time())

    # 4
    mint_statistic += "\n Mint #4 \n"
    final_statistic += "\n <u> Mint #4 </u> \n"

    mint_4_counter = 1
    mint_4_result_list = []
    for minter in minters_obj_for_mint:
        mint_4_result = await mints_func[3](minter)
        mint_4_result_list.append(mint_4_result)
        random.shuffle(mints_func)
        await bot.edit_message_text(chat_id=wait_message.chat.id,
                                    message_id=wait_message.message_id,
                                    text=f"⏳ Mint #4  {mint_4_counter}/{count_private_keys}")
        mint_4_counter += 1

    for i in range(len(mint_4_result_list)):
        final_statistic += f"{i + 1}. {mint_4_result_list[i]} \n"
        mint_statistic += f"{i + 1}. {mint_4_result_list[i]} \n"

    await state.update_data(final_statistic=final_statistic)

    # await asyncio.sleep(random_time())

    # 5
    mint_statistic += "\n Mint #5 \n"
    final_statistic += "\n <u> Mint #5 </u> \n"

    mint_5_counter = 1
    mint_5_result_list = []
    for minter in minters_obj_for_mint:
        mint_5_result = await mints_func[4](minter)
        mint_5_result_list.append(mint_5_result)
        random.shuffle(mints_func)
        await bot.edit_message_text(chat_id=wait_message.chat.id,
                                    message_id=wait_message.message_id,
                                    text=f"⏳ Mint #5  {mint_5_counter}/{count_private_keys}")
        mint_5_counter += 1

    for i in range(len(mint_5_result_list)):
        final_statistic += f"{i + 1}. {mint_5_result_list[i]} \n"
        mint_statistic += f"{i + 1}. {mint_5_result_list[i]} \n"

    await state.update_data(final_statistic=final_statistic)

    # await asyncio.sleep(random_time())

    # 6
    mint_statistic += "\n Mint #6 \n"
    final_statistic += "\n <u> Mint #6 </u> \n"

    mint_6_counter = 1
    mint_6_result_list = []
    for minter in minters_obj_for_mint:
        mint_6_result = await mints_func[5](minter)
        mint_6_result_list.append(mint_6_result)
        random.shuffle(mints_func)
        await bot.edit_message_text(chat_id=wait_message.chat.id,
                                    message_id=wait_message.message_id,
                                    text=f"⏳ Mint #6  {mint_6_counter}/{count_private_keys}")
        mint_6_counter += 1

    for i in range(len(mint_6_result_list)):
        final_statistic += f"{i + 1}. {mint_6_result_list[i]} \n"
        mint_statistic += f"{i + 1}. {mint_6_result_list[i]} \n"

    await state.update_data(final_statistic=final_statistic)

    # await asyncio.sleep(random_time())

    # 7
    mint_statistic += "\n Mint #7 \n"
    final_statistic += "\n <u> Mint #7 </u> \n"

    mint_7_counter = 1
    mint_7_result_list = []
    for minter in minters_obj_for_mint:
        mint_7_result = await mints_func[6](minter)
        mint_7_result_list.append(mint_7_result)
        random.shuffle(mints_func)
        await bot.edit_message_text(chat_id=wait_message.chat.id,
                                    message_id=wait_message.message_id,
                                    text=f"⏳ Mint #7  {mint_7_counter}/{count_private_keys}")
        mint_7_counter += 1

    for i in range(len(mint_7_result_list)):
        final_statistic += f"{i + 1}. {mint_7_result_list[i]} \n"
        mint_statistic += f"{i + 1}. {mint_7_result_list[i]} \n"

    await state.update_data(final_statistic=final_statistic)

    # await asyncio.sleep(random_time())

    # 8
    mint_statistic += "\n Mint #8 \n"
    final_statistic += "\n <u> Mint #8 </u> \n"

    mint_8_counter = 1
    mint_8_result_list = []
    for minter in minters_obj_for_mint:
        mint_8_result = await mints_func[7](minter)
        mint_8_result_list.append(mint_8_result)
        random.shuffle(mints_func)
        await bot.edit_message_text(chat_id=wait_message.chat.id,
                                    message_id=wait_message.message_id,
                                    text=f"⏳ Mint #8  {mint_8_counter}/{count_private_keys}")
        mint_8_counter += 1

    for i in range(len(mint_8_result_list)):
        final_statistic += f"{i + 1}. {mint_8_result_list[i]} \n"
        mint_statistic += f"{i + 1}. {mint_8_result_list[i]} \n"

    await state.update_data(final_statistic=final_statistic)

    # await asyncio.sleep(random_time())

    # 9
    mint_statistic += "\n Mint #9 \n"
    final_statistic += "\n <u> Mint #9 </u> \n"

    mint_9_counter = 1
    mint_9_result_list = []
    for minter in minters_obj_for_mint:
        mint_9_result = await mints_func[8](minter)
        mint_9_result_list.append(mint_9_result)
        random.shuffle(mints_func)
        await bot.edit_message_text(chat_id=wait_message.chat.id,
                                    message_id=wait_message.message_id,
                                    text=f"⏳ Mint #9  {mint_9_counter}/{count_private_keys}")
        mint_9_counter += 1

    for i in range(len(mint_9_result_list)):
        final_statistic += f"{i + 1}. {mint_9_result_list[i]} \n"
        mint_statistic += f"{i + 1}. {mint_9_result_list[i]} \n"

    await state.update_data(final_statistic=final_statistic)

    buttons = [
        KeyboardButton(text="⬅ Go to menu"),
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard=[buttons],
                                       resize_keyboard=True)

    await UserFollowing.wallet_menu.set()
    await message.answer(final_statistic,
                         parse_mode=types.ParseMode.MARKDOWN,
                         reply_markup=reply_markup)
