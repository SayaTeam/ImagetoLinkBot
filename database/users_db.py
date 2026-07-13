from motor.motor_asyncio import AsyncIOMotorClient
from info import DB_URL
from datetime import datetime

client = AsyncIOMotorClient(DB_URL)
mydb = client["avbotz"]

class Database:
    def __init__(self):
        self.users = mydb.users
        self.req = mydb.req
        self.config = mydb.config
        self.uploads = mydb.uploads

    async def add_user(self, id, name):
        user = {"id": int(id), "name": name}
        await self.users.update_one({"id": int(id)}, {"$set": user}, upsert=True)

    async def is_user_exist(self, id):
        user = await self.users.find_one({'id': int(id)})
        return bool(user)

    async def total_users_count(self):
        return await self.users.count_documents({})

    async def get_all_users(self):
        return self.users.find({})

    async def delete_user(self, user_id):
        await self.users.delete_many({'id': int(user_id)})

    async def add_join_req(self, user_id: int, channel_id: int):
        await self.req.update_one(
            {'user_id': user_id},
            {
                '$addToSet': {'channels': channel_id},
                '$setOnInsert': {'created_at': datetime.utcnow()}
            },
            upsert=True
        )

    async def has_joined_channel(self, user_id: int, channel_id: int):
        doc = await self.req.find_one({'user_id': user_id})
        return doc and 'channels' in doc and channel_id in doc['channels']

    async def del_join_req(self):
        await self.req.drop()
        
    

    async def get_maintenance_mode(self):
        data = await self.config.find_one({"_id": "maintenance_mode"})
        return data["status"] if data else False

    async def set_maintenance_mode(self, status):
        await self.config.update_one({"_id": "maintenance_mode"}, {"$set": {"status": status}}, upsert=True)

    async def set_upload_mode(self, mode):
        await self.config.update_one(
            {"_id": "bot_settings"},
            {"$set": {"upload_mode": mode}},
            upsert=True
        )

    async def get_upload_mode(self):
        data = await self.config.find_one({"_id": "bot_settings"})
        return data["upload_mode"] if data else "catbox"
        
    async def add_file(self, user_id, link):
        data = {"user_id": int(user_id), "link": link, "date": datetime.now()}
        await self.uploads.insert_one(data)

    async def get_user_files(self, user_id, limit=10, skip=0):
        return await self.uploads.find({"user_id": int(user_id)}).sort("date", -1).skip(skip).limit(limit).to_list(length=limit)

    async def total_files_by_user(self, user_id):
        return await self.uploads.count_documents({"user_id": int(user_id)})

    async def delete_file(self, user_id, link):
        await self.uploads.delete_one({"user_id": int(user_id), "link": link})

    async def delete_all_files(self, user_id):
        await self.uploads.delete_many({"user_id": int(user_id)})

    async def total_files_count(self):
        return await self.uploads.count_documents({})

    

    async def add_web_upload(self):
        await self.config.update_one({"_id": "website_stats"}, {"$inc": {"total_uploads": 1}}, upsert=True)

    async def total_web_uploads_count(self):
        data = await self.config.find_one({"_id": "website_stats"})
        return data["total_uploads"] if data else 0
        
    async def add_ban(self, user_id):
        await self.users.update_one({"id": int(user_id)}, {"$set": {"banned": True}}, upsert=True)

    async def remove_ban(self, user_id):
        await self.users.update_one({"id": int(user_id)}, {"$set": {"banned": False}}, upsert=True)

    async def is_banned(self, user_id):
        user = await self.users.find_one({"id": int(user_id)})
        return user.get("banned", False) if user else False
    
    async def get_banned_users(self):
        return self.users.find({"banned": True})

    async def total_banned_users_count(self):
        return await self.users.count_documents({"banned": True})
        
    

    async def get_top_uploaders(self):
        pipeline = [{"$group": {"_id": "$user_id", "count": {"$sum": 1}}}, {"$sort": {"count": -1}}]
        return await self.uploads.aggregate(pipeline).to_list(length=None)
        
    async def get_user_name(self, user_id):
        user = await self.users.find_one({"id": int(user_id)})
        return user["name"] if user else "Unknown"
        
db = Database()
