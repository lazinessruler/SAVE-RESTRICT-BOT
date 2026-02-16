import asyncio
import datetime
import sys
import os
from datetime import timezone, timedelta
from pyrogram import Client, filters, enums, __version__ as pyrogram_version
from pyrogram.types import Message, BotCommand
from pyrogram.errors import FloodWait, RPCError
from config import API_ID, API_HASH, BOT_TOKEN, LOG_CHANNEL, ADMINS
from database.db import db
from logger import LOGGER

# Keep-alive server (Render / Heroku)
try:
    from keep_alive import keep_alive
except ImportError:
    keep_alive = None

logger = LOGGER(__name__)
IST = timezone(timedelta(hours=5, minutes=30))

# Small cache for your ~200 users to prevent DB lag
USER_CACHE = set()

LOGO = r"""
  ██████╗  ██╗  ██╗  █████╗  ███╗   ██╗ ██████╗   █████╗  ██╗      
  ██╔══██╗ ██║  ██║ ██╔══██╗ ████╗  ██║ ██╔══██╗ ██╔══██╗ ██║      
  ██║  ██║ ███████║ ███████║ ██╔██╗ ██║ ██████╔╝ ███████║ ██║      
  ██║  ██║ ██╔══██║ ██╔══██║ ██║╚██╗██║ ██╔═══╝  ██╔══██║ ██║      
  ██████╔╝ ██║  ██║ ██║  ██║ ██║ ╚████║ ██║      ██║  ██║ ███████
    𝙱𝙾𝚃 𝚆𝙾𝚁𝙺𝙸𝙽𝙶 𝙿𝚁𝙾𝙿𝙴𝚁𝙻𝚈....
"""

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="cantarella_Login_Bot",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            plugins=dict(root="cantarella"),
            workers=10, 
            sleep_threshold=15,
            max_concurrent_transmissions=5,
            ipv6=False,
            in_memory=False,
        )
        self._keep_alive_started = False

    async def start(self):
        print(LOGO)

        # 1. Start keep-alive BEFORE attempting Telegram login
        if keep_alive and not self._keep_alive_started:
            try:
                loop = asyncio.get_running_loop()
                try:
                    keep_alive(loop)
                except TypeError:
                    keep_alive()
                self._keep_alive_started = True
                logger.info("Keep-alive server started.")
            except Exception as e:
                logger.warning(f"Keep-alive failed: {e}")

        # 2. FIX FOR FLOOD WAIT: Resilient Login Loop
        while True:
            try:
                await super().start()
                break # Success!
            except FloodWait as e:
                wait_time = int(e.value) + 10
                logger.warning(f"FLOOD_WAIT detected during login. Sleeping for {wait_time}s...")
                await asyncio.sleep(wait_time)
            except Exception as e:
                logger.error(f"Critical Startup Error: {e}")
                await asyncio.sleep(15)

        me = await self.get_me()

        # 3. DB Stats
        try:
            user_count = await db.total_users_count()
            logger.info(f"MongoDB Connected: {user_count} users found.")
        except Exception as e:
            logger.error(f"DB stats failed: {e}")
            user_count = "Unknown"

        # 4. Startup notification
        now = datetime.datetime.now(IST)
        startup_text = (
            f"<b><i>🤖 Bot Successfully Started ♻️</i></b>\n\n"
            f"<b>Bot:</b> @{me.username}\n"
            f"<b>Users:</b> <code>{user_count} / 200</code>\n"
            f"<b>Time:</b> <code>{now.strftime('%I:%M %p')} IST</code>\n\n"
            f"<b>Developed by @cantarellabots</b>"
        )

        try:
            await self.send_message(LOG_CHANNEL, startup_text)
            logger.info("Startup log sent.")
        except Exception as e:
            logger.error(f"Failed to send startup log: {e}")

        await self.set_bot_commands_list()

    async def stop(self, *args):
        try:
            await self.send_message(LOG_CHANNEL, "<b><i>❌ Bot is going Offline</i></b>")
        except:
            pass
        await asyncio.shield(super().stop())
        logger.info("Bot stopped cleanly")

    async def set_bot_commands_list(self):
        commands = [
    BotCommand("start", "ꜱᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ 🚀"),
    BotCommand("help", "ɢᴇᴛ ʜᴇʟᴘ & ɢᴜɪᴅᴇ 📖"),
    BotCommand("login", "ʟᴏɢɪɴ ᴛᴏ ʏᴏᴜʀ ᴀᴄᴄᴏᴜɴᴛ 🔐"),
    BotCommand("logout", "ʟᴏɢᴏᴜᴛ ꜱᴀꜰᴇʟʏ 🚪"),
    BotCommand("cancel", "ᴄᴀɴᴄᴇʟ ᴄᴜʀʀᴇɴᴛ ᴀᴄᴛɪᴏɴ ❌"),
    BotCommand("myplan", "ᴄʜᴇᴄᴋ ʏᴏᴜʀ ᴘʟᴀɴ 💎"),
    BotCommand("premium", "ᴘʀᴇᴍɪᴜᴍ ɪɴꜰᴏ & ʙᴇɴᴇꜰɪᴛꜱ ✨"),
    BotCommand("setchat", "ꜱᴇᴛ ᴛᴀʀɢᴇᴛ ᴄʜᴀᴛ 🎯"),
    BotCommand("set_thumb", "ꜱᴇᴛ ᴄᴜꜱᴛᴏᴍ ᴛʜᴜᴍʙɴᴀɪʟ 🖼"),
    BotCommand("view_thumb", "ᴠɪᴇᴡ ʏᴏᴜʀ ᴛʜᴜᴍʙɴᴀɪʟ 👀"),
    BotCommand("del_thumb", "ᴅᴇʟᴇᴛᴇ ᴛʜᴜᴍʙɴᴀɪʟ 🗑"),
    BotCommand("set_caption", "ꜱᴇᴛ ᴄᴜꜱᴛᴏᴍ ᴄᴀᴘᴛɪᴏɴ 📝"),
    BotCommand("see_caption", "ᴠɪᴇᴡ ᴄᴜʀʀᴇɴᴛ ᴄᴀᴘᴛɪᴏɴ 👁"),
    BotCommand("del_caption", "ᴅᴇʟᴇᴛᴇ ᴄᴀᴘᴛɪᴏɴ ❌"),
    BotCommand("set_del_word", "ᴀᴅᴅ ᴅᴇʟᴇᴛᴇ ᴡᴏʀᴅ 🚫"),
    BotCommand("rem_del_word", "ʀᴇᴍᴏᴠᴇ ᴅᴇʟᴇᴛᴇ ᴡᴏʀᴅ ♻️"),
    BotCommand("set_repl_word", "ᴀᴅᴅ ʀᴇᴘʟᴀᴄᴇ ᴡᴏʀᴅ 🔄"),
    BotCommand("rem_repl_word", "ʀᴇᴍᴏᴠᴇ ʀᴇᴘʟᴀᴄᴇ ᴡᴏʀᴅ 🔁"),
]
        await self.set_bot_commands(commands)

BotInstance = Bot()

@BotInstance.on_message(filters.private & filters.incoming, group=-1)
async def new_user_log(bot: Client, message: Message):
    user = message.from_user
    if not user or user.id in USER_CACHE:
        return

    if not await db.is_user_exist(user.id):
        await db.add_user(user.id, user.first_name)
        
        now = datetime.datetime.now(IST)
        log_text = (
            f"<b>#NewUser 👤</b>\n"
            f"<b>User:</b> {user.mention}\n"
            f"<b>ID:</b> <code>{user.id}</code>\n"
            f"<b>Time:</b> {now.strftime('%I:%M %p')} IST"
        )
        try:
            await bot.send_message(LOG_CHANNEL, log_text)
        except:
            pass
    
    USER_CACHE.add(user.id)

@BotInstance.on_message(filters.command("cmd") & filters.user(ADMINS))
async def update_commands(bot: Client, message: Message):
    try:
        await bot.set_bot_commands_list()
        await message.reply_text("✅ Commands menu updated!")
    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")

if __name__ == "__main__":
    BotInstance.run()
