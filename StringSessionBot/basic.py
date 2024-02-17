from Data import Data
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, Message


def filter(cmd: str):
    return filters.private & filters.incoming & filters.command(cmd)


# Start Message
@Client.on_message(filter("start"))
async def start(bot: Client, msg: Message):
    user = await bot.get_me()
    mention = user.mention
    await bot.send_message(
        msg.chat.id,
        text="**شكراً لخوض التجربة مع سورس ديثون ❤️**",
    )
    await asyncio.sleep(2)
    
    await bot.send_message(
        msg.chat.id,
        text="**عيش التجربة مع سورس ديثون من حيث**",
    )
    await asyncio.sleep(2)

    await bot.send_message(
        msg.chat.id,
        text="**السرعة**",
    )
    await asyncio.sleep(2)
    await bot.send_message(
        msg.chat.id,
        text="**والسلاسة**",
    )
    await asyncio.sleep(2)
    await bot.send_message(
        msg.chat.id,
        text="**والمميزات الحصرية 😍**",
    )
    await asyncio.sleep(3)
    await bot.send_message(
        msg.chat.id,
        Data.START.format(msg.from_user.mention, mention),
        reply_markup=InlineKeyboardMarkup(Data.buttons),
    )


# Help Message
@Client.on_message(filter("help"))
async def _help(bot: Client, msg: Message):
    await bot.send_message(
        msg.chat.id, Data.HELP, reply_markup=InlineKeyboardMarkup(Data.home_buttons)
    )


# About Message
@Client.on_message(filter("about"))
async def about(bot: Client, msg: Message):
    await bot.send_message(
        msg.chat.id,
        Data.ABOUT,
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(Data.home_buttons),
    )


# Repo Message
@Client.on_message(filter("repo"))
async def repo(bot, msg):
    await bot.send_message(
        msg.chat.id,
        Data.REPO,
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(Data.home_buttons),
    )
