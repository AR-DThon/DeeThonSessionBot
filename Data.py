from pyrogram.types import InlineKeyboardButton


class Data:
    generate_single_button = [
        InlineKeyboardButton("بدء استخراج الجلسة", callback_data="generate")
    ]

    home_buttons = [
        generate_single_button,
        [InlineKeyboardButton(text="父 العودة إلى الصفحة الرئيسية", callback_data="home")],
    ]

    generate_button = [generate_single_button]

    buttons = [
        generate_single_button,
        [
            InlineKeyboardButton(
                "سورس الجوكر ", url="https://t.me/jepthon"
            )
        ],
        [
            InlineKeyboardButton("كيفية استخدام البوت ?", callback_data="help"),
            InlineKeyboardButton("حـول", callback_data="about"),
        ],
        [InlineKeyboardButton("المطور", url="https://t.me/jepthon")],
    ]

    START = """
أهلًا {} ♦
ومرحبًا بك عزيزي في {}
هذا البوت مخصص لاستخراج الجلسات
إذا كنـت تريـد أن يكون حسـابك في أمـان تام فاختر بايروجـرام أمـا إذا كـان رقمك حقيقـي فاختر تيرمـكس
المطور :- @lMl10l
    """

    HELP = """
 **الأوامر المتاحة**

/about - لحول البوت
/help - لمساعدتك
/start - لبدء البوت 
/repo - لإعطاء ريبو البوت
/generate - لاستخراج الجلسات 
/cancel - لإلغاء الاستخراج 
/restart - لترسيت اليوت
"""

    # About Message
    ABOUT = """
**حول البوت** 

هذا هو بوت استخراج كود تيرمكس وبايروجرام مقدم من @jepthon

قناة السورس : [ᴄʟɪᴄᴋ ʜᴇʀᴇ](https://t.me/jepthon)
لغة البرمجة : [ᴘʏʀᴏɢʀᴀᴍ](docs.pyrogram.org)
اللغة : [ᴘʏᴛʜᴏɴ](www.python.org)
المطور : @lml10l
    """

    # Repo Message
    REPO = """
━━━━━━━━━━━━━━━━━━━━━━━━
💥 أنا مشغل لكي أقوم باستخراج الجلسات 
┏━━━━━━━━━━━━━━━━━┓
┣★ المطور : [اضغط هنا](https://t.me/lMl10l)
┣★ [سورس الجوكر](https://t.me/SHA_HM1)
┗━━━━━━━━━━━━━━━━━┛
💞 
إذا كان لديك أي سؤال ، فراسل » المطور » [المطور] @lMl10l
   """
