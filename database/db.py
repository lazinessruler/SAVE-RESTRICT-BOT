import motor.motor_asyncio
import datetime
from config import DB_NAME, DB_URI
from logger import LOGGER

logger = LOGGER(__name__)

class Database:
   
    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users
        self.settings = self.db.settings
        self.urls = self.db.urls
   
    def new_user(self, id, name):
        return dict(
            id = id,
            name = name,
            session = None,
            daily_usage = 0,
            limit_reset_time = None,
            total_usage = 0,
            joined_date = datetime.datetime.now(),
            thumbnail = None,
            caption = None,
            is_premium = False,
            premium_expiry = None,
            is_banned = False,
            dump_chat = None,
            delete_words = [],
            replace_words = {}
        )
   
    async def add_user(self, id, name):
        if await self.is_user_exist(id):
            return
        user = self.new_user(id, name)
        await self.col.insert_one(user)
        logger.info(f"✅ New user added to DB: {id} - {name}")
   
    async def is_user_exist(self, id):
        user = await self.col.find_one({'id': int(id)})
        return bool(user)
   
    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count
   
    async def get_all_users(self):
        return self.col.find({})
   
    async def delete_user(self, user_id):
        await self.col.delete_many({'id': int(user_id)})
        logger.info(f"🗑️ User deleted from DB: {user_id}")
   
    # ==================== SESSION FUNCTIONS ====================
   
    async def set_session(self, id, session):
        await self.col.update_one({'id': int(id)}, {'$set': {'session': session}})
   
    async def get_session(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('session') if user else None
   
    # ==================== CAPTION FUNCTIONS ====================
   
    async def set_caption(self, id, caption):
        await self.col.update_one({'id': int(id)}, {'$set': {'caption': caption}})
   
    async def get_caption(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('caption') if user else None
   
    async def del_caption(self, id):
        await self.col.update_one({'id': int(id)}, {'$unset': {'caption': ""}})
   
    # ==================== THUMBNAIL FUNCTIONS ====================
   
    async def set_thumbnail(self, id, thumbnail):
        await self.col.update_one({'id': int(id)}, {'$set': {'thumbnail': thumbnail}})
   
    async def get_thumbnail(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('thumbnail') if user else None
   
    async def del_thumbnail(self, id):
        await self.col.update_one({'id': int(id)}, {'$unset': {'thumbnail': ""}})
   
    # ==================== PREMIUM FUNCTIONS - FIXED ====================
   
    async def add_premium(self, id, expiry_date):
        """Add premium to user - expiry_date must be datetime object"""
        # Ensure expiry_date is datetime
        if not isinstance(expiry_date, datetime.datetime):
            if isinstance(expiry_date, str):
                try:
                    # Try ISO format
                    expiry_date = datetime.datetime.fromisoformat(expiry_date.replace('Z', '+00:00'))
                except:
                    try:
                        # Try common format
                        expiry_date = datetime.datetime.strptime(expiry_date, "%Y-%m-%d %H:%M:%S")
                    except:
                        # Default to 30 days from now
                        expiry_date = datetime.datetime.now() + datetime.timedelta(days=30)
            else:
                expiry_date = datetime.datetime.now() + datetime.timedelta(days=30)
        
        await self.col.update_one({'id': int(id)}, {
            '$set': {
                'is_premium': True,
                'premium_expiry': expiry_date,
                'daily_usage': 0,
                'limit_reset_time': None
            }
        })
        logger.info(f"💎 User {id} granted premium until {expiry_date}")
   
    async def remove_premium(self, id):
        """Remove premium from user"""
        await self.col.update_one({'id': int(id)}, {
            '$set': {
                'is_premium': False,
                'premium_expiry': None
            }
        })
        logger.info(f"💎 User {id} removed from premium")
   
    async def check_premium(self, id):
        """Check if user has active premium - FIXED"""
        user = await self.col.find_one({'id': int(id)})
        if not user:
            return False
        
        if not user.get('is_premium'):
            return False
        
        expiry = user.get('premium_expiry')
        if not expiry:
            return False
        
        # FIX: Convert string to datetime if needed
        now = datetime.datetime.now()
        
        if isinstance(expiry, str):
            try:
                # Try to parse the string
                if 'T' in expiry:
                    expiry = datetime.datetime.fromisoformat(expiry.replace('Z', '+00:00'))
                else:
                    expiry = datetime.datetime.strptime(expiry, "%Y-%m-%d %H:%M:%S")
            except Exception as e:
                logger.error(f"Error parsing expiry date: {e}")
                # If can't parse, assume expired
                await self.remove_premium(id)
                return False
        
        # Now compare
        if expiry > now:
            return True
        else:
            # Expired
            await self.remove_premium(id)
            return False
   
    async def get_premium_users(self):
        """Get all premium users"""
        cursor = self.col.find({'is_premium': True})
        return await cursor.to_list(length=None)
   
    # ==================== BAN FUNCTIONS ====================
   
    async def ban_user(self, id):
        await self.col.update_one({'id': int(id)}, {'$set': {'is_banned': True}})
        logger.warning(f"🚫 User banned: {id}")
   
    async def unban_user(self, id):
        await self.col.update_one({'id': int(id)}, {'$set': {'is_banned': False}})
        logger.info(f"✅ User unbanned: {id}")
   
    async def is_banned(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('is_banned', False) if user else False
   
    # ==================== DUMP CHAT FUNCTIONS ====================
   
    async def set_dump_chat(self, id, chat_id):
        await self.col.update_one({'id': int(id)}, {'$set': {'dump_chat': int(chat_id) if chat_id else None}})
   
    async def get_dump_chat(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('dump_chat') if user else None
   
    # ==================== DELETE/WORDS FUNCTIONS ====================
   
    async def set_delete_words(self, id, words):
        await self.col.update_one({'id': int(id)}, {'$addToSet': {'delete_words': {'$each': words}}})
   
    async def get_delete_words(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('delete_words', []) if user else []
   
    async def remove_delete_words(self, id, words):
        await self.col.update_one({'id': int(id)}, {'$pull': {'delete_words': {'$in': words}}})
   
    # ==================== REPLACE WORDS FUNCTIONS ====================
   
    async def set_replace_words(self, id, repl_dict):
        user = await self.col.find_one({'id': int(id)})
        if user:
            current_repl = user.get('replace_words', {})
            current_repl.update(repl_dict)
            await self.col.update_one({'id': int(id)}, {'$set': {'replace_words': current_repl}})
   
    async def get_replace_words(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('replace_words', {}) if user else {}
   
    async def remove_replace_words(self, id, words):
        user = await self.col.find_one({'id': int(id)})
        if user:
            current_repl = user.get('replace_words', {})
            for w in words:
                current_repl.pop(w, None)
            await self.col.update_one({'id': int(id)}, {'$set': {'replace_words': current_repl}})
   
    # ==================== DAILY LIMIT FUNCTIONS ====================
   
    async def check_limit(self, id):
        """Check if user has hit daily limit"""
        user = await self.col.find_one({'id': int(id)})
        if not user:
            return False
       
        # Premium Check
        if await self.check_premium(id):
            return False
       
        # Check Time Reset
        now = datetime.datetime.now()
        reset_time = user.get('limit_reset_time')
       
        if reset_time is None or now >= reset_time:
            await self.col.update_one(
                {'id': int(id)},
                {'$set': {'daily_usage': 0, 'limit_reset_time': None}}
            )
            return False
       
        # Check Count
        usage = user.get('daily_usage', 0)
        if usage >= 10:
            return True
       
        return False
   
    async def add_traffic(self, id):
        """Increment usage count"""
        user = await self.col.find_one({'id': int(id)})
        if not user:
            return
       
        # Increment total usage
        await self.col.update_one(
            {'id': int(id)},
            {'$inc': {'total_usage': 1}}
        )
       
        # If premium, don't track daily
        if await self.check_premium(id):
            return
       
        now = datetime.datetime.now()
        reset_time = user.get('limit_reset_time')
       
        if reset_time is None:
            new_reset_time = now + datetime.timedelta(hours=24)
            await self.col.update_one(
                {'id': int(id)},
                {'$set': {'daily_usage': 1, 'limit_reset_time': new_reset_time}}
            )
        else:
            await self.col.update_one(
                {'id': int(id)},
                {'$inc': {'daily_usage': 1}}
            )
   
    async def get_user_stats(self, id):
        """Get user statistics"""
        user = await self.col.find_one({'id': int(id)})
        if not user:
            return None
       
        return {
            'id': user.get('id'),
            'name': user.get('name'),
            'joined': user.get('joined_date'),
            'total_usage': user.get('total_usage', 0),
            'daily_usage': user.get('daily_usage', 0),
            'is_premium': await self.check_premium(id),
            'has_thumbnail': bool(user.get('thumbnail')),
            'has_caption': bool(user.get('caption'))
        }
   
    # ==================== RENDER URL FUNCTIONS ====================
   
    async def add_url(self, url: str, name: str = None) -> bool:
        try:
            if not name:
                name = url.replace("https://", "").replace("http://", "").split(".")[0]
           
            await self.urls.update_one(
                {"url": url},
                {
                    "$set": {
                        "url": url,
                        "name": name,
                        "active": True,
                        "last_ping": None,
                        "last_status": None,
                        "last_error": None,
                        "added_at": datetime.datetime.now()
                    }
                },
                upsert=True
            )
            return True
        except Exception as e:
            logger.error(f"Error adding URL: {e}")
            return False
   
    async def remove_url(self, url: str) -> bool:
        result = await self.urls.delete_one({"url": url})
        return result.deleted_count > 0
   
    async def get_all_urls(self):
        cursor = self.urls.find({})
        return await cursor.to_list(length=None)
   
    async def update_url_status(self, url: str, status: int = None, error: str = None):
        update_data = {"last_ping": datetime.datetime.now()}
        if status:
            update_data["last_status"] = status
        if error:
            update_data["last_status"] = "Failed"
            update_data["last_error"] = error
        await self.urls.update_one({"url": url}, {"$set": update_data})
   
    async def get_active_urls(self):
        cursor = self.urls.find({"active": True})
        return await cursor.to_list(length=None)

db = Database(DB_URI, DB_NAME)
