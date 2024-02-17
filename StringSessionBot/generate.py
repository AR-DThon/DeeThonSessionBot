from asyncio.exceptions import TimeoutError
from Data import Data
from pyrogram import Client, filters
from telethon import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.sessions import StringSession
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import (
    ApiIdInvalid,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
    PasswordHashInvalid,
)
from telethon.errors import (
    ApiIdInvalidError,
    PhoneNumberInvalidError,
    PhoneCodeInvalidError,
    PhoneCodeExpiredError,
    SessionPasswordNeededError,
    PasswordHashInvalidError,
)


@Client.on_message(filters.private & ~filters.forwarded & filters.command("generate"))
async def main(_, msg):
    await msg.reply(
        "||» اذا كان حسابك جديد او وهمي (ليس رقم حقيقي) فأستخرج كود بايروجرام لكي لا ينحذف حسابك فأذا كنت تستخدم رقم حقيقي وقديم فأستخرج كود تيرمكس||",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("بايروجرام", callback_data="pyrogram"),
                    InlineKeyboardButton("تيرمكس", callback_data="telethon"),
                ]
            ]
        ),
    )


async def generate_session(bot, msg, telethon=False):
    await msg.reply(
        "تم بدء  {} استخراج الجلسة...".format(
            "Telethon" if telethon else "Pyrogram"
        )
    )
    user_id = msg.chat.id
    api_id_msg = await bot.ask(
        user_id, "**⎆┊ أرسـل الاب أيـدي الخـاص بـك - Send APP ID Bro ...**", filters=filters.text
    )
    if await cancelled(api_id_msg):
        return
    try:
        api_id = int(api_id_msg.text)
    except ValueError:
        await api_id_msg.reply(
            "غير صالحAPI_ID(أعد المحاولة).  الخاص بك غير صالح حاول مرة أخرى.",
            quote=True,
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return
    api_hash_msg = await bot.ask(
        user_id, "**⎆┊ أرسـل الأيبـي هـاش الخـاص بـك - Send API HASH Bro...**", filters=filters.text
    )
    if await cancelled(api_id_msg):
        return
    api_hash = api_hash_msg.text
    phone_number_msg = await bot.ask(
        user_id,
        "**⎆┊ يـرجـى إرسـال رقـم هاتفـك مـع رمـز الدولة\nمثــال 📱: +96479702387**",
        filters=filters.text,
    )
    if await cancelled(api_id_msg):
        return
    phone_number = phone_number_msg.text
    await msg.reply("جاري إرسال الكود انتظر قليلًا لطفًا ♥️...")
    if telethon:
        client = TelegramClient(StringSession(), api_id, api_hash)
    else:
        client = Client(":memory:", api_id, api_hash)
    await client.connect()
    try:
        if telethon:
            code = await client.send_code_request(phone_number)
        else:
            code = await client.send_code(phone_number)
    except (ApiIdInvalid, ApiIdInvalidError):
        await msg.reply(
            "**⎆┊ الأيبـي أيـدي والأيبـي هـاش غير صالحـان أعـد استخـراج الجلسـة مـرة أخـرى 😭**",
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return
    except (PhoneNumberInvalid, PhoneNumberInvalidError):
        await msg.reply(
            "**⎆┊ رقـم الهـاتف الذي أرسلـته غير صالح أعـد استخـراج الجلسـة مـرة أخـرى.**",
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return
    try:
        phone_code_msg = await bot.ask(user_id, "[ارسل الكود مثل اللي في الصورة ](https://telegra.ph/file/da1af082c6b754959ab47.jpg)»  🔍من فضلك افحص حسابك بالتليجرام وتفقد الكود من حساب إشعارات التليجرام. إذا كان\n  هناك تحقق بخطوتين( المرور ) ، أرسل كلمة المرور هنا بعد إرسال كود الدخول بالتنسيق أدناه.- إذا كانت كلمة المرور او الكود  هي\n 12345 يرجى إرسالها بالشكل التالي 1 2 3 4 5 مع وجود مسـافـات بين الارقام إذا احتجت مساعدة @l_lllv.", filters=filters.text, timeout=600)
        if await cancelled(api_id_msg):
            return
    except TimeoutError:
        await msg.reply(
            "لقد تجاوزت الحد الزمني 10 دقائق أعد استخراج الجلسة مرة أخرى.",
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return
    phone_code = phone_code_msg.text.replace(" ", "")
    try:
        if telethon:
            await client.sign_in(phone_number, phone_code, password=None)
        else:
            await client.sign_in(phone_number, code.phone_code_hash, phone_code)
    except (PhoneCodeInvalid, PhoneCodeInvalidError):
        await msg.reply(
            "**⎆┊ الكـود الخـاص بـك غير صالـح\nأعد استخـراج الجلسـة مـرة أخـرى**",
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return
    except (PhoneCodeExpired, PhoneCodeExpiredError):
        await msg.reply(
            "**⎆┊ انتهت مـدة الكـود\nأعـد استخـراج الجلسـة مـرة أخـرى**",
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return
    except (SessionPasswordNeeded, SessionPasswordNeededError):
        try:
            two_step_msg = await bot.ask(
                user_id,
                "التحقق بخطوتين مفعل بحسابك لذا قم بإدخاله هنا لطفًا.",
                filters=filters.text,
                timeout=300,
            )
        except TimeoutError:
            await msg.reply(
                "لقد تجاوزت المدة الزمنية يجب عليك إعادة استخراج الجلسة مرة أخرى",
                reply_markup=InlineKeyboardMarkup(Data.generate_button),
            )
            return
        try:
            password = two_step_msg.text
            if telethon:
                await client.sign_in(password=password)
            else:
                await client.check_password(password=password)
            if await cancelled(api_id_msg):
                return
        except (PasswordHashInvalid, PasswordHashInvalidError):
            await two_step_msg.reply(
                "التحقق بخطوتين الذي ادخلته خطأ يرجى إعادة الاستخراج مرة أخرى 🤍.",
                quote=True,
                reply_markup=InlineKeyboardMarkup(Data.generate_button),
            )
            return
    if telethon:
        string_session = client.session.save()
    else:
        string_session = await client.export_session_string()
    text = "**{} كود الجلسة** \n\n`{}` \n**استخرجت بواسطة مُستخرج الجوكر\nانتبه لا تعطي الرمز لأي أحد يمكنه الدخول لحسابك عبره كما يستطيع حذف حسابك! @deethon**".format(
"تيرمكس" if telethon else "بايروجرام", string_session
    )
    try:
        await client.send_message("me", text)
    except KeyError:
        pass
    await client.disconnect()
    await phone_code_msg.reply(
        "تم استخراج {} الجلسة. \n\nيرجى تفحص الرسائل المحفوظة! \n\nمن @deethon".format(
            "telethon" if telethon else "pyrogram"
        )
    )

async def cancelled(msg):
    if "/cancel" in msg.text:
        await msg.reply(
            "تم إلغاء استخراج الجلسة!",
            quote=True,
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return True
    elif "/restart" in msg.text:
        await msg.reply(
            "تم ترسيت البوت!",
            quote=True,
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return True
    elif msg.text.startswith("/"):  # Bot Commands
        await msg.reply("تم إلغاؤه!", quote=True)
        return True
    else:
        return False 
