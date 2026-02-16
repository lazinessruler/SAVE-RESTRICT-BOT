# Developed by: LastPerson07 × cantarella
# Modified by: Flexyy 🔥
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

# ==================== 🔥 PREMIUM IMAGES ====================
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

# ==================== 🔥 SMALL CAPS FONT ONLY ====================
def small_caps(text: str) -> str:
    """Convert to small caps - Premium Font"""
    normal = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    small = "ᴀʙᴄᴅᴇғɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢᴀʙᴄᴅᴇғɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢ𝟶𝟷𝟸𝟹𝟺𝟻𝟼𝟽𝟾𝟿"
    result = ""
    for char in text:
        if char in normal:
            idx = normal.index(char)
            result += small[idx]
        else:
            result += char
    return result

def get_random_premium_image() -> str:
    return random.choice(START_IMAGES)

# ==================== 🔥 THUMBNAIL STATE ====================
class ThumbnailState:
    waiting_for_thumbnail = {}

# ==================== 🔥 TEXT CLASS ====================
class script(object):
   
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
"""

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
"""

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
"""

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
"""

    SETTINGS_TXT = """
<b>{}</b>

┌─────────────────────┐
│ <b>👤 {}</b>    │
│ <b>🆔 {}</b> <code>{}</code> │
└─────────────────────┘

<b>🎯 {}:</b>
"""

    THUMBNAIL_INFO = """
<b>{}</b>

{}
"""

    PROGRESS_BAR = """
<b>⚡ {}</b>

<b>📊 {}:</b> {percentage:.1f}%
<b>🚀 {}:</b> <code>{speed}/s</code>
<b>💾 {}:</b> <code>{current} {total}</code>
<b>⏱ {}:</b> <code>{elapsed}</code>
<b>⏳ {}:</b> <code>{eta}</code>
"""

    CAPTION = """
{}
"""

    LIMIT_REACHED = """
<b>{}</b>

┌─────────────────────┐
│ <b>⚠️ {}</b> │
│ <i>{}</i> │
└─────────────────────┘

<blockquote><b>🔓 {}!</b></blockquote>
<i>{}</i>
"""

    SIZE_LIMIT = """
<b>{}</b>

┌─────────────────────┐
│ <b>⚠️ {} 2GB {}.</b> │
└─────────────────────┘

<blockquote><b>🔓 {}</b></blockquote>
<i>{} 4GB+ {}!</i>
"""

    LOGIN_REQUIRED = """
<b>{}</b>

┌─────────────────────┐
│ 🔒 <i>{}</i> │
│ 📌 <i>{}</i> │
│ 🔑 <i>{} /login</i>    │
└─────────────────────┘
"""

    CANCELLED = """
<b>{}</b>
└────── <b>❌</b> ──────┘
"""
    
    PROCESSING = """
<b>{}</b>
┌─────────────────────┐
│ <i>{}</i> │
│ <i>{}</i> │
└─────────────────────┘
"""

    THUMBNAIL_PROMPT = """
<b>{}</b>

{}
<i>{}</i>
"""

    THUMBNAIL_SUCCESS = """
<b>{}</b>

{}
<b>{}</b> <code>{}</code>
"""

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
           
            status = script.PROGRESS_BAR.format(
                small_caps("PROCESSING TASK..."),
                small_caps("Progress"),
                small_caps("Speed"),
                small_caps("Size"),
                small_caps("of"),
                small_caps("Elapsed"),
                small_caps("ETA"),
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
        except Exception as e:
            logger.error(f"Progress error: {e}")
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
            InlineKeyboardButton(small_caps("💎 Premium"), callback_data="buy_premium"),
            InlineKeyboardButton(small_caps("🆘 Help"), callback_data="help_btn")
        ],
        [
            InlineKeyboardButton(small_caps("⚙️ Settings"), callback_data="settings_btn"),
            InlineKeyboardButton(small_caps("ℹ️ About"), callback_data="about_btn")
        ]
    ]
   
    reply_markup = InlineKeyboardMarkup(buttons)
    bot = await client.get_me()
   
    start_text = script.START_TXT.format(
        small_caps("WELCOME TO RESTRICTED SAVER"),
        small_caps(f"Hello {message.from_user.first_name}, I'm {bot.first_name}"),
        small_caps("Your Ultimate Restricted Content Saver Bot"),
        small_caps("System Status: 🟢 Online"),
        small_caps("Performance: 10x High-Speed"),
        small_caps("Security: End-to-End Encrypted"),
        small_caps("Uptime: 99.9% Guaranteed"),
        small_caps("Select Option Below to Get Started")
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
    buttons = [[InlineKeyboardButton(small_caps("❌ Close"), callback_data="close_btn")]]
    
    help_text = script.HELP_TXT.format(
        small_caps("HELP DESK"),
        small_caps("Comprehensive User Guide"),
        small_caps("Public Channels (No Login)"),
        small_caps("Forward or send post link directly"),
        small_caps("Compatible with any public channel/group"),
        small_caps("Example Link:"),
        small_caps("Private Channels (Login Required)"),
        small_caps("Use"),
        small_caps("to securely connect"),
        small_caps("Send private link (e.g.,"),
        small_caps("Bot accesses using your session"),
        small_caps("Batch Downloading Mode"),
        small_caps("Initiate with"),
        small_caps("for multiple files"),
        small_caps("Free User Limitations"),
        small_caps("Daily Quota:"),
        small_caps("Files / 24 Hours"),
        small_caps("File Size Cap:"),
        small_caps("Maximum"),
        small_caps("Premium Benefits"),
        small_caps("Unlimited Downloads • No Restrictions"),
        small_caps("Priority Support • Advanced Features")
    )
    
    await client.send_message(
        chat_id=message.chat.id,
        text=help_text,
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode=enums.ParseMode.HTML
    )

@Client.on_message(filters.command(["plan", "myplan", "premium"]))
async def send_plan(client: Client, message: Message):
    buttons = [
        [InlineKeyboardButton(small_caps("📸 Send Proof"), url="https://t.me/xFlexyy")],
        [InlineKeyboardButton(small_caps("❌ Close"), callback_data="close_btn")]
    ]
   
    premium_text = script.PREMIUM_TEXT.format(
        small_caps("PREMIUM MEMBERSHIP"),
        small_caps("Unlock Unlimited Power! ⚡"),
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
        small_caps("After Payment: Send Screenshot to @xFlexyy for Instant Activation!")
    )
   
    await client.send_photo(
        chat_id=message.chat.id,
        photo=SUBSCRIPTION,
        caption=premium_text,
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode=enums.ParseMode.HTML
    )

@Client.on_message(filters.command(["settings"]))
async def settings_cmd(client: Client, message: Message):
    user_id = message.from_user.id
    is_premium = await db.check_premium(user_id)
    badge = small_caps("💎 Premium") if is_premium else small_caps("👤 Free User")
    
    # Get thumbnail status
    thumb = await db.get_thumbnail(user_id)
    thumb_status = small_caps("✅ Active") if thumb else small_caps("❌ Not Set")
    
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton(small_caps("🖼️ Set Thumbnail"), callback_data="set_thumb")],
        [InlineKeyboardButton(small_caps("👁️ View Thumbnail"), callback_data="view_thumb")],
        [InlineKeyboardButton(small_caps("🗑️ Remove Thumbnail"), callback_data="remove_thumb")],
        [InlineKeyboardButton(small_caps("📊 My Stats"), callback_data="user_stats_btn")],
        [InlineKeyboardButton(small_caps("⬅️ Back to Home"), callback_data="start_btn")]
    ])
    
    text = script.SETTINGS_TXT.format(
        small_caps("⚙️ Settings Dashboard"),
        badge,
        small_caps("User ID:"),
        user_id,
        small_caps("Current Settings")
    ) + f"\n• {small_caps('Thumbnail:')} {thumb_status}"
    
    photo_url = get_random_premium_image()
    
    await client.send_photo(
        chat_id=message.chat.id,
        photo=photo_url,
        caption=text,
        reply_markup=buttons,
        parse_mode=enums.ParseMode.HTML
    )

@Client.on_callback_query(filters.regex("^set_thumb$"))
async def set_thumb_prompt(client: Client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    
    await callback_query.answer()
    
    ThumbnailState.waiting_for_thumbnail[user_id] = True
    
    text = script.THUMBNAIL_PROMPT.format(
        small_caps("🖼️ Set Custom Thumbnail"),
        small_caps("Please send me a photo to use as your custom thumbnail."),
        small_caps("This will appear on all your downloaded videos.")
    )
    
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton(small_caps("❌ Cancel"), callback_data="cancel_thumb")]
    ])
    
    await callback_query.message.edit_caption(
        caption=text,
        reply_markup=buttons,
        parse_mode=enums.ParseMode.HTML
    )

@Client.on_callback_query(filters.regex("^cancel_thumb$"))
async def cancel_thumb(client: Client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    
    if user_id in ThumbnailState.waiting_for_thumbnail:
        del ThumbnailState.waiting_for_thumbnail[user_id]
    
    await callback_query.answer(small_caps("❌ Cancelled"), show_alert=False)
    await settings_cmd(client, callback_query.message)

@Client.on_message(filters.photo & filters.private)
async def receive_thumbnail(client: Client, message: Message):
    user_id = message.from_user.id
    
    if user_id not in ThumbnailState.waiting_for_thumbnail:
        return
    
    file_id = message.photo[-1].file_id
    
    # Save to database
    await db.set_thumbnail(user_id, file_id)
    
    del ThumbnailState.waiting_for_thumbnail[user_id]
    
    text = script.THUMBNAIL_SUCCESS.format(
        small_caps("✅ Thumbnail Set Successfully!"),
        small_caps("Your custom thumbnail has been saved."),
        small_caps("File ID:"),
        file_id[:20] + "..."
    )
    
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton(small_caps("👁️ View Thumbnail"), callback_data="view_thumb")],
        [InlineKeyboardButton(small_caps("⬅️ Back to Settings"), callback_data="back_to_settings")]
    ])
    
    await message.reply_photo(
        photo=file_id,
        caption=text,
        reply_markup=buttons,
        parse_mode=enums.ParseMode.HTML
    )

@Client.on_callback_query(filters.regex("^view_thumb$"))
async def view_thumbnail(client: Client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    thumb = await db.get_thumbnail(user_id)
    
    if not thumb:
        await callback_query.answer(small_caps("❌ No thumbnail set!"), show_alert=True)
        return
    
    await callback_query.answer()
    
    text = script.THUMBNAIL_INFO.format(
        small_caps("🖼️ Your Current Thumbnail"),
        small_caps("This thumbnail will be used for all your downloads.")
    )
    
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton(small_caps("🗑️ Remove"), callback_data="remove_thumb")],
        [InlineKeyboardButton(small_caps("⬅️ Back to Settings"), callback_data="back_to_settings")]
    ])
    
    await callback_query.message.edit_media(
        media=InputMediaPhoto(
            media=thumb,
            caption=text
        ),
        reply_markup=buttons
    )

@Client.on_callback_query(filters.regex("^remove_thumb$"))
async def remove_thumbnail(client: Client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    
    await db.remove_thumbnail(user_id)
    
    await callback_query.answer(small_caps("✅ Thumbnail removed!"), show_alert=False)
    
    await settings_cmd(client, callback_query.message)

@Client.on_callback_query(filters.regex("^back_to_settings$"))
async def back_to_settings(client: Client, callback_query: CallbackQuery):
    await settings_cmd(client, callback_query.message)

@Client.on_message(filters.command(["cancel"]))
async def send_cancel(client: Client, message: Message):
    batch_temp.IS_BATCH[message.from_user.id] = True
    cancel_text = script.CANCELLED.format(small_caps("TASK CANCELLED"))
    await message.reply_text(cancel_text, parse_mode=enums.ParseMode.HTML)

async def settings_panel(client, callback_query):
    user_id = callback_query.from_user.id
    is_premium = await db.check_premium(user_id)
    badge = small_caps("💎 Premium") if is_premium else small_caps("👤 Free User")
    
    thumb = await db.get_thumbnail(user_id)
    thumb_status = small_caps("✅ Active") if thumb else small_caps("❌ Not Set")
    
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton(small_caps("🖼️ Set Thumbnail"), callback_data="set_thumb")],
        [InlineKeyboardButton(small_caps("👁️ View Thumbnail"), callback_data="view_thumb")],
        [InlineKeyboardButton(small_caps("🗑️ Remove Thumbnail"), callback_data="remove_thumb")],
        [InlineKeyboardButton(small_caps("📊 My Stats"), callback_data="user_stats_btn")],
        [InlineKeyboardButton(small_caps("⬅️ Back to Home"), callback_data="start_btn")]
    ])
   
    text = script.SETTINGS_TXT.format(
        small_caps("⚙️ Settings Dashboard"),
        badge,
        small_caps("User ID:"),
        user_id,
        small_caps("Current Settings")
    ) + f"\n• {small_caps('Thumbnail:')} {thumb_status}"
   
    await callback_query.message.edit_caption(
        caption=text,
        reply_markup=buttons,
        parse_mode=enums.ParseMode.HTML
    )

@Client.on_message(filters.text & filters.private & ~filters.regex("^/"))
async def save(client: Client, message: Message):
    if "https://t.me/" in message.text:
       
        is_limit_reached = await db.check_limit(message.from_user.id)
        if is_limit_reached:
            btn = InlineKeyboardMarkup([[InlineKeyboardButton(small_caps("💎 Upgrade Premium"), callback_data="buy_premium")]])
            limit_text = script.LIMIT_REACHED.format(
                small_caps("DAILY LIMIT EXCEEDED"),
                small_caps("Your 10 free saves for today are used"),
                small_caps("Quota resets after 24 hours"),
                small_caps("Upgrade to Premium for Unlimited"),
                small_caps("Remove restrictions & enjoy seamless downloading")
            )
            return await message.reply_photo(
                photo=SUBSCRIPTION,
                caption=limit_text,
                reply_markup=btn,
                parse_mode=enums.ParseMode.HTML
            )
       
        if batch_temp.IS_BATCH.get(message.from_user.id) == False:
            process_text = script.PROCESSING.format(
                small_caps("PROCESSING"),
                small_caps("A task is currently processing"),
                small_caps("Please wait or use /cancel to stop")
            )
            return await message.reply_text(process_text, parse_mode=enums.ParseMode.HTML)
       
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
                login_text = script.LOGIN_REQUIRED.format(
                    small_caps("AUTHENTICATION REQUIRED"),
                    small_caps("Access requires login"),
                    small_caps("This is a private channel"),
                    small_caps("Use")
                )
                await message.reply(
                    login_text,
                    parse_mode=enums.ParseMode.HTML
                )
                batch_temp.IS_BATCH[message.from_user.id] = True
                return
           
            session_name = f"session_{message.from_user.id}_{msgid}_{int(time.time())}"
            acc = None
            try:
                acc = Client(
                    session_name,
                    session_string=user_data,
                    api_hash=API_HASH,
                    api_id=API_ID,
                    in_memory=True
                )
                await acc.connect()
                
                if is_private_link:
                    chatid = int("-100" + datas[4])
                    await handle_restricted_content(client, acc, message, chatid, msgid)
                elif is_batch:
                    username = datas[4]
                    await handle_restricted_content(client, acc, message, username, msgid)
                else:
                    username = datas[3]
                    await handle_restricted_content(client, acc, message, username, msgid)
               
            except Exception as e:
                logger.error(f"Session error: {e}")
            finally:
                if acc:
                    try:
                        await acc.disconnect()
                    except:
                        pass
           
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
            btn = InlineKeyboardMarkup([[InlineKeyboardButton(small_caps("💎 Upgrade Premium"), callback_data="buy_premium")]])
            size_text = script.SIZE_LIMIT.format(
                small_caps("FILE SIZE EXCEEDED"),
                small_caps("Free tier limited to"),
                small_caps("per file"),
                small_caps("Upgrade to Premium"),
                small_caps("Download files up to"),
                small_caps("with no limits")
            )
            await client.send_message(
                message.chat.id,
                size_text,
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
            cancel_text = script.CANCELLED.format(small_caps("TASK CANCELLED"))
            return await smsg.edit(cancel_text)
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
            final_caption = ""  # Empty caption
            if msg.caption:
                final_caption = msg.caption
       
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
   
    if data == "settings_btn":
        await settings_panel(client, callback_query)
   
    elif data == "buy_premium":
        buttons = [
            [InlineKeyboardButton(small_caps("📸 Send Proof"), url="https://t.me/xFlexyy")],
            [InlineKeyboardButton(small_caps("⬅️ Back to Home"), callback_data="start_btn")]
        ]
       
        premium_text = script.PREMIUM_TEXT.format(
            small_caps("PREMIUM MEMBERSHIP"),
            small_caps("Unlock Unlimited Power! ⚡"),
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
            small_caps("After Payment: Send Screenshot to @xFlexyy for Instant Activation!")
        )
       
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
        buttons = [[InlineKeyboardButton(small_caps("⬅️ Back to Home"), callback_data="start_btn")]]
        help_text = script.HELP_TXT.format(
            small_caps("HELP DESK"),
            small_caps("Comprehensive User Guide"),
            small_caps("Public Channels (No Login)"),
            small_caps("Forward or send post link directly"),
            small_caps("Compatible with any public channel/group"),
            small_caps("Example Link:"),
            small_caps("Private Channels (Login Required)"),
            small_caps("Use"),
            small_caps("to securely connect"),
            small_caps("Send private link (e.g.,"),
            small_caps("Bot accesses using your session"),
            small_caps("Batch Downloading Mode"),
            small_caps("Initiate with"),
            small_caps("for multiple files"),
            small_caps("Free User Limitations"),
            small_caps("Daily Quota:"),
            small_caps("Files / 24 Hours"),
            small_caps("File Size Cap:"),
            small_caps("Maximum"),
            small_caps("Premium Benefits"),
            small_caps("Unlimited Downloads • No Restrictions"),
            small_caps("Priority Support • Advanced Features")
        )
        await client.edit_message_caption(
            chat_id=message.chat.id,
            message_id=message.id,
            caption=help_text,
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=enums.ParseMode.HTML
        )
   
    elif data == "about_btn":
        buttons = [[InlineKeyboardButton(small_caps("⬅️ Back to Home"), callback_data="start_btn")]]
        about_text = script.ABOUT_TXT.format(
            small_caps("ABOUT SYSTEM"),
            small_caps("Bot Name:") + " <a href=http://t.me/THEUPDATEDGUYS_Bot>Save Content Pro</a>",
            small_caps("Developer:") + " <a href=https://t.me/xFlexyy>Flexyy</a>",
            small_caps("Library:") + " <a href='https://docs.pyrogram.org/'>Pyrogram Async</a>",
            small_caps("Language:") + " <a href='https://www.python.org/'>Python 3.11+</a>",
            small_caps("Database:") + " <a href='https://www.mongodb.com/'>MongoDB Atlas</a>",
            small_caps("Hosting:") + " Dedicated High-Speed VPS",
            small_caps("Powered by ᴅʀᴀɢᴏɴʙʏᴛᴇ ɴᴇᴛᴡᴏʀᴋ")
        )
        await client.edit_message_caption(
            chat_id=message.chat.id,
            message_id=message.id,
            caption=about_text,
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=enums.ParseMode.HTML
        )
   
    elif data == "start_btn":
        bot = await client.get_me()
        photo_url = get_random_premium_image()
       
        buttons = [
            [
                InlineKeyboardButton(small_caps("💎 Premium"), callback_data="buy_premium"),
                InlineKeyboardButton(small_caps("🆘 Help"), callback_data="help_btn")
            ],
            [
                InlineKeyboardButton(small_caps("⚙️ Settings"), callback_data="settings_btn"),
                InlineKeyboardButton(small_caps("ℹ️ About"), callback_data="about_btn")
            ]
        ]
       
        start_text = script.START_TXT.format(
            small_caps("WELCOME TO RESTRICTED SAVER"),
            small_caps(f"Hello {callback_query.from_user.first_name}, I'm {bot.first_name}"),
            small_caps("Your Ultimate Restricted Content Saver Bot"),
            small_caps("System Status: 🟢 Online"),
            small_caps("Performance: 10x High-Speed"),
            small_caps("Security: End-to-End Encrypted"),
            small_caps("Uptime: 99.9% Guaranteed"),
            small_caps("Select Option Below to Get Started")
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
   
    elif data == "user_stats_btn":
        await callback_query.answer(small_caps("📊 Coming Soon!"), show_alert=True)
   
    await callback_query.answer()