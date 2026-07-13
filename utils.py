import os
import asyncio
import aiohttp
import logging
from pyrogram import Client, enums
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid
from database.users_db import db
from Script import script

class temp(object):
    ME = None
    U_NAME = None
    B_NAME = None
    B_LINK = None
    USERS_CANCEL = False  
    MAINTENANCE = False 
    UPLOAD_MODE = "catbox"

def get_readable_time(seconds: int) -> str:
    result = ""
    (days, remainder) = divmod(seconds, 86400)
    days = int(days)
    if days != 0: result += f"{days}d "
    (hours, remainder) = divmod(remainder, 3600)
    hours = int(hours)
    if hours != 0: result += f"{hours}h "
    (minutes, seconds) = divmod(remainder, 60)
    minutes = int(minutes)
    if minutes != 0: result += f"{minutes}m "
    seconds = int(seconds)
    result += f"{seconds}s"
    return result

async def users_broadcast(user_id, message, is_pin):
    try:
        m = await message.copy(chat_id=user_id)
        if is_pin:
            try: await m.pin(both_sides=True)
            except Exception: pass 
        return True, "Success"
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await users_broadcast(user_id, message, is_pin)
    except InputUserDeactivated:
        await db.delete_user(int(user_id))
        return False, "Deleted"
    except UserIsBlocked:
        await db.delete_user(int(user_id))
        return False, "Blocked"
    except PeerIdInvalid:
        await db.delete_user(int(user_id))
        return False, "Error"
    except Exception: return False, "Error"

async def upload_to_catbox(file_path):
    url = "https://catbox.moe/user/api.php"
    try:
        async with aiohttp.ClientSession() as session:
            data = aiohttp.FormData()
            data.add_field('reqtype', 'fileupload')
            data.add_field('userhash', '')
            data.add_field('fileToUpload', open(file_path, 'rb'))
            async with session.post(url, data=data) as response:
                if response.status == 200:
                    text = await response.text()
                    if text.startswith("https://"): return text.strip()
    except Exception: pass
    return None

async def upload_to_uguu(file_path):
    url = "https://uguu.se/upload"
    try:
        async with aiohttp.ClientSession() as session:
            data = aiohttp.FormData()
            data.add_field('files[]', open(file_path, 'rb'))
            async with session.post(url, data=data) as resp:
                if resp.status == 200:
                    result = await resp.json()
                    if result.get('success') or 'files' in result:
                        return result['files'][0]['url'].replace('\\/', '/')
    except Exception: pass
    return None

