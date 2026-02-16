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
import datetime
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

# ==================== 🔥 SMALL CAPS FONT ====================
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

# ==================== 🔥 STATE MANAGEMENT ====================
class UserState:
    waiting_for_thumbnail = {}
    waiting_for_caption = {}
    waiting_for_del_word = {}
    waiting_for_repl_word_target = {}
    waiting_for_repl_word_replacement = {}
    waiting_for_dump_chat = {}

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

    # ==================== MAIN DASHBOARD ====================
    DASHBOARD_TXT = """
<b>{}</b>

<blockquote>
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ <b>👤 {}</b>        ┃
┃ <b>🆔 {}</b> <code>{}</code>     ┃
┃ <b>💎 {}</b> <code>{}</code>      ┃
┃ <b>📊 {}</b> <code>{}/{}</code>     ┃
┃ <b>📁 {}</b> <code>{}</code>     ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
</blockquote>

<b>📋 {}</b>

<blockquote>
┌─────────────────────────────────┐
│ <b>🖼️ {}</b> {}{}  │
│ <b>📝 {}</b> {}{}      │
│ <b>🗑️ {}</b> {}      │
│ <b>🔄 {}</b> {}  │
│ <b>📤 {}</b> {} │
└─────────────────────────────────┘
</blockquote>

<i>{}</i>
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

# ======================================================
# MAIN DASHBOARD FUNCTION
# ======================================================
async def show_dashboard(client: Client, message_or_callback, user_id: int, first_name: str, edit: bool = False):
    """Show main dashboard with all settings in one page"""
    
    # Get user data
    is_premium = await db.check_premium(user_id)
    premium_status = small_caps("✅ Premium") if is_premium else small_caps("❌ Free")
    
    # Get usage stats
    user_data = await db.col.find_one({'id': int(user_id)})
    daily_used = user_data.get('daily_usage', 0) if user_data else 0
    total_used = user_data.get('total_usage', 0) if user_data else 0
    
    # Get thumbnail status
    thumb = await db.get_thumbnail(user_id)
    thumb_status = "✅" if thumb else "❌"
    thumb_text = small_caps("Set") if thumb else small_caps("Not Set")
    
    # Get caption status
    caption = await db.get_caption(user_id)
    caption_status = "✅" if caption else "❌"
    caption_text = small_caps("Custom") if caption else small_caps("Default")
    
    # Get delete words
    delete_words = await db.get_delete_words(user_id)
    delete_count = len(delete_words)
    
    # Get replace words
    replace_words = await db.get_replace_words(user_id)
    replace_count = len(replace_words)
    
    # Get dump chat
    dump_chat = await db.get_dump_chat(user_id)
    dump_text = str(dump_chat) if dump_chat else small_caps("Not Set")
    
    # Format delete words preview
    if delete_words:
        words_preview = ", ".join(delete_words[:3])
        if len(delete_words) > 3:
            words_preview += f"... (+{len(delete_words)-3})"
        delete_preview = f"{delete_count} ({words_preview})"
    else:
        delete_preview = small_caps("None")
    
    # Format replace words preview
    if replace_words:
        repl_list = [f"{k}→{v}" for k, v in list(replace_words.items())[:2]]
        repl_preview = ", ".join(repl_list)
        if len(replace_words) > 2:
            repl_preview += f"... (+{len(replace_words)-2})"
        replace_preview = f"{replace_count} ({repl_preview})"
    else:
        replace_preview = small_caps("None")
    
    # Create dashboard text
    dashboard_text = script.DASHBOARD_TXT.format(
        small_caps("⚙️ MASTER CONTROL DASHBOARD"),
        small_caps("Account:"),
        small_caps("User ID:"),
        user_id,
        small_caps("Status:"),
        premium_status,
        small_caps("Today's Usage:"),
        daily_used,
        FREE_LIMIT_DAILY,
        small_caps("Total Saves:"),
        total_used,
        small_caps("CURRENT CONFIGURATION"),
        small_caps("Thumbnail:"),
        thumb_status,
        thumb_text,
        small_caps("Caption:"),
        caption_status,
        caption_text,
        small_caps("Delete Words:"),
        delete_preview,
        small_caps("Replace Rules:"),
        replace_preview,
        small_caps("Dump Chat:"),
        dump_text,
        small_caps("Select an option below to customize your experience")
    )
    
    # Create main keyboard
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton(small_caps("🖼️ THUMBNAIL SETTINGS"), callback_data="thumb_menu")],
        [
            InlineKeyboardButton(small_caps("📝 CAPTION"), callback_data="caption_menu"),
            InlineKeyboardButton(small_caps("🗑️ DUMP CHAT"), callback_data="dump_menu")
        ],
        [InlineKeyboardButton(small_caps("🔤 WORD FILTERS"), callback_data="word_menu")],
        [
            InlineKeyboardButton(small_caps("📊 STATS"), callback_data="stats_view"),
            InlineKeyboardButton(small_caps("💎 PREMIUM"), callback_data="buy_premium")
        ],
        [
            InlineKeyboardButton(small_caps("🏠 HOME"), callback_data="start_btn"),
            InlineKeyboardButton(small_caps("❌ CLOSE"), callback_data="close_btn")
        ]
    ])
    
    photo_url = get_random_premium_image()
    
    if edit:
        # Edit existing message
        if hasattr(message_or_callback, 'message'):
            # It's a callback query
            await message_or_callback.message.edit_media(
                media=InputMediaPhoto(
                    media=photo_url,
                    caption=dashboard_text
                ),
                reply_markup=buttons
            )
        else:
            # It's a message
            await message_or_callback.edit_media(
                media=InputMediaPhoto(
                    media=photo_url,
                    caption=dashboard_text
                ),
                reply_markup=buttons
            )
    else:
        # Send new message
        if hasattr(message_or_callback, 'message'):
            # It's a callback query with message
            await message_or_callback.message.reply_photo(
                photo=photo_url,
                caption=dashboard_text,
                reply_markup=buttons,
                parse_mode=enums.ParseMode.HTML
            )
        else:
            # It's a direct message
            await message_or_callback.reply_photo(
                photo=photo_url,
                caption=dashboard_text,
                reply_markup=buttons,
                parse_mode=enums.ParseMode.HTML
            )

# ======================================================
# START COMMAND
# ======================================================
@Client.on_message(filters.command(["start"]) & filters.private)
async def send_start(client: Client, message: Message):
    user_id = message.from_user.id
    
    if not await db.is_user_exist(user_id):
        await db.add_user(user_id, message.from_user.first_name)
   
    try:
        await message.react(emoji=random.choice(REACTIONS), big=True)
    except:
        pass
    
    await show_dashboard(client, message, user_id, message.from_user.first_name, edit=False)

# ======================================================
# HELP COMMAND
# ======================================================
@Client.on_message(filters.command(["help"]) & filters.private)
async def send_help(client: Client, message: Message):
    buttons = [[InlineKeyboardButton(small_caps("⬅️ Back to Dashboard"), callback_data="start_btn")]]
    
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
    
    await message.reply_photo(
        photo=get_random_premium_image(),
        caption=help_text,
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode=enums.ParseMode.HTML
    )

# ======================================================
# PREMIUM COMMAND
# ======================================================
@Client.on_message(filters.command(["plan", "myplan", "premium"]) & filters.private)
async def send_plan(client: Client, message: Message):
    buttons = [
        [InlineKeyboardButton(small_caps("📸 Send Proof"), url="https://t.me/xFlexyy")],
        [InlineKeyboardButton(small_caps("⬅️ Back to Dashboard"), callback_data="start_btn")]
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
   
    await message.reply_photo(
        photo=SUBSCRIPTION,
        caption=premium_text,
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode=enums.ParseMode.HTML
    )

# ======================================================
# CANCEL COMMAND
# ======================================================
@Client.on_message(filters.command(["cancel"]) & filters.private)
async def send_cancel(client: Client, message: Message):
    user_id = message.from_user.id
    batch_temp.IS_BATCH[user_id] = True
    
    # Clear any waiting states
    for state_dict in [UserState.waiting_for_thumbnail, UserState.waiting_for_caption,
                       UserState.waiting_for_del_word, UserState.waiting_for_repl_word_target,
                       UserState.waiting_for_repl_word_replacement, UserState.waiting_for_dump_chat]:
        if user_id in state_dict:
            del state_dict[user_id]
    
    cancel_text = script.CANCELLED.format(small_caps("TASK CANCELLED"))
    await message.reply_text(cancel_text, parse_mode=enums.ParseMode.HTML)

# ======================================================
# THUMBNAIL MENU
# ======================================================
async def show_thumb_menu(client: Client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    thumb = await db.get_thumbnail(user_id)
    
    if thumb:
        status = small_caps("✅ Active")
    else:
        status = small_caps("❌ Not Set")
    
    text = f"""
<b>{small_caps('🖼️ Thumbnail Settings')}</b>

<blockquote>
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ <b>{small_caps('Current Status')}:</b> {status}           ┃
┃                              ┃
┃ <b>{small_caps('Set')}:</b> {small_caps('Reply to any photo with')}  ┃
┃      <code>/set_thumb</code> {small_caps('or click button below')} ┃
┃                              ┃
┃ <b>{small_caps('View')}:</b> {small_caps('See your current thumbnail')} ┃
┃ <b>{small_caps('Delete')}:</b> {small_caps('Remove custom thumbnail')} ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
</blockquote>
"""
    
    buttons = []
    if thumb:
        buttons.append([
            InlineKeyboardButton(small_caps("👁️ View"), callback_data="view_thumb"),
            InlineKeyboardButton(small_caps("🗑️ Delete"), callback_data="remove_thumb")
        ])
    
    buttons.append([InlineKeyboardButton(small_caps("🖼️ Set New"), callback_data="set_thumb_prompt")])
    buttons.append([InlineKeyboardButton(small_caps("⬅️ Back to Dashboard"), callback_data="start_btn")])
    
    await callback_query.message.edit_media(
        media=InputMediaPhoto(
            media=get_random_premium_image(),
            caption=text
        ),
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# ======================================================
# CAPTION MENU
# ======================================================
async def show_caption_menu(client: Client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    caption = await db.get_caption(user_id)
    
    if caption:
        preview = caption.format(filename="video.mp4", size="1.2 GB")
        status = small_caps("✅ Custom")
        caption_preview = f"<code>{caption}</code>\n\n<b>{small_caps('Preview')}:</b>\n{preview}"
    else:
        status = small_caps("❌ Default")
        caption_preview = small_caps("No custom caption set")
    
    text = f"""
<b>{small_caps('📝 Caption Settings')}</b>

<blockquote>
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ <b>{small_caps('Current Status')}:</b> {status}           ┃
┃                              ┃
┃ <b>{small_caps('Current Caption')}:</b>                    ┃
┃ {caption_preview} ┃
┃                              ┃
┃ <b>{small_caps('Placeholders')}:</b>                         ┃
┃ • <code>{{filename}}</code> - {small_caps('File name')}        ┃
┃ • <code>{{size}}</code> - {small_caps('File size')}          ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
</blockquote>
"""
    
    buttons = [
        [InlineKeyboardButton(small_caps("✏️ Set Caption"), callback_data="set_caption_prompt")],
        [InlineKeyboardButton(small_caps("⬅️ Back to Dashboard"), callback_data="start_btn")]
    ]
    
    if caption:
        buttons.insert(0, [InlineKeyboardButton(small_caps("🗑️ Delete"), callback_data="del_caption")])
    
    await callback_query.message.edit_media(
        media=InputMediaPhoto(
            media=get_random_premium_image(),
            caption=text
        ),
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# ======================================================
# WORD FILTER MENU
# ======================================================
async def show_word_menu(client: Client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    
    delete_words = await db.get_delete_words(user_id)
    replace_words = await db.get_replace_words(user_id)
    
    delete_text = "• " + "\n• ".join(delete_words) if delete_words else small_caps("• None")
    
    replace_text = ""
    if replace_words:
        for target, replacement in replace_words.items():
            replace_text += f"• <code>{target}</code> → <code>{replacement}</code>\n"
    else:
        replace_text = small_caps("• None")
    
    text = f"""
<b>{small_caps('🔤 Word Filter Settings')}</b>

<blockquote>
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ <b>🗑️ {small_caps('Delete Words')}:</b>                 ┃
{delete_text}
┃                              ┃
┃ <b>🔄 {small_caps('Replace Rules')}:</b>                ┃
{replace_text}
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

<b>{small_caps('Commands')}:</b>
• <code>/set_del_word word1 word2</code>
• <code>/rem_del_word word1</code>
• <code>/set_repl_word target replacement</code>
• <code>/rem_repl_word target</code>
</blockquote>
"""
    
    buttons = [
        [
            InlineKeyboardButton(small_caps("➕ Add Delete"), callback_data="add_del_prompt"),
            InlineKeyboardButton(small_caps("🗑️ Rem Delete"), callback_data="rem_del_prompt")
        ],
        [
            InlineKeyboardButton(small_caps("➕ Add Replace"), callback_data="add_repl_prompt"),
            InlineKeyboardButton(small_caps("🗑️ Rem Replace"), callback_data="rem_repl_prompt")
        ],
        [InlineKeyboardButton(small_caps("⬅️ Back to Dashboard"), callback_data="start_btn")]
    ]
    
    await callback_query.message.edit_media(
        media=InputMediaPhoto(
            media=get_random_premium_image(),
            caption=text
        ),
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# ======================================================
# DUMP CHAT MENU
# ======================================================
async def show_dump_menu(client: Client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    dump_chat = await db.get_dump_chat(user_id)
    
    if dump_chat:
        try:
            chat = await client.get_chat(dump_chat)
            title = chat.title or small_caps("Private Chat")
            status = small_caps(f"✅ {dump_chat}")
        except:
            title = small_caps("Inaccessible")
            status = small_caps(f"⚠️ {dump_chat}")
    else:
        status = small_caps("❌ Not Set")
        title = small_caps("N/A")
    
    text = f"""
<b>{small_caps('🗑️ Dump Chat Settings')}</b>

<blockquote>
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ <b>{small_caps('Current Status')}:</b> {status}      ┃
┃ <b>{small_caps('Chat Title')}:</b> {title}              ┃
┃                              ┃
┃ <b>{small_caps('Set')}:</b> <code>/setchat &lt;chat_id&gt;</code>     ┃
┃ <b>{small_caps('Clear')}:</b> <code>/setchat clear</code>         ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
</blockquote>
"""
    
    buttons = [
        [InlineKeyboardButton(small_caps("✏️ Set New"), callback_data="set_dump_prompt")],
        [InlineKeyboardButton(small_caps("⬅️ Back to Dashboard"), callback_data="start_btn")]
    ]
    
    if dump_chat:
        buttons.insert(0, [InlineKeyboardButton(small_caps("🗑️ Clear"), callback_data="clear_dump")])
    
    await callback_query.message.edit_media(
        media=InputMediaPhoto(
            media=get_random_premium_image(),
            caption=text
        ),
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# ======================================================
# STATS VIEW
# ======================================================
async def show_stats(client: Client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    
    user_data = await db.col.find_one({'id': int(user_id)})
    is_premium = await db.check_premium(user_id)
    
    daily_used = user_data.get('daily_usage', 0) if user_data else 0
    total_used = user_data.get('total_usage', 0) if user_data else 0
    joined = user_data.get('joined_date', datetime.datetime.now()) if user_data else datetime.datetime.now()
    
    if isinstance(joined, str):
        try:
            joined = datetime.datetime.fromisoformat(joined)
        except:
            joined = datetime.datetime.now()
    
    if is_premium:
        limit_text = small_caps("♾️ Unlimited")
        usage_text = small_caps("Ignored (Premium)")
    else:
        limit_text = f"10 {small_caps('Files / 24h')}"
        usage_text = f"{daily_used} / 10"
    
    text = f"""
<b>{small_caps('📊 Your Statistics')}</b>

<blockquote>
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ <b>👤 {small_caps('User ID')}:</b> <code>{user_id}</code>         ┃
┃ <b>💎 {small_caps('Plan')}:</b> {'✅ Premium' if is_premium else '❌ Free'}        ┃
┃ <b>📅 {small_caps('Joined')}:</b> {joined.strftime('%Y-%m-%d') if hasattr(joined, 'strftime') else joined}        ┃
┃ <b>📊 {small_caps('Total Saves')}:</b> {total_used}                ┃
┃ <b>⚡ {small_caps('Daily Limit')}:</b> {limit_text}    ┃
┃ <b>📈 {small_caps("Today's Usage")}:</b> {usage_text}        ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
</blockquote>
"""
    
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton(small_caps("⬅️ Back to Dashboard"), callback_data="start_btn")]
    ])
    
    await callback_query.message.edit_media(
        media=InputMediaPhoto(
            media=get_random_premium_image(),
            caption=text
        ),
        reply_markup=buttons
    )

# ======================================================
# CALLBACK HANDLERS
# ======================================================
@Client.on_callback_query()
async def button_callbacks(client: Client, callback_query: CallbackQuery):
    data = callback_query.data
    user_id = callback_query.from_user.id
    message = callback_query.message
    
    if not message:
        return
    
    # ===== MAIN NAVIGATION =====
    if data == "start_btn":
        await show_dashboard(client, callback_query, user_id, callback_query.from_user.first_name, edit=True)
    
    elif data == "close_btn":
        await message.delete()
        await callback_query.answer()
        return
    
    # ===== THUMBNAIL MENU =====
    elif data == "thumb_menu":
        await show_thumb_menu(client, callback_query)
    
    elif data == "set_thumb_prompt":
        UserState.waiting_for_thumbnail[user_id] = True
        text = f"""
<b>{small_caps('🖼️ Set Custom Thumbnail')}</b>

<blockquote>
<i>{small_caps('Please send me a photo to use as your custom thumbnail')}.</i>
<i>{small_caps('This will appear on all your downloaded videos')}.</i>
</blockquote>
"""
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton(small_caps("❌ Cancel"), callback_data="cancel_thumb")]
        ])
        await message.edit_media(
            media=InputMediaPhoto(
                media=get_random_premium_image(),
                caption=text
            ),
            reply_markup=buttons
        )
    
    elif data == "cancel_thumb":
        if user_id in UserState.waiting_for_thumbnail:
            del UserState.waiting_for_thumbnail[user_id]
        await callback_query.answer(small_caps("❌ Cancelled"), show_alert=False)
        await show_thumb_menu(client, callback_query)
    
    elif data == "view_thumb":
        thumb = await db.get_thumbnail(user_id)
        if thumb:
            await message.edit_media(
                media=InputMediaPhoto(
                    media=thumb,
                    caption=f"<b>{small_caps('🖼️ Your Current Thumbnail')}</b>"
                ),
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(small_caps("⬅️ Back"), callback_data="thumb_menu")]
                ])
            )
        else:
            await callback_query.answer(small_caps("❌ No thumbnail set!"), show_alert=True)
    
    elif data == "remove_thumb":
        await db.del_thumbnail(user_id)
        await callback_query.answer(small_caps("✅ Thumbnail removed!"), show_alert=False)
        await show_thumb_menu(client, callback_query)
    
    # ===== CAPTION MENU =====
    elif data == "caption_menu":
        await show_caption_menu(client, callback_query)
    
    elif data == "set_caption_prompt":
        UserState.waiting_for_caption[user_id] = True
        text = f"""
<b>{small_caps('📝 Set Custom Caption')}</b>

<blockquote>
<i>{small_caps('Send me the caption you want to use')}.</i>
<i>{small_caps('Use {filename} and {size} as placeholders')}.</i>

<b>{small_caps('Example')}:</b>
<code>Downloaded: {{filename}} Size: {{size}}</code>
</blockquote>
"""
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton(small_caps("❌ Cancel"), callback_data="cancel_caption")]
        ])
        await message.edit_media(
            media=InputMediaPhoto(
                media=get_random_premium_image(),
                caption=text
            ),
            reply_markup=buttons
        )
    
    elif data == "cancel_caption":
        if user_id in UserState.waiting_for_caption:
            del UserState.waiting_for_caption[user_id]
        await callback_query.answer(small_caps("❌ Cancelled"), show_alert=False)
        await show_caption_menu(client, callback_query)
    
    elif data == "del_caption":
        await db.del_caption(user_id)
        await callback_query.answer(small_caps("✅ Caption deleted!"), show_alert=False)
        await show_caption_menu(client, callback_query)
    
    # ===== WORD FILTER MENU =====
    elif data == "word_menu":
        await show_word_menu(client, callback_query)
    
    elif data == "add_del_prompt":
        UserState.waiting_for_del_word[user_id] = True
        text = f"""
<b>{small_caps('➕ Add Delete Words')}</b>

<blockquote>
<i>{small_caps('Send me the words you want to delete')}.</i>
<i>{small_caps('Separate multiple words with spaces')}.</i>

<b>{small_caps('Example')}:</b>
<code>spoiler nsfw @spam</code>
</blockquote>
"""
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton(small_caps("❌ Cancel"), callback_data="cancel_word")]
        ])
        await message.edit_media(
            media=InputMediaPhoto(
                media=get_random_premium_image(),
                caption=text
            ),
            reply_markup=buttons
        )
    
    elif data == "rem_del_prompt":
        delete_words = await db.get_delete_words(user_id)
        if not delete_words:
            await callback_query.answer(small_caps("❌ No words to remove!"), show_alert=True)
            return
        
        UserState.waiting_for_del_word[user_id] = True
        word_list = "\n• ".join(delete_words)
        text = f"""
<b>{small_caps('🗑️ Remove Delete Words')}</b>

<blockquote>
<b>{small_caps('Current Words')}:</b>
• {word_list}

<i>{small_caps('Send me the words you want to remove')}.</i>
<i>{small_caps('Separate multiple words with spaces')}.</i>
</blockquote>
"""
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton(small_caps("❌ Cancel"), callback_data="cancel_word")]
        ])
        await message.edit_media(
            media=InputMediaPhoto(
                media=get_random_premium_image(),
                caption=text
            ),
            reply_markup=buttons
        )
    
    elif data == "add_repl_prompt":
        UserState.waiting_for_repl_word_target[user_id] = True
        text = f"""
<b>{small_caps('➕ Add Replace Rule - Step 1')}</b>

<blockquote>
<i>{small_caps('Send me the TARGET word/phrase to replace')}.</i>

<b>{small_caps('Example')}:</b>
<code>@OldChannel</code>
</blockquote>
"""
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton(small_caps("❌ Cancel"), callback_data="cancel_word")]
        ])
        await message.edit_media(
            media=InputMediaPhoto(
                media=get_random_premium_image(),
                caption=text
            ),
            reply_markup=buttons
        )
    
    elif data == "rem_repl_prompt":
        replace_words = await db.get_replace_words(user_id)
        if not replace_words:
            await callback_query.answer(small_caps("❌ No rules to remove!"), show_alert=True)
            return
        
        UserState.waiting_for_repl_word_target[user_id] = True
        rule_list = ""
        for target, replacement in replace_words.items():
            rule_list += f"• <code>{target}</code> → <code>{replacement}</code>\n"
        
        text = f"""
<b>{small_caps('🗑️ Remove Replace Rules')}</b>

<blockquote>
<b>{small_caps('Current Rules')}:</b>
{rule_list}

<i>{small_caps('Send me the TARGET word to remove')}.</i>
</blockquote>
"""
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton(small_caps("❌ Cancel"), callback_data="cancel_word")]
        ])
        await message.edit_media(
            media=InputMediaPhoto(
                media=get_random_premium_image(),
                caption=text
            ),
            reply_markup=buttons
        )
    
    elif data == "cancel_word":
        for state in [UserState.waiting_for_del_word, UserState.waiting_for_repl_word_target,
                      UserState.waiting_for_repl_word_replacement]:
            if user_id in state:
                del state[user_id]
        await callback_query.answer(small_caps("❌ Cancelled"), show_alert=False)
        await show_word_menu(client, callback_query)
    
    # ===== DUMP CHAT MENU =====
    elif data == "dump_menu":
        await show_dump_menu(client, callback_query)
    
    elif data == "set_dump_prompt":
        UserState.waiting_for_dump_chat[user_id] = True
        text = f"""
<b>{small_caps('🗑️ Set Dump Chat')}</b>

<blockquote>
<i>{small_caps('Send me the Chat ID where files should be forwarded')}.</i>

<b>{small_caps('Example')}:</b>
<code>-1001234567890</code>

<i>{small_caps('Send')} <code>clear</code> {small_caps('to remove')}</i>
</blockquote>
"""
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton(small_caps("❌ Cancel"), callback_data="cancel_dump")]
        ])
        await message.edit_media(
            media=InputMediaPhoto(
                media=get_random_premium_image(),
                caption=text
            ),
            reply_markup=buttons
        )
    
    elif data == "cancel_dump":
        if user_id in UserState.waiting_for_dump_chat:
            del UserState.waiting_for_dump_chat[user_id]
        await callback_query.answer(small_caps("❌ Cancelled"), show_alert=False)
        await show_dump_menu(client, callback_query)
    
    elif data == "clear_dump":
        await db.set_dump_chat(user_id, None)
        await callback_query.answer(small_caps("✅ Dump chat cleared!"), show_alert=False)
        await show_dump_menu(client, callback_query)
    
    # ===== STATS VIEW =====
    elif data == "stats_view":
        await show_stats(client, callback_query)
    
    # ===== OTHER =====
    elif data == "buy_premium":
        buttons = [
            [InlineKeyboardButton(small_caps("📸 Send Proof"), url="https://t.me/xFlexyy")],
            [InlineKeyboardButton(small_caps("⬅️ Back to Dashboard"), callback_data="start_btn")]
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
       
        await message.edit_media(
            media=InputMediaPhoto(
                media=SUBSCRIPTION,
                caption=premium_text
            ),
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    
    elif data == "help_btn":
        buttons = [[InlineKeyboardButton(small_caps("⬅️ Back to Dashboard"), callback_data="start_btn")]]
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
        await message.edit_media(
            media=InputMediaPhoto(
                media=get_random_premium_image(),
                caption=help_text
            ),
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    
    elif data == "about_btn":
        buttons = [[InlineKeyboardButton(small_caps("⬅️ Back to Dashboard"), callback_data="start_btn")]]
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
        await message.edit_media(
            media=InputMediaPhoto(
                media=get_random_premium_image(),
                caption=about_text
            ),
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    
    await callback_query.answer()

# ======================================================
# MESSAGE HANDLERS FOR USER INPUT
# ======================================================

@Client.on_message(filters.photo & filters.private)
async def receive_thumbnail(client: Client, message: Message):
    user_id = message.from_user.id
    
    if user_id in UserState.waiting_for_thumbnail:
        file_id = message.photo[-1].file_id
        await db.set_thumbnail(user_id, file_id)
        del UserState.waiting_for_thumbnail[user_id]
        
        await message.reply_photo(
            photo=file_id,
            caption=f"<b>{small_caps('✅ Thumbnail Set Successfully!')}</b>",
            parse_mode=enums.ParseMode.HTML
        )
        await show_dashboard(client, message, user_id, message.from_user.first_name, edit=False)
        return

@Client.on_message(filters.text & filters.private & ~filters.regex("^/"))
async def receive_text_input(client: Client, message: Message):
    user_id = message.from_user.id
    text = message.text.strip()
    
    # Caption input
    if user_id in UserState.waiting_for_caption:
        await db.set_caption(user_id, text)
        del UserState.waiting_for_caption[user_id]
        await message.reply_text(f"<b>{small_caps('✅ Caption Set Successfully!')}</b>", parse_mode=enums.ParseMode.HTML)
        await show_dashboard(client, message, user_id, message.from_user.first_name, edit=False)
        return
    
    # Delete words input
    if user_id in UserState.waiting_for_del_word:
        words = text.split()
        await db.set_delete_words(user_id, words)
        del UserState.waiting_for_del_word[user_id]
        await message.reply_text(f"<b>{small_caps('✅ Words Added to Delete List!')}</b>", parse_mode=enums.ParseMode.HTML)
        await show_dashboard(client, message, user_id, message.from_user.first_name, edit=False)
        return
    
    # Replace word target input
    if user_id in UserState.waiting_for_repl_word_target:
        UserState.waiting_for_repl_word_replacement[user_id] = text
        del UserState.waiting_for_repl_word_target[user_id]
        await message.reply_text(
            f"<b>{small_caps('➕ Add Replace Rule - Step 2')}</b>\n\n"
            f"<i>{small_caps('Now send the REPLACEMENT word/phrase')}.</i>",
            parse_mode=enums.ParseMode.HTML
        )
        return
    
    # Replace word replacement input
    if user_id in UserState.waiting_for_repl_word_replacement:
        target = UserState.waiting_for_repl_word_replacement.pop(user_id)
        replacement = text
        await db.set_replace_words(user_id, {target: replacement})
        await message.reply_text(f"<b>{small_caps('✅ Replace Rule Added!')}</b>", parse_mode=enums.ParseMode.HTML)
        await show_dashboard(client, message, user_id, message.from_user.first_name, edit=False)
        return
    
    # Dump chat input
    if user_id in UserState.waiting_for_dump_chat:
        if text.lower() == "clear":
            await db.set_dump_chat(user_id, None)
            await message.reply_text(f"<b>{small_caps('✅ Dump Chat Cleared!')}</b>", parse_mode=enums.ParseMode.HTML)
        else:
            try:
                chat_id = int(text)
                await db.set_dump_chat(user_id, chat_id)
                await message.reply_text(f"<b>{small_caps('✅ Dump Chat Set Successfully!')}</b>", parse_mode=enums.ParseMode.HTML)
            except ValueError:
                await message.reply_text(f"<b>{small_caps('❌ Invalid Chat ID!')}</b>", parse_mode=enums.ParseMode.HTML)
        
        del UserState.waiting_for_dump_chat[user_id]
        await show_dashboard(client, message, user_id, message.from_user.first_name, edit=False)
        return

# ======================================================
# SAVE FUNCTION - HANDLES TELEGRAM LINKS
# ======================================================
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
           
            # FIXED: Better session management with unique names
            session_name = f"session_{message.from_user.id}_{msgid}_{int(time.time())}"
            acc = None
            try:
                # Create new client
                acc = Client(
                    session_name,
                    session_string=user_data,
                    api_hash=API_HASH,
                    api_id=API_ID,
                    in_memory=True
                )
                
                # Connect
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
                # Always disconnect
                if acc:
                    try:
                        if hasattr(acc, 'is_connected') and acc.is_connected:
                            await acc.disconnect()
                    except:
                        pass
                    # Clean up
                    try:
                        await acc.storage.save()
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
       
        # Apply word filters to caption
        final_caption = ""
        if msg.caption:
            final_caption = msg.caption
            
            # Apply delete words
            delete_words = await db.get_delete_words(message.from_user.id)
            for word in delete_words:
                final_caption = final_caption.replace(word, "")
            
            # Apply replace words
            replace_words = await db.get_replace_words(message.from_user.id)
            for target, replacement in replace_words.items():
                final_caption = final_caption.replace(target, replacement)
        
        # Apply custom caption if set
        custom_caption = await db.get_caption(message.from_user.id)
        if custom_caption:
            final_caption = custom_caption.format(
                filename=file.split("/")[-1] if file else "video.mp4",
                size=humanbytes(file_size)
            )
       
        if msg_type == "Document":
            await client.send_document(message.chat.id, file, thumb=ph_path, caption=final_caption, progress=progress, progress_args=[message, "up"])
        elif msg_type == "Video":
            await client.send_video(message.chat.id, file, duration=msg.video.duration, width=msg.video.width, height=msg.video.height, thumb=ph_path, caption=final_caption, progress=progress, progress_args=[message, "up"])
        elif msg_type == "Audio":
            await client.send_audio(message.chat.id, file, thumb=ph_path, caption=final_caption, progress=progress, progress_args=[message, "up"])
        elif msg_type == "Photo":
            await client.send_photo(message.chat.id, file, caption=final_caption)
       
        # Forward to dump chat if set
        dump_chat = await db.get_dump_chat(message.from_user.id)
        if dump_chat:
            try:
                if msg_type == "Document":
                    await client.send_document(dump_chat, file, thumb=ph_path, caption=final_caption)
                elif msg_type == "Video":
                    await client.send_video(dump_chat, file, thumb=ph_path, caption=final_caption)
                elif msg_type == "Audio":
                    await client.send_audio(dump_chat, file, thumb=ph_path, caption=final_caption)
                elif msg_type == "Photo":
                    await client.send_photo(dump_chat, file, caption=final_caption)
            except Exception as e:
                logger.error(f"Failed to forward to dump chat: {e}")
       
    except Exception as e:
         await smsg.edit(f"Upload Failed: {e}")
   
    if os.path.exists(f'{message.id}upstatus.txt'): os.remove(f'{message.id}upstatus.txt')
    if os.path.exists(temp_dir): shutil.rmtree(temp_dir)
    await client.delete_messages(message.chat.id, [smsg.id])