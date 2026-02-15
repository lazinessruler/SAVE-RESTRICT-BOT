# Developed by: LastPerson07 × cantarella
# Modified by: Flexyy Joren 🔥
# Telegram: @xFlexyy | @DragonByte_Network

import os
import asyncio
import random
import time
import shutil
import pyrogram
import requests
import hashlib 
from pyrogram import Client, filters, enums
from pyrogram.errors import (
    FloodWait, UserIsBlocked, InputUserDeactivated, UserAlreadyParticipant,
    InviteHashExpired, UsernameNotOccupied, AuthKeyUnregistered, UserDeactivated, UserDeactivatedBan
)
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery, InputMediaPhoto
from config import API_ID, API_HASH, ERROR_MESSAGE
from database.db import db
import math
from logger import LOGGER

logger = LOGGER(__name__)

SUBSCRIPTION = os.environ.get('SUBSCRIPTION', 'https://graph.org/file/242b7f1b52743938d81f1.jpg')
FREE_LIMIT_SIZE = 2 * 1024 * 1024 * 1024
FREE_LIMIT_DAILY = 10
UPI_ID = os.environ.get("UPI_ID", "your_upi@oksbi")
QR_CODE = os.environ.get("QR_CODE", "https://graph.org/file/242b7f1b52743938d81f1.jpg")

# ==================== 🔥 ULTRA PREMIUM IMAGES ====================
START_IMAGES = [
    "https://i.postimg.cc/Hx1qXv0f/0f22a4ab4d44a829a33797eb7d8fbdc6.jpg",
    "https://i.postimg.cc/j5YpP3Qb/22df44ff326cbce5d99344d904e993af.jpg",
    "https://i.postimg.cc/26Nsh9dg/2b8ed2a65ecec6caa3c442cd08cffd27.jpg",
    "https://i.postimg.cc/Kzh6Bprz/6274337955fefbe4c95d4712714597e4.jpg",
    "https://i.postimg.cc/SsLwrLDN/9a8fe855f0dc641cf81aae32d9f0e9bb.jpg",
    "https://i.postimg.cc/vB7pz73Z/a08029e31cd662dcb778a917b09deee4.jpg",
    "https://i.postimg.cc/ydhwPhvz/a85d30361837800fd31935ec137863bf.jpg",
    "https://i.postimg.cc/LsPdqFPW/b6e808ff4ded204ba2abadedaeeef2b2.jpg",
    "https://i.postimg.cc/vBwJf2Ly/bd7b083aebb810f4ffba2d60ee98053a.jpg",
    "https://i.postimg.cc/W3mQnmXc/cfbf4a2ce731632aa88dd87456844586.jpg",
    "https://i.postimg.cc/85dqHdtS/f4895703153ffd7f73fa8024eada8287.jpg"
]

REACTIONS = [
    "👍", "❤️", "🔥", "🥰", "👏", "😁", "🤔", "🤯", "😱", "🤬",
    "😢", "🎉", "🤩", "🤮", "💩", "🙏", "👌", "🕊", "🤡", "🥱",
    "🥴", "😍", "🐳", "❤️‍🔥", "🌚", "🌭", "💯", "🤣", "⚡", "🍌",
    "🏆", "💔", "🤨", "😐", "🍓", "🍾", "💋", "🖕", "😈", "😴",
    "😭", "🤓", "👻", "👨‍💻", "👀", "🎃", "🙈", "😇", "😨", "🤝",
    "✍", "🤗", "🫡", "🎅", "🎄", "☃", "💅", "🤪", "🗿", "🆒",
    "💘", "🙉", "🦄", "😘", "💊", "🙊", "😎", "👾", "🤷‍♂️", "🤷‍♀️",
    "😡"
]

# ==================== 🔥 ULTRA COOL FONTS ====================
def small_caps(text: str) -> str:
    """Convert to small caps - Premium Font Style 1"""
    normal = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    small = "ᴀʙᴄᴅᴇғɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢᴀʙᴄᴅᴇғɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢ"
    result = ""
    for char in text:
        if char in normal:
            idx = normal.index(char)
            result += small[idx]
        else:
            result += char
    return result

def bold_style(text: str) -> str:
    """Convert to bold unicode - Premium Font Style 2"""
    normal = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    bold = "𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵"
    result = ""
    for char in text:
        if char in normal:
            idx = normal.index(char)
            result += bold[idx]
        else:
            result += char
    return result

def italic_style(text: str) -> str:
    """Convert to italic unicode - Premium Font Style 3"""
    normal = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    italic = "𝘢𝘣𝘤𝘥𝘦𝘧𝘨𝘩𝘪𝘫𝘬𝘭𝘮𝘯𝘰𝘱𝘲𝘳𝘴𝘵𝘶𝘷𝘸𝘹𝘺𝘻𝘈𝘉𝘊𝘋𝘌𝘍𝘎𝘏𝘐𝘑𝘒𝘓𝘔𝘕𝘖𝘗𝘘𝘙𝘚𝘛𝘜𝘝𝘞𝘟𝘠𝘡"
    result = ""
    for char in text:
        if char in normal:
            idx = normal.index(char)
            result += italic[idx]
        else:
            result += char
    return result

def double_struck(text: str) -> str:
    """Convert to double struck - Premium Font Style 4"""
    normal = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    double = "𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ𝟘𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡"
    result = ""
    for char in text:
        if char in normal:
            idx = normal.index(char)
            result += double[idx]
        else:
            result += char
    return result

def get_random_premium_image() -> str:
    """Return random premium image"""
    return random.choice(START_IMAGES)

# ==================== 🔥 ULTRA COOL TEXT CLASS ====================
class script(object):
   
    # 🔥 START MENU - ULTRA COOL
    START_TXT = """
<b>{}</b>

<b>✨ {} ✨</b>
<i>{}</i>

<blockquote>
┏━━━━━━━━━━━━━━━━━━━┓
┃ <b>🚀 {}</b>     ┃
┃ <b>⚡ {}</b>  ┃
┃ <b>🔐 {}</b>      ┃
┃ <b>📊 {}</b>      ┃
┗━━━━━━━━━━━━━━━━━━━┛
</blockquote>

<b>🔥 {} 🔥</b>
""".format(
    double_struck("𝗪𝗘𝗟𝗖𝗢𝗠𝗘 𝗧𝗢 𝗥𝗘𝗦𝗧𝗥𝗜𝗖𝗧𝗘𝗗 𝗦𝗔𝗩𝗘𝗥"),
    small_caps("Hello {}, I'm").format("{}") + " <a href=https://t.me/{}>{}</a>".format("{}", "{}"),
    italic_style("Your Ultimate Restricted Content Saver Bot"),
    small_caps("System Status: 🟢 Online"),
    small_caps("Performance: 10x High-Speed"),
    small_caps("Security: End-to-End"),
    small_caps("Uptime: 99.9% Guaranteed"),
    small_caps("Select Option Below to Get Started")
)

    # 🔥 HELP MENU - ULTRA COOL
    HELP_TXT = """
<b>{}</b>

<blockquote><b>╔════════════════════╗</b>
<b>║  {}  ║</b>
<b>╚════════════════════╝</b></blockquote>

<blockquote><b>🔰 {} 🔰</b>
• {}
• {}
• <i>{}</i> <code>https://t.me/channel/123</code></blockquote>

<blockquote><b>🔒 {} 🔒</b>
• {} <code>/login</code> {}
• {} <code>t.me/c/123...</code>
• {}</blockquote>

<blockquote><b>📦 {} 📦</b>
• {} <code>/batch</code>
• {}</blockquote>

<blockquote><b>⚠️ {} ⚠️</b>
• <b>{}</b> 10 {}
• <b>{}</b> 2GB {}</blockquote>

<blockquote><b>💎 {} 💎</b>
• {}
• {}</blockquote>
""".format(
    double_struck("𝗛𝗘𝗟𝗣 𝗗𝗘𝗦𝗞"),
    small_caps("Comprehensive User Guide"),
    small_caps("Public Channels"),
    small_caps("Forward or send post link directly"),
    small_caps("Compatible with any public channel/group"),
    small_caps("Example Link:"),
    small_caps("Private Channels"),
    small_caps("Use"),
    small_caps("to securely connect"),
    small_caps("Send private link (e.g.,"),
    small_caps("Bot accesses using your session"),
    small_caps("Batch Mode"),
    small_caps("Initiate with"),
    small_caps("for multiple files"),
    small_caps("Free Limits"),
    small_caps("Daily Quota:"),
    small_caps("Files"),
    small_caps("File Size:"),
    small_caps("Max"),
    small_caps("Premium Benefits"),
    small_caps("Unlimited Downloads • No Restrictions"),
    small_caps("Priority Support • Advanced Features")
)

    # 🔥 ABOUT MENU - ULTRA COOL
    ABOUT_TXT = """
<b>{}</b>

<blockquote>
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ <b>🤖 {}</b> ┃
┃ <b>👨‍💻 {}</b> ┃
┃ <b>📚 {}</b> ┃
┃ <b>🐍 {}</b> ┃
┃ <b>🗄 {}</b> ┃
┃ <b>📡 {}</b> ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
</blockquote>

<b>⚡ {} ⚡</b>
""".format(
    double_struck("𝗔𝗕𝗢𝗨𝗧 𝗦𝗬𝗦𝗧𝗘𝗠"),
    small_caps("Bot Name:") + " <a href=http://t.me/THEUPDATEDGUYS_Bot>Save Content Pro</a>",
    small_caps("Developer:") + " <a href=https://t.me/DmOwner>Ⓜ️ark X cantarella × Flexyy</a>",
    small_caps("Library:") + " <a href='https://docs.pyrogram.org/'>Pyrogram Async</a>",
    small_caps("Language:") + " <a href='https://www.python.org/'>Python 3.11+</a>",
    small_caps("Database:") + " <a href='https://www.mongodb.com/'>MongoDB Atlas</a>",
    small_caps("Hosting:") + " Dedicated High-Speed VPS",
    small_caps("Powered by DragonByte Network")
)

    # 🔥 PREMIUM MENU - ULTRA COOL
    PREMIUM_TEXT = """
<b>{}</b>
<b>{}</b>

<blockquote>
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ <b>✨ {}</b> ✨ ┃
┃ <b>♾️ {}</b> ┃
┃ <b>📂 {} 4GB+ {}</b> ┃
┃ <b>⚡ {} {}</b> ┃
┃ <b>🖼 {}</b> ┃
┃ <b>📝 {}</b> ┃
┃ <b>🛂 24/7 {}</b> ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
</blockquote>

<blockquote><b>💳 {} 💳</b></blockquote>
┌─────────────────────┐
│ • <b>1 {}:</b> ₹50 / $1      │
│ • <b>3 {}:</b> ₹120 / $2.5   │
│ • <b>{}:</b> ₹200 / $4       │
└─────────────────────┘

<blockquote><b>💸 {} 💸</b></blockquote>
<b>UPI ID:</b> <code>{}</code>
<b>QR Code:</b> <a href='{}'>📸 {}</a>

<i>{}</i>
""".format(
    double_struck("𝗣𝗥𝗘𝗠𝗜𝗨𝗠 𝗠𝗘𝗠𝗕𝗘𝗥𝗦𝗛𝗜𝗣"),
    bold_style("Unlock Unlimited Power! ⚡"),
    small_caps("Key Benefits"),
    small_caps("Unlimited Daily Downloads"),
    small_caps("Support for"),
    small_caps("File Sizes"),
    small_caps("Instant Processing"),
    small_caps("(Zero Delay)"),
    small_caps("Customizable Thumbnails"),
    small_caps("Personalized Captions"),
    small_caps("Priority Support"),
    small_caps("Pricing Options"),
    small_caps("Month Plan"),
    small_caps("Month Plan"),
    small_caps("Lifetime Access"),
    small_caps("Secure Payment"),
    UPI_ID,
    QR_CODE,
    small_caps("Scan to Pay"),
    italic_style("After Payment: Send Screenshot to @DmOwner for Instant Activation!")
)

    # 🔥 PROGRESS BAR - ULTRA COOL
    PROGRESS_BAR = """
<b>{}</b>
<blockquote>
┌─────────────────────┐
│ <b>📊 {}:</b> {bar} {percentage:.1f}%  │
│ <b>🚀 {}:</b> <code>{speed}/s</code>       │
│ <b>💾 {}:</b> <code>{current} {total}</code>  │
│ <b>⏱ {}:</b> <code>{elapsed}</code>      │
│ <b>⏳ {}:</b> <code>{eta}</code>         │
└─────────────────────┘
</blockquote>
""".format(
    bold_style("⚡ PROCESSING TASK... ⚡"),
    small_caps("Progress"),
    small_caps("Speed"),
    small_caps("Size"),
    small_caps("of"),
    small_caps("Elapsed"),
    small_caps("ETA")
)

    # 🔥 CAPTION - ULTRA COOL
    CAPTION = """
<b><a href="https://t.me/THEUPDATEDGUYS">{}</a></b>

<b>⚜️ {} ⚜️</b>
<b><a href="https://t.me/THEUPDATEDGUYS">{}</a></b>
""".format(
    double_struck("ᴘᴏᴡᴇʀᴇᴅ ʙʏ ᴛʜᴇ ᴜᴘᴅᴀᴛᴇᴅ ɢᴜʏs"),
    small_caps("Powered By"),
    bold_style("THE UPDATED GUYS 😎")
)

    # 🔥 ERROR MESSAGES - ULTRA COOL
    LIMIT_REACHED = """
<b>{}</b>

┌─────────────────────┐
│ <b>⚠️ {}</b> │
│ <i>{}</i> │
└─────────────────────┘

<blockquote><b>🔓 {}!</b></blockquote>
<i>{}</i>
""".format(
    double_struck("𝗗𝗔𝗜𝗟𝗬 𝗟𝗜𝗠𝗜𝗧 𝗘𝗫𝗖𝗘𝗘𝗗𝗘𝗗"),
    small_caps("Your 10 free saves for today are used"),
    small_caps("Quota resets after 24 hours"),
    small_caps("Upgrade to Premium for Unlimited"),
    small_caps("Remove restrictions & enjoy seamless downloading")
)

    SIZE_LIMIT = """
<b>{}</b>

┌─────────────────────┐
│ <b>⚠️ {} 2GB {}.</b> │
└─────────────────────┘

<blockquote><b>🔓 {}</b></blockquote>
<i>{} 4GB+ {}!</i>
""".format(
    double_struck("𝗙𝗜𝗟𝗘 𝗦𝗜𝗭𝗘 𝗘𝗫𝗖𝗘𝗘𝗗𝗘𝗗"),
    small_caps("Free tier limited to"),
    small_caps("per file"),
    small_caps("Upgrade to Premium"),
    small_caps("Download files up to"),
    small_caps("with no limits")
)

    LOGIN_REQUIRED = """
<b>{}</b>

┌─────────────────────┐
│ 🔒 <i>{}</i> │
│ 📌 <i>{}</i> │
│ 🔑 <i>{} /login</i>    │
└─────────────────────┘
""".format(
    double_struck("𝗔𝗨𝗧𝗛𝗘𝗡𝗧𝗜𝗖𝗔𝗧𝗜𝗢𝗡 𝗥𝗘𝗤𝗨𝗜𝗥𝗘𝗗"),
    small_caps("Access requires login"),
    small_caps("This is a private channel"),
    small_caps("Use")
)

    CANCELLED = """
<b>{}</b>
└────── <b>❌</b> ──────┘
""".format(double_struck("𝗧𝗔𝗦𝗞 𝗖𝗔𝗡𝗖𝗘𝗟𝗟𝗘𝗗"))
    
    PROCESSING = """
<b>{}</b>
┌─────────────────────┐
│ <i>{}</i> │
│ <i>{}</i> │
└─────────────────────┘
""".format(
    double_struck("𝗣𝗥𝗢𝗖𝗘𝗦𝗦𝗜𝗡𝗚"),
    small_caps("A task is currently processing"),
    small_caps("Please wait or use /cancel to stop")
)

def humanbytes(size):
    if not size:
        return "0B"
    power = 2**10
    n = 0
    Dic_powerN = {0: ' ', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n] + 'B'

def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + "d, ") if days else "") + \
        ((str(hours) + "h, ") if hours else "") + \
        ((str(minutes) + "m, ") if minutes else "") + \
        ((str(seconds) + "s, ") if seconds else "")
    return tmp[:-2] if tmp else "0s"

class batch_temp(object):
    IS_BATCH = {}

def get_message_type(msg):
    if getattr(msg, 'document', None): return "Document"
    if getattr(msg, 'video', None): return "Video"
    if getattr(msg, 'photo', None): return "Photo"
    if getattr(msg, 'audio', None): return "Audio"
    if getattr(msg, 'text', None): return "Text"
    return None

async def downstatus(client, statusfile, message, chat):
    while not os.path.exists(statusfile):
        await asyncio.sleep(3)
    while os.path.exists(statusfile):
        try:
            with open(statusfile, "r", encoding='utf-8') as downread:
                txt = downread.read()
            await client.edit_message_text(chat, message.id, f"{txt}")
            await asyncio.sleep(5)
        except:
            await asyncio.sleep(5)

async def upstatus(client, statusfile, message, chat):
    while not os.path.exists(statusfile):
        await asyncio.sleep(3)
    while os.path.exists(statusfile):
        try:
            with open(statusfile, "r", encoding='utf-8') as upread:
                txt = upread.read()
            await client.edit_message_text(chat, message.id, f"{txt}")
            await asyncio.sleep(5)
        except:
            await asyncio.sleep(5)

def progress(current, total, message, type):
    if batch_temp.IS_BATCH.get(message.from_user.id):
        raise Exception("Cancelled")
    if not hasattr(progress, "cache"):
        progress.cache = {}
   
    now = time.time()
    task_id = f"{message.id}{type}"
    last_time = progress.cache.get(task_id, 0)
   
    if not hasattr(progress, "start_time"):
        progress.start_time = {}
    if task_id not in progress.start_time:
        progress.start_time[task_id] = now
       
    if (now - last_time) > 5 or current == total:
        try:
            percentage = current * 100 / total
            speed = current / (now - progress.start_time[task_id]) if (now - progress.start_time[task_id]) > 0 else 0
            eta = (total - current) / speed if speed > 0 else 0
            elapsed = now - progress.start_time[task_id]
           
            filled_length = int(percentage / 5)
            bar = '█' * filled_length + ' ' * (20 - filled_length)
           
            status = script.PROGRESS_BAR.format(
                bar=bar,
                percentage=percentage,
                current=humanbytes(current),
                total=humanbytes(total),
                speed=humanbytes(speed),
                elapsed=TimeFormatter(elapsed * 1000),
                eta=TimeFormatter(eta * 1000)
            )
           
            with open(f'{message.id}{type}status.txt', "w", encoding='utf-8') as fileup:
                fileup.write(status)
               
            progress.cache[task_id] = now
           
            if current == total:
                progress.start_time.pop(task_id, None)
                progress.cache.pop(task_id, None)
        except:
            pass

@Client.on_message(filters.command(["start"]))
async def send_start(client: Client, message: Message):
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id, message.from_user.first_name)
   
    try:
        await message.react(emoji=random.choice(REACTIONS), big=True)
    except:
        pass
   
    photo_url = get_random_premium_image()
   
    buttons = [
        [
            InlineKeyboardButton("💎 𝙋𝙧𝙚𝙢𝙞𝙪𝙢", callback_data="buy_premium"),
            InlineKeyboardButton("🆘 𝙃𝙚𝙡𝙥", callback_data="help_btn")
        ],
        [
            InlineKeyboardButton("⚙️ 𝙎𝙚𝙩𝙩𝙞𝙣𝙜𝙨", callback_data="settings_btn"),
            InlineKeyboardButton("ℹ️ 𝘼𝙗𝙤𝙪𝙩", callback_data="about_btn")
        ],
        [
            InlineKeyboardButton('📢 𝘾𝙝𝙖𝙣𝙣𝙚𝙡𝙨', callback_data="channels_info"),
            InlineKeyboardButton('👨‍💻 𝘿𝙚𝙫𝙨', callback_data="dev_info")
        ]
    ]
   
    reply_markup = InlineKeyboardMarkup(buttons)
    bot = await client.get_me()
   
    start_text = script.START_TXT.format(
        message.from_user.mention,
        bot.username,
        bot.first_name
    )
   
    await client.send_photo(
        chat_id=message.chat.id,
        photo=photo_url,
        caption=start_text,
        reply_markup=reply_markup,
        reply_to_message_id=message.id,
        parse_mode=enums.ParseMode.HTML
    )

@Client.on_message(filters.command(["help"]))
async def send_help(client: Client, message: Message):
    buttons = [[InlineKeyboardButton("❌ 𝘾𝙡𝙤𝙨𝙚", callback_data="close_btn")]]
    await client.send_message(
        chat_id=message.chat.id,
        text=script.HELP_TXT,
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode=enums.ParseMode.HTML
    )

@Client.on_message(filters.command(["plan", "myplan", "premium"]))
async def send_plan(client: Client, message: Message):
    buttons = [
        [InlineKeyboardButton("📸 𝙋𝙖𝙮𝙢𝙚𝙣𝙩 𝙋𝙧𝙤𝙤𝙛", url="https://t.me/DmOwner")],
        [InlineKeyboardButton("❌ 𝘾𝙡𝙤𝙨𝙚", callback_data="close_btn")]
    ]
   
    premium_text = script.PREMIUM_TEXT.format(UPI_ID, QR_CODE)
   
    await client.send_photo(
        chat_id=message.chat.id,
        photo=SUBSCRIPTION,
        caption=premium_text,
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode=enums.ParseMode.HTML
    )

@Client.on_message(filters.command(["cancel"]))
async def send_cancel(client: Client, message: Message):
    batch_temp.IS_BATCH[message.from_user.id] = True
    await message.reply_text(script.CANCELLED, parse_mode=enums.ParseMode.HTML)

async def settings_panel(client, callback_query):
    """Settings Menu - Ultra Cool"""
    user_id = callback_query.from_user.id
    is_premium = await db.check_premium(user_id)
    badge = "💎 𝙋𝙧𝙚𝙢𝙞𝙪𝙢" if is_premium else "👤 𝙎𝙩𝙖𝙣𝙙𝙖𝙧𝙙"
   
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("📜 𝘾𝙤𝙢𝙢𝙖𝙣𝙙𝙨", callback_data="cmd_list_btn")],
        [InlineKeyboardButton("📊 𝙐𝙨𝙖𝙜𝙚 𝙎𝙩𝙖𝙩𝙨", callback_data="user_stats_btn")],
        [InlineKeyboardButton("🗑 𝘿𝙪𝙢𝙥 𝘾𝙝𝙖𝙩", callback_data="dump_chat_btn")],
        [InlineKeyboardButton("🖼 𝙏𝙝𝙪𝙢𝙗𝙣𝙖𝙞𝙡", callback_data="thumb_btn")],
        [InlineKeyboardButton("📝 𝘾𝙖𝙥𝙩𝙞𝙤𝙣", callback_data="caption_btn")],
        [InlineKeyboardButton("⬅️ 𝘽𝙖𝙘𝙠 𝙃𝙤𝙢𝙚", callback_data="start_btn")]
    ])
   
    text = f"""
<b>{double_struck("𝗦𝗘𝗧𝗧𝗜𝗡𝗚𝗦 𝗗𝗔𝗦𝗛𝗕𝗢𝗔𝗥𝗗")}</b>

┌─────────────────────┐
│ <b>{small_caps('Account:')}</b> {badge}    │
│ <b>{small_caps('User ID:')}</b> <code>{user_id}</code> │
└─────────────────────┘

<i>{italic_style('Customize your experience below')}</i>
"""
   
    await callback_query.edit_message_caption(
        caption=text,
        reply_markup=buttons,
        parse_mode=enums.ParseMode.HTML
    )

@Client.on_message(filters.text & filters.private & ~filters.regex("^/"))
async def save(client: Client, message: Message):
    if "https://t.me/" in message.text:
       
        is_limit_reached = await db.check_limit(message.from_user.id)
        if is_limit_reached:
            btn = InlineKeyboardMarkup([[InlineKeyboardButton("💎 𝙐𝙥𝙜𝙧𝙖𝙙𝙚 𝙋𝙧𝙚𝙢𝙞𝙪𝙢", callback_data="buy_premium")]])
            return await message.reply_photo(
                photo=SUBSCRIPTION,
                caption=script.LIMIT_REACHED,
                reply_markup=btn,
                parse_mode=enums.ParseMode.HTML
            )
       
        if batch_temp.IS_BATCH.get(message.from_user.id) == False:
            return await message.reply_text(script.PROCESSING, parse_mode=enums.ParseMode.HTML)
       
        datas = message.text.split("/")
        temp = datas[-1].replace("?single", "").split("-")
        fromID = int(temp[0].strip())
        try:
            toID = int(temp[1].strip())
        except:
            toID = fromID
       
        batch_temp.IS_BATCH[message.from_user.id] = False
        is_private_link = "https://t.me/c/" in message.text
        is_batch = "https://t.me/b/" in message.text
        is_public_link = not is_private_link and not is_batch
       
        for msgid in range(fromID, toID + 1):
           
            if batch_temp.IS_BATCH.get(message.from_user.id):
                break
           
            if is_public_link:
                username = datas[3]
                try:
                    await client.copy_message(
                        chat_id=message.chat.id,
                        from_chat_id=username,
                        message_id=msgid,
                        reply_to_message_id=message.id
                    )
                    await db.add_traffic(message.from_user.id)
                    await asyncio.sleep(1)
                    continue
                except Exception as e:
                    pass
           
            user_data = await db.get_session(message.from_user.id)
            if user_data is None:
                await message.reply(
                    script.LOGIN_REQUIRED,
                    parse_mode=enums.ParseMode.HTML
                )
                batch_temp.IS_BATCH[message.from_user.id] = True
                return
           
            try:
                acc = Client(
                    "saverestricted",
                    session_string=user_data,
                    api_hash=API_HASH,
                    api_id=API_ID,
                    in_memory=True,
                    max_concurrent_transmissions=10
                )
                await acc.connect()
            except Exception as e:
                batch_temp.IS_BATCH[message.from_user.id] = True
                return await message.reply(f"<b>❌ Authentication Failed</b>\n\n<i>Your session may have expired. Please /logout and /login again.</i>\n<code>{e}</code>", parse_mode=enums.ParseMode.HTML)
           
            if is_private_link:
                chatid = int("-100" + datas[4])
                await handle_restricted_content(client, acc, message, chatid, msgid)
            elif is_batch:
                username = datas[4]
                await handle_restricted_content(client, acc, message, username, msgid)
            else:
                username = datas[3]
                await handle_restricted_content(client, acc, message, username, msgid)
           
            await asyncio.sleep(2)
       
        batch_temp.IS_BATCH[message.from_user.id] = True

async def handle_restricted_content(client: Client, acc, message: Message, chat_target, msgid):
    try:
        msg: Message = await acc.get_messages(chat_target, msgid)
    except Exception as e:
        logger.error(f"Error fetching message: {e}")
        return
   
    if msg.empty:
        return
   
    msg_type = get_message_type(msg)
    if not msg_type:
        return
   
    file_size = 0
    if msg_type == "Document": file_size = msg.document.file_size
    elif msg_type == "Video": file_size = msg.video.file_size
    elif msg_type == "Audio": file_size = msg.audio.file_size
   
    if file_size > FREE_LIMIT_SIZE:
        if not await db.check_premium(message.from_user.id):
            btn = InlineKeyboardMarkup([[InlineKeyboardButton("💎 𝙐𝙥𝙜𝙧𝙖𝙙𝙚 𝙋𝙧𝙚𝙢𝙞𝙪𝙢", callback_data="buy_premium")]])
            await client.send_message(
                message.chat.id,
                script.SIZE_LIMIT,
                reply_markup=btn,
                parse_mode=enums.ParseMode.HTML
            )
            return
   
    if msg_type == "Text":
        try:
            await client.send_message(message.chat.id, msg.text, entities=msg.entities, parse_mode=enums.ParseMode.HTML)
            return
        except:
            return
   
    await db.add_traffic(message.from_user.id)
    smsg = await client.send_message(message.chat.id, f"<b>⬇️ {small_caps('Starting Download...')}</b>", reply_to_message_id=message.id, parse_mode=enums.ParseMode.HTML)
   
    temp_dir = f"downloads/{message.id}"
    if not os.path.exists(temp_dir): os.makedirs(temp_dir)
   
    try:
        asyncio.create_task(downstatus(client, f'{message.id}downstatus.txt', smsg, message.chat.id))
       
        file = await acc.download_media(
            msg,
            file_name=f"{temp_dir}/",
            progress=progress,
            progress_args=[message, "down"]
        )
       
        if os.path.exists(f'{message.id}downstatus.txt'): os.remove(f'{message.id}downstatus.txt')
       
    except Exception as e:
        if batch_temp.IS_BATCH.get(message.from_user.id) or "Cancelled" in str(e):
            if os.path.exists(temp_dir): shutil.rmtree(temp_dir)
            return await smsg.edit(script.CANCELLED)
        return await smsg.delete()
   
    try:
        asyncio.create_task(upstatus(client, f'{message.id}upstatus.txt', smsg, message.chat.id))
       
        ph_path = None
        thumb_id = await db.get_thumbnail(message.from_user.id)
       
        if thumb_id:
            try:
                ph_path = await client.download_media(thumb_id, file_name=f"{temp_dir}/custom_thumb.jpg")
            except Exception as e:
                logger.error(f"Failed to download custom thumb: {e}")
       
        if not ph_path:
            try:
                if msg_type == "Video" and msg.video.thumbs:
                    ph_path = await acc.download_media(msg.video.thumbs[0].file_id, file_name=f"{temp_dir}/thumb.jpg")
                elif msg_type == "Document" and msg.document.thumbs:
                    ph_path = await acc.download_media(msg.document.thumbs[0].file_id, file_name=f"{temp_dir}/thumb.jpg")
            except:
                pass
       
        custom_caption = await db.get_caption(message.from_user.id)
        if custom_caption:
            final_caption = custom_caption.format(filename=file.split("/")[-1], size=humanbytes(file_size))
        else:
            final_caption = script.CAPTION
            if msg.caption:
                final_caption += f"\n\n{msg.caption}"
       
        if msg_type == "Document":
            await client.send_document(message.chat.id, file, thumb=ph_path, caption=final_caption, progress=progress, progress_args=[message, "up"])
        elif msg_type == "Video":
            await client.send_video(message.chat.id, file, duration=msg.video.duration, width=msg.video.width, height=msg.video.height, thumb=ph_path, caption=final_caption, progress=progress, progress_args=[message, "up"])
        elif msg_type == "Audio":
            await client.send_audio(message.chat.id, file, thumb=ph_path, caption=final_caption, progress=progress, progress_args=[message, "up"])
        elif msg_type == "Photo":
            await client.send_photo(message.chat.id, file, caption=final_caption)
       
    except Exception as e:
         await smsg.edit(f"Upload Failed: {e}")
   
    if os.path.exists(f'{message.id}upstatus.txt'): os.remove(f'{message.id}upstatus.txt')
    if os.path.exists(temp_dir): shutil.rmtree(temp_dir)
    await client.delete_messages(message.chat.id, [smsg.id])

@Client.on_callback_query()
async def button_callbacks(client: Client, callback_query: CallbackQuery):
    data = callback_query.data
    message = callback_query.message
    if not message: return
   
    if data == "dev_info":
        await callback_query.answer(
            text=f"""👨‍💻 {bold_style('DEVELOPER TEAM')} 👨‍💻

╔══════════════════╗
║ • @DmOwner       ║
║ • @akaza7902     ║
║ • @xFlexyy       ║
╚══════════════════╝

{italic_style('Powered by DragonByte Network')}""",
            show_alert=True
        )
   
    elif data == "channels_info":
        await callback_query.answer(
            text=f"""📢 {bold_style('OFFICIAL CHANNELS')} 📢

╔══════════════════╗
║ • @ReX_update    ║
║ • @THEUPDATEDGUYS║
║ • @DragonByte_Network ║
╚══════════════════╝

{italic_style('Stay updated for new features!')}""",
            show_alert=True
        )
   
    elif data == "settings_btn":
        await settings_panel(client, callback_query)
   
    elif data == "buy_premium":
        buttons = [
            [InlineKeyboardButton("📸 𝙋𝙖𝙮𝙢𝙚𝙣𝙩 𝙋𝙧𝙤𝙤𝙛", url="https://t.me/DmOwner")],
            [InlineKeyboardButton("⬅️ 𝘽𝙖𝙘𝙠 𝙃𝙤𝙢𝙚", callback_data="start_btn")]
        ]
       
        premium_text = script.PREMIUM_TEXT.format(UPI_ID, QR_CODE)
       
        await client.edit_message_media(
            chat_id=message.chat.id,
            message_id=message.id,
            media=InputMediaPhoto(
                media=SUBSCRIPTION,
                caption=premium_text
            ),
            reply_markup=InlineKeyboardMarkup(buttons)
        )
   
    elif data == "help_btn":
        buttons = [[InlineKeyboardButton("⬅️ 𝘽𝙖𝙘𝙠 𝙃𝙤𝙢𝙚", callback_data="start_btn")]]
        await client.edit_message_caption(
            chat_id=message.chat.id,
            message_id=message.id,
            caption=script.HELP_TXT,
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=enums.ParseMode.HTML
        )
   
    elif data == "about_btn":
        buttons = [[InlineKeyboardButton("⬅️ 𝘽𝙖𝙘𝙠 𝙃𝙤𝙢𝙚", callback_data="start_btn")]]
        await client.edit_message_caption(
            chat_id=message.chat.id,
            message_id=message.id,
            caption=script.ABOUT_TXT,
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=enums.ParseMode.HTML
        )
   
    elif data == "start_btn":
        bot = await client.get_me()
        photo_url = get_random_premium_image()
       
        buttons = [
            [
                InlineKeyboardButton("💎 𝙋𝙧𝙚𝙢𝙞𝙪𝙢", callback_data="buy_premium"),
                InlineKeyboardButton("🆘 𝙃𝙚𝙡𝙥", callback_data="help_btn")
            ],
            [
                InlineKeyboardButton("⚙️ 𝙎𝙚𝙩𝙩𝙞𝙣𝙜𝙨", callback_data="settings_btn"),
                InlineKeyboardButton("ℹ️ 𝘼𝙗𝙤𝙪𝙩", callback_data="about_btn")
            ],
            [
                InlineKeyboardButton('📢 𝘾𝙝𝙖𝙣𝙣𝙚𝙡𝙨', callback_data="channels_info"),
                InlineKeyboardButton('👨‍💻 𝘿𝙚𝙫𝙨', callback_data="dev_info")
            ]
        ]
       
        start_text = script.START_TXT.format(
            callback_query.from_user.mention,
            bot.username,
            bot.first_name
        )
       
        await client.edit_message_media(
            chat_id=message.chat.id,
            message_id=message.id,
            media=InputMediaPhoto(
                media=photo_url,
                caption=start_text
            ),
            reply_markup=InlineKeyboardMarkup(buttons)
        )
   
    elif data == "close_btn":
        await message.delete()
   
    elif data in ["cmd_list_btn", "user_stats_btn", "dump_chat_btn", "thumb_btn", "caption_btn"]:
        await callback_query.answer("🔄 𝘾𝙤𝙢𝙞𝙣𝙜 𝙎𝙤𝙤𝙣! 🔥", show_alert=True)
   
    await callback_query.answer()
