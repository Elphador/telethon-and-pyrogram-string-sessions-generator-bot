from telethon import TelegramClient
from asyncio.exceptions import TimeoutError
from telethon.sessions import StringSession
from telethon.errors import (
    ApiIdInvalidError,
    PhoneNumberInvalidError,
    PhoneCodeInvalidError,
    PhoneCodeExpiredError,
    SessionPasswordNeededError,
    PasswordHashInvalidError
)
import asyncio,os
from bot import bot
from pyroaddon import listen
from asyncio.exceptions import TimeoutError
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import (
    SessionPasswordNeeded, FloodWait,
    PhoneNumberInvalid, ApiIdInvalid,
    PhoneCodeInvalid, PhoneCodeExpired
)

API_TEXT = """Hi, {}.
This is Pyrogram and telethon  String Session Generator Bot. I will generate String Session of your Telegram Account.

By @Neuralp

Now send your `API_ID`."""
HASH_TEXT = "Now send your `API_HASH`.\n\nPress /cancel to Cancel Task."
PHONE_NUMBER_TEXT = (
    "Now send your Telegram account's Phone number in International Format. \n"
    "Including Country code. Example: **+14154566376**\n\n"
    "Press /cancel to Cancel Task."
)
@bot.on_message(filters.private & filters.command('telethon'))
async def tele(c,m):
    chat = m.chat
    api = await bot.ask(
        chat.id, API_TEXT.format(m.from_user.mention)
    )
    if await is_cancel(m, api.text):
        return
    try:
        check_api = int(api.text)
    except Exception:
        await m.reply("`API_ID` is Invalid.\nPress /start to Start again.")
        return
    api_id = api.text
    hash = await bot.ask(chat.id, HASH_TEXT)
    if await is_cancel(m, hash.text):
        return
    if not len(hash.text) >= 30:
        await m.reply("`API_HASH` is Invalid.\nPress /start to Start again.")
        return
    api_hash = hash.text
    while True:
        number = await bot.ask(chat.id, PHONE_NUMBER_TEXT)
        if not number.text:
            continue
        if await is_cancel(m, number.text):
            return
        phone = number.text
        confirm = await bot.ask(chat.id, f'`Is "{phone}" correct? (y/n):` \n\nSend: `y` (If Yes)\nSend: `n` (If No)')
        if await is_cancel(m, confirm.text):
            return
        if "y" in confirm.text:
            break
    try :
        client = TelegramClient(StringSession(), api_id, api_hash)
        await client.connect()
    except Exception as e:
        await m.reply(e)
    try :
        code = await client.send_code_request(phone)
    except (ApiIdInvalid, ApiIdInvalidError):
        await m.reply('`API_ID` and `API_HASH` combination is invalid. Please start generating session again.')
        return
    except (PhoneNumberInvalid, PhoneNumberInvalidError):
        await m.reply('`PHONE_NUMBER` is invalid. Please start generating session again.')
        return
    try:
        code= await bot.ask(chat.id, "Please check for an OTP in official telegram account. If you got it, send OTP here after reading the below format. \nIf OTP is `12345`, **please send it as** `1 2 3 4 5`.", filters=filters.text, timeout=600)
    except TimeoutError:
        await m.reply('Time limit reached of 10 minutes. Please start generating session again.')
        return
    try :
        code = code.text 
        code = ' '.join(str(code))
        await client.sign_in(phone, code, password=None)
    except (PhoneCodeInvalid, PhoneCodeInvalidError):
        await m.reply('OTP is invalid. Please start generating session again.')
        return
    except (PhoneCodeExpired, PhoneCodeExpiredError):
        await m.reply('OTP is expired. Please start generating session again.')
        return
    except (SessionPasswordNeeded, SessionPasswordNeededError): 
        try:
            two_step= await bot.ask(chat.id, 'Your account has enabled two-step verification. Please provide the password.', filters=filters.text, timeout=300)
        except TimeoutError:
            await m.reply('Time limit reached of 5 minutes. Please start generating session again.')
            return
        try:
            password = two_step.text
            await client.sign_in(password=password)
        except (PasswordHashInvalid, PasswordHashInvalidError):
            await m.reply('Invalid Password Provided. Please start generating session again.', quote=True)
            return
    string_session = client.session.save()
    await m.reply(f'copy it `{string_session}`')
            

@bot.on_message(filters.private & filters.command("pyrogram"))
async def genStr(_, msg: Message):
    chat = msg.chat
    api = await bot.ask(
        chat.id, API_TEXT.format(msg.from_user.mention)
    )
    if await is_cancel(msg, api.text):
        return
    try:
        check_api = int(api.text)
    except Exception:
        await msg.reply("`API_ID` is Invalid.\nPress /start to Start again.")
        return
    api_id = api.text
    hash = await bot.ask(chat.id, HASH_TEXT)
    if await is_cancel(msg, hash.text):
        return
    if not len(hash.text) >= 30:
        await msg.reply("`API_HASH` is Invalid.\nPress /start to Start again.")
        return
    api_hash = hash.text
    while True:
        number = await bot.ask(chat.id, PHONE_NUMBER_TEXT)
        if not number.text:
            continue
        if await is_cancel(msg, number.text):
            return
        phone = number.text
        confirm = await bot.ask(chat.id, f'`Is "{phone}" correct? (y/n):` \n\nSend: `y` (If Yes)\nSend: `n` (If No)')
        if await is_cancel(msg, confirm.text):
            return
        if "y" in confirm.text:
            break
    try:
        client = Client("my_account", api_id=api_id, api_hash=api_hash)
    except Exception as e:
        await bot.send_message(chat.id ,f"**ERROR:** `{str(e)}`\nPress /start to Start again.")
        return
    try:
        await client.connect()
    except ConnectionError:
        await client.disconnect()
        await client.connect()
    try:
        code = await client.send_code(phone)
        await asyncio.sleep(1)
    except FloodWait as e:
        await msg.reply(f"You have Floodwait of {e.x} Seconds")
        return
    except ApiIdInvalid:
        await msg.reply("API ID and API Hash are Invalid.\n\nPress /start to Start again.")
        return
    except PhoneNumberInvalid:
        await msg.reply("Your Phone Number is Invalid.\n\nPress /start to Start again.")
        return
    try:
        otp = await bot.ask(
            chat.id, ("An OTP is sent to your phone number, "
                      "Please enter OTP in `1 2 3 4 5` format. __(Space between each numbers!)__ \n\n"
                      "If Bot not sending OTP then try /restart and Start Task again with /start command to Bot.\n"
                      "Press /cancel to Cancel."), timeout=300)

    except TimeoutError:
        await msg.reply("Time limit reached of 5 min.\nPress /start to Start again.")
        return
    if await is_cancel(msg, otp.text):
        return
    otp_code = otp.text
    try:
        await client.sign_in(phone, code.phone_code_hash, phone_code=' '.join(str(otp_code)))
    except PhoneCodeInvalid:
        await msg.reply("Invalid Code.\n\nPress /start to Start again.")
        return
    except PhoneCodeExpired:
        await msg.reply("Code is Expired.\n\nPress /start to Start again.")
        return
    except SessionPasswordNeeded:
        try:
            two_step_code = await bot.ask(
                chat.id, 
                "Your account have Two-Step Verification.\nPlease enter your Password.\n\nPress /cancel to Cancel.",
                timeout=300
            )
        except TimeoutError:
            await msg.reply("`Time limit reached of 5 min.\n\nPress /start to Start again.`")
            return
        if await is_cancel(msg, two_step_code.text):
            return
        new_code = two_step_code.text
        try:
            await client.check_password(new_code)
        except Exception as e:
            await msg.reply(f"**ERROR:** `{str(e)}`")
            return
    except Exception as e:
        await bot.send_message(chat.id ,f"**ERROR:** `{str(e)}`")
        return
    try:
        session_string = await client.export_session_string()
        await msg.reply(f'click to copy `{str(session_string)}`')
        await client.disconnect()
        os.remove("my_account.session")
    except Exception as e:
        await bot.send_message(chat.id ,f"**ERROR:** `{str(e)}`")
        os.remove("my_account.session")
        return


@bot.on_message(filters.private & filters.command("start") | filters.text)
async def restart(_, msg: Message):
    out = f"""
Hi, {msg.from_user.mention}. This is Pyrogram and telethon  Session String Generator Bot. \
use /pyrogram for pyrogram session use /telethon for telethon session
It needs `API_ID`, `API_HASH`, Phone Number and One Time Verification Code. \
Which will be sent to your Phone Number.
You have to put **OTP** in `1 2 3 4 5` this format. __(Space between each numbers!)__

Must Join Channel for Bot Updates !!
"""
    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton('Support Group', url='https://t.me/neuralg'),
                InlineKeyboardButton('Developer', url='https://t.me/botfather')
            ],
            [
                InlineKeyboardButton('Bots Updates Channel', url='https://t.me/neuralp'),
            ]
        ]
    )
    await msg.reply(out, reply_markup=reply_markup)


async def is_cancel(msg: Message, text: str):
    if text.startswith("/cancel"):
        await msg.reply("Process Cancelled.")
        return True
    return False

if __name__ == "__main__":
    bot.run()
