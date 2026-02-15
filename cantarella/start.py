# Developed by: LastPerson07 × cantarella
# Modified by: Flexyy Joren
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

# Premium Images - Aapki Di Hui List
PREMIUM_IMAGES = [
    "https://i.postimg.cc/JnY5fHyX/026736497b6d047c910a0da13bd23e7b.jpg",
    "https://i.postimg.cc/rmZNBRdt/23c874004ccca79fdd3fbcb260a80829.jpg",
    "https://i.postimg.cc/LXQ3cgqY/2412165f7ca24a6422b4bdb96d169e98.jpg",
    "https://i.postimg.cc/xCp3wNkx/3511407df15923bbc85720e712cec44e.jpg",
    "https://i.postimg.cc/DZpP94WP/45b4da77420ccfff9ab8196944c8cf26.jpg",
    "https://i.postimg.cc/gJtHCLwV/57e045c8b5bba2adfa522f15d6bd9094.jpg",
    "https://i.postimg.cc/hjt0Z1GV/72702cbdbf3bf0ceeac3ef6d7f0c118b.jpg",
    "https://i.postimg.cc/zB2FsHLk/7926a8d03b5c9094761a7ca17202e356.jpg",
    "https://i.postimg.cc/85Xm2fFY/82c3c50baee7980a9ae08c017bb669e6.jpg",
    "https://i.postimg.cc/85Xm2fFB/b16da8b99a83d33ad649c48210b4f42d.jpg",
    "https://i.postimg.cc/vB2tJx13/ba221a265c809c0ce3f3a83a2735d2bc.jpg",
    "https://i.postimg.cc/fLqfGS39/dbffd4c10a7db8b310f760bc4f5d5427.jpg",
    "https://i.postimg.cc/xCp3wNk6/e8b74238880bd9d67ec728cff79415e0.jpg"
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

def small_caps(text: str) -> str:
    """Convert text to small caps unicode (premium font)"""
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

def get_random_premium_image() -> str:
    """Return a random premium image from the list"""
    return random.choice(PREMIUM_IMAGES)

class script(object):
   
    START_TXT = """<b>{}</b>

<b>{}</b>
<i>{}</i>

<blockquote><b>🚀 {}</b>
<b>⚡ {}</b>
<b>🔐 {}</b>
<b>📊 {}</b></blockquote>

<b>👇 {}:</b>
""".format(
    small_caps("✨ Welcome to Restricted Saver Bot! ✨"),
    small_caps("Hello {}, I'm").format("{}") + " <a href=https://t.me/{}>{}</a>".format("{}", "{}"),
    small_caps("Your Professional Restricted Content Saver Bot"),
    small_caps("System Status: 🟢 Online"),
    small_caps("Performance: 10x High-Speed Processing"),
    small_caps("Security: End-to-End Encrypted"),
    small_caps("Uptime: 99.9% Guaranteed"),
    small_caps("Select an Option Below to Get Started")
)

    HELP_TXT = """<b>{}</b>

<blockquote><b>1️⃣ {}</b></blockquote>
• {}
• {}
• <i>{}</i> <code>https://t.me/channel/123</code>

<blockquote><b>2️⃣ {}</b></blockquote>
• {} <code>/login</code> {}
• {} <code>t.me/c/123...</code>
• {}

<blockquote><b>3️⃣ {}</b></blockquote>
• {} <code>/batch</code>
• {}

<blockquote><b>🛑 {}:</b></blockquote>
• <b>{}</b> 10 {}
• <b>{}</b> 2GB {}

<blockquote><b>💎 {}:</b></blockquote>
• {}
• {}
""".format(
    small_caps("📚 Comprehensive Help & User Guide"),
    small_caps("Public Channels (No Login Required)"),
    small_caps("Forward or send the post link directly"),
    small_caps("Compatible with any public channel or group"),
    small_caps("Example Link:"),
    small_caps("Private/Restricted Channels (Login Required)"),
    small_caps("Use"),
    small_caps("to securely connect your Telegram account"),
    small_caps("Send the private link (e.g.,"),
    small_caps("Bot accesses content using your authenticated session"),
    small_caps("Batch Downloading Mode"),
    small_caps("Initiate with"),
    small_caps("for multiple files"),
    small_caps("Free User Limitations"),
    small_caps("Daily Quota:"),
    small_caps("Files / 24 Hours"),
    small_caps("File Size Cap:"),
    small_caps("Maximum"),
    small_caps("Premium Membership Benefits"),
    small_caps("Unlimited Downloads & No Restrictions"),
    small_caps("Priority Support & Advanced Features")
)

    ABOUT_TXT = """<b>{}</b>

<blockquote><b>╭────[ 🧩 {} ]────⍟</b>
<b>├⍟ 🤖 {} : <a href=http://t.me/THEUPDATEDGUYS_Bot>{}</a></b>
<b>├⍟ 👨‍💻 {} : <a href=https://t.me/DmOwner>Ⓜ️ark X cantarella × Flexyy</a></b>
<b>├⍟ 📚 {} : <a href='https://docs.pyrogram.org/'>{}</a></b>
<b>├⍟ 🐍 {} : <a href='https://www.python.org/'>{}</a></b>
<b>├⍟ 🗄 {} : <a href='https://www.mongodb.com/'>{}</a></b>
<b>├⍟ 📡 {} : {}</b>
<b>╰───────────────⍟</b></blockquote>
""".format(
    small_caps("ℹ️ About This Bot"),
    small_caps("Technical Stack"),
    small_caps("Bot Name"),
    small_caps("Save Content"),
    small_caps("Developer"),
    small_caps("Pyrogram Async"),
    small_caps("Language"),
    small_caps("Python 3.11+"),
    small_caps("Database"),
    small_caps("MongoDB Atlas Cluster"),
    small_caps("Hosting"),
    small_caps("Dedicated High-Speed VPS")
)

    PREMIUM_TEXT = """<b>{}</b>
<b>{}</b>

<blockquote><b>✨ {}:</b>
<b>♾️ {}</b>
<b>📂 {} 4GB+ {}</b>
<b>⚡ {} ({})</b>
<b>🖼 {}</b>
<b>📝 {}</b>
<b>🛂 24/7 {}</b></blockquote>

<blockquote><b>💳 {}:</b></blockquote>
• <b>1 {}:</b> ₹50 / $1 ({})
• <b>3 {}:</b> ₹120 / $2.5 ({} 20%)
• <b>{}:</b> ₹200 / $4 ({}-{})

<blockquote><b>👇 {}:</b></blockquote>
<b>💸 UPI ID:</b> <code>{}</code>
<b>📸 QR Code:</b> <a href='{}'>{}</a>

<i>{}: {} {}</i>
""".format(
    small_caps("💎 Premium Membership Plans"),
    small_caps("Unlock Unlimited Access & Advanced Features!"),
    small_caps("Key Benefits"),
    small_caps("Unlimited Daily Downloads"),
    small_caps("Support for"),
    small_caps("File Sizes"),
    small_caps("Instant Processing"),
    small_caps("Zero Delay"),
    small_caps("Customizable Thumbnails"),
    small_caps("Personalized Captions"),
    small_caps("Priority Support"),
    small_caps("Pricing Options"),
    small_caps("Month Plan"),
    small_caps("Billed Monthly"),
    small_caps("Month Plan"),
    small_caps("Save"),
    small_caps("Lifetime Access"),
    small_caps("One-Time Payment"),
    small_caps("Secure Payment"),
    UPI_ID,
    QR_CODE,
    small_caps("Scan to Pay"),
    small_caps("After Payment"),
    small_caps("Send Screenshot to Admin for Instant Activation")
)

    PROGRESS_BAR = """<b>{}</b>
<blockquote>
<b>{}:</b> {bar} {percentage:.1f}%
<b>🚀 {}:</b> <code>{speed}/s</code>
<b>💾 {}:</b> <code>{current} {total}</code>
<b>⏱ {}:</b> <code>{elapsed}</code>
<b>⏳ {}:</b> <code>{eta}</code>
</blockquote>
""".format(
    small_caps("⚡ Processing Task..."),
    small_caps("Progress"),
    small_caps("Speed"),
    small_caps("Size"),
    small_caps("of"),
    small_caps("Elapsed"),
    small_caps("ETA")
)

    CAPTION = """<b><a href="https://t.me/THEUPDATEDGUYS">{}</a></b>\n\n<b>⚜️ {} : <a href="https://t.me/THEUPDATEDGUYS">{}</a></b>""".format(
    small_caps("⚡ Powered by THE UPDATED GUYS"),
    small_caps("Powered By"),
    small_caps("THE UPDATED GUYS 😎")
)

    LIMIT_REACHED = """<b>{}</b>
<b>{} 10 {}.</b>
<i>{} 24 {}.</i>

<blockquote><b>🔓 {}!</b></blockquote>
{}
""".format(
    small_caps("🚫 Daily Limit Exceeded"),
    small_caps("Your free saves for today have been used"),
    small_caps("files"),
    small_caps("Quota resets automatically after"),
    small_caps("hours from first download"),
    small_caps("Upgrade to Premium for Unlimited Access"),
    small_caps("Remove all restrictions and enjoy seamless downloading")
)

    SIZE_LIMIT = """<b>{}</b>
<b>{} 2GB {}.</b>

<blockquote><b>🔓 {}</b></blockquote>
{} 4GB {}!
""".format(
    small_caps("⚠️ File Size Exceeded"),
    small_caps("Free tier limited to"),
    small_caps("per file"),
    small_caps("Upgrade to Premium"),
    small_caps("Download files up to"),
    small_caps("and beyond with no limits")
)

    LOGIN_REQUIRED = """<b>{}</b>

<blockquote><i>{}</i>
<i>{}</i>
<i>{} /login {}.</i></blockquote>
""".format(
    small_caps("🔒 Authentication Required"),
    small_caps("Access to this content requires login"),
    small_caps("This is a private/restricted channel"),
    small_caps("Use"),
    small_caps("to securely authorize your account")
)

    CANCELLED = """<b>❌ {}</b>""".format(small_caps("Task Cancelled"))
    
    PROCESSING = """<b>⚠️ {}</b>
<i>{}</i>""".format(
    small_caps("A Task is Currently Processing"),
    small_caps("Please wait for completion or use /cancel to stop")
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
           
            # Use the formatted PROGRESS_BAR
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
   
    # Use premium images instead of API
    photo_url = get_random_premium_image()
   
    buttons = [
        [
            InlineKeyboardButton(small_caps("💎 Buy Premium"), callback_data="buy_premium"),
            InlineKeyboardButton(small_caps("🆘 Help & Guide"), callback_data="help_btn")
        ],
        [
            InlineKeyboardButton(small_caps("⚙️ Settings Panel"), callback_data="settings_btn"),
            InlineKeyboardButton(small_caps("ℹ️ About Bot"), callback_data="about_btn")
        ],
        [
            InlineKeyboardButton(small_caps('📢 Channels'), callback_data="channels_info"),
            InlineKeyboardButton(small_caps('👨‍💻 Developers'), callback_data="dev_info")
        ]
    ]
   
    reply_markup = InlineKeyboardMarkup(buttons)
    bot = await client.get_me()
   
    # Format start text with user mention
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
    buttons = [[InlineKeyboardButton(small_caps("❌ Close Menu"), callback_data="close_btn")]]
    await client.send_message(
        chat_id=message.chat.id,
        text=script.HELP_TXT,
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode=enums.ParseMode.HTML
    )

@Client.on_message(filters.command(["plan", "myplan", "premium"]))
async def send_plan(client: Client, message: Message):
    buttons = [
        [InlineKeyboardButton(small_caps("📸 Send Payment Proof"), url="https://t.me/DmOwner")],
        [InlineKeyboardButton(small_caps("❌ Close Menu"), callback_data="close_btn")]
    ]
   
    await client.send_photo(
        chat_id=message.chat.id,
        photo=SUBSCRIPTION,
        caption=script.PREMIUM_TEXT,
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode=enums.ParseMode.HTML
    )

@Client.on_message(filters.command(["cancel"]))
async def send_cancel(client: Client, message: Message):
    batch_temp.IS_BATCH[message.from_user.id] = True
    await message.reply_text(script.CANCELLED, parse_mode=enums.ParseMode.HTML)

async def settings_panel(client, callback_query):
    """
    Renders the Settings Menu with professional layout.
    """
    user_id = callback_query.from_user.id
    is_premium = await db.check_premium(user_id)
    badge = small_caps("💎 Premium Member") if is_premium else small_caps("👤 Standard User")
   
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton(small_caps("📜 Command List"), callback_data="cmd_list_btn")],
        [InlineKeyboardButton(small_caps("📊 Usage Stats"), callback_data="user_stats_btn")],
        [InlineKeyboardButton(small_caps("🗑 Dump Chat Settings"), callback_data="dump_chat_btn")],
        [InlineKeyboardButton(small_caps("🖼 Manage Thumbnail"), callback_data="thumb_btn")],
        [InlineKeyboardButton(small_caps("📝 Edit Caption"), callback_data="caption_btn")],
        [InlineKeyboardButton(small_caps("⬅️ Return to Home"), callback_data="start_btn")]
    ])
   
    text = f"<b>{small_caps('⚙️ Settings Dashboard')}</b>\n\n<b>{small_caps('Account Status:')}</b> {badge}\n<b>{small_caps('User ID:')}</b> <code>{user_id}</code>\n\n<i>{small_caps('Customize and manage your bot preferences below for an optimized experience')}:</i>"
   
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
            btn = InlineKeyboardMarkup([[InlineKeyboardButton(small_caps("💎 Upgrade to Premium"), callback_data="buy_premium")]])
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
                return await message.reply(f"<b>{small_caps('❌ Authentication Failed')}</b>\n\n<i>{small_caps('Your session may have expired. Please /logout and /login again')}.</i>\n<code>{e}</code>", parse_mode=enums.ParseMode.HTML)
           
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
            btn = InlineKeyboardMarkup([[InlineKeyboardButton(small_caps("💎 Upgrade to Premium"), callback_data="buy_premium")]])
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
    smsg = await client.send_message(message.chat.id, f"<b>{small_caps('⬇️ Starting Download...')}</b>", reply_to_message_id=message.id, parse_mode=enums.ParseMode.HTML)
   
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
   
   # --- DEVELOPER INFO ---
    if data == "dev_info":
        await callback_query.answer(
            text=f"{small_caps('👨‍💻 Mind Behind This Bot')}:\n• @DmOwner\n• @akaza7902\n• @xFlexyy",
            show_alert=True
        )
   
    elif data == "channels_info":
        await callback_query.answer(
            text=f"{small_caps('📢 Official Channels')}:\n• @ReX_update\n• @THEUPDATEDGUYS\n• @DragonByte_Network\n\n{small_caps('Stay updated for new features')}!",
            show_alert=True
        )
   
    elif data == "settings_btn":
        await settings_panel(client, callback_query)
   
    elif data == "buy_premium":
        buttons = [
            [InlineKeyboardButton(small_caps("📸 Send Payment Proof"), url="https://t.me/DmOwner")],
            [InlineKeyboardButton(small_caps("⬅️ Back to Home"), callback_data="start_btn")]
        ]
       
        await client.edit_message_media(
            chat_id=message.chat.id,
            message_id=message.id,
            media=InputMediaPhoto(
                media=SUBSCRIPTION,
                caption=script.PREMIUM_TEXT
            ),
            reply_markup=InlineKeyboardMarkup(buttons)
        )
   
    elif data == "help_btn":
        buttons = [[InlineKeyboardButton(small_caps("⬅️ Back to Home"), callback_data="start_btn")]]
        await client.edit_message_caption(
            chat_id=message.chat.id,
            message_id=message.id,
            caption=script.HELP_TXT,
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=enums.ParseMode.HTML
        )
   
    elif data == "about_btn":
        buttons = [[InlineKeyboardButton(small_caps("⬅️ Back to Home"), callback_data="start_btn")]]
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
                InlineKeyboardButton(small_caps("💎 Buy Premium"), callback_data="buy_premium"),
                InlineKeyboardButton(small_caps("🆘 Help & Guide"), callback_data="help_btn")
            ],
            [
                InlineKeyboardButton(small_caps("⚙️ Settings Panel"), callback_data="settings_btn"),
                InlineKeyboardButton(small_caps("ℹ️ About Bot"), callback_data="about_btn")
            ],
            [
                InlineKeyboardButton(small_caps('📢 Channels'), callback_data="channels_info"),
                InlineKeyboardButton(small_caps('👨‍💻 Developers'), callback_data="dev_info")
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
        # These will be implemented later
        await callback_query.answer(small_caps("🔄 Coming Soon!"), show_alert=True)
   
    await callback_query.answer()
