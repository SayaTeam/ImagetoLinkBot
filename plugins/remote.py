import os
import time
import aiohttp
from pyrogram import Client, filters, enums
from utils import upload_to_catbox, upload_to_uguu, temp
from database.users_db import db
from info import LOG_CHANNEL

@Client.on_message(filters.command(["remote", "url", "upload"]))
async def remote_upload(client, message):
    if await db.is_banned(message.from_user.id):
        return await message.reply(text="<b>🚫 ʏᴏᴜ ᴀʀᴇ ʙᴀɴɴᴇᴅ ғʀᴏᴍ ᴜsɪɴɢ ᴛʜɪs ʙᴏᴛ !\n\n👮‍♂️ ᴄᴏɴᴛᴀᴄᴛ : @SayaProject</b>", quote=True, parse_mode=enums.ParseMode.HTML)

    

    if len(message.command) < 2:
        return await message.reply("<b>⚠️ ᴘʀᴏᴠɪᴅᴇ ᴀ ᴅɪʀᴇᴄᴛ ʟɪɴᴋ !\n\nᴇx:</b> <code>/remote https://example.com/image.jpg</code>")
    url = message.command[1]
    status_msg = await message.reply("<b>📥 ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ғʀᴏᴍ ᴜʀʟ...</b>")
    filename = f"downloaded_{int(time.time())}"
    try:
        if "." in url:
            ext = url.split(".")[-1]
            filename += f".{ext}" if len(ext) < 5 else ".jpg"
        else:
            filename += ".jpg"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    return await status_msg.edit("<b>❌ ɪɴᴠᴀʟɪᴅ ʟɪɴᴋ ᴏʀ sᴇʀᴠᴇʀ ᴇʀʀᴏʀ !</b>")
                with open(filename, 'wb') as f:
                    while True:
                        chunk = await resp.content.read(1024)
                        if not chunk: break
                        f.write(chunk)

        

        current_server = temp.UPLOAD_MODE.upper()
        await status_msg.edit(f"<b>📤 ᴜᴘʟᴏᴀᴅɪɴɢ ᴛᴏ {current_server}...</b>")
        link = None
        if temp.UPLOAD_MODE == "uguu":
            link = await upload_to_uguu(filename)
            if not link:
                await status_msg.edit("<b>⚠️ ᴜɢᴜᴜ ғᴀɪʟᴇᴅ, ᴛʀʏɪɴɢ ᴄᴀᴛʙᴏx...</b>")
                link = await upload_to_catbox(filename)
        else:
            link = await upload_to_catbox(filename)
            if not link:
                await status_msg.edit("<b>⚠️ ᴄᴀᴛʙᴏx ғᴀɪʟᴇᴅ, ᴛʀʏɪɴɢ ᴜɢᴜᴜ...</b>")
                link = await upload_to_uguu(filename)

        

        if link:
            await db.add_file(message.from_user.id, link)
            await status_msg.edit(f"<b>✅ ʀᴇᴍᴏᴛᴇ ᴜᴘʟᴏᴀᴅ sᴜᴄᴄᴇss !</b>\n\n<b>🔗 ʟɪɴᴋ :</b> <code>{link}</code>", disable_web_page_preview=True, parse_mode=enums.ParseMode.HTML)
            if LOG_CHANNEL:
                try:
                    log_text = f"<b>#RemoteUpload</b>\n\n<b>👤 ᴜsᴇʀ :</b> {message.from_user.mention} (<code>{message.from_user.id}</code>)\n<b>🔗 ʟɪɴᴋ :</b> <code>{link}</code>\n<b>⚙️ sᴇʀᴠᴇʀ :</b> <code>{temp.UPLOAD_MODE.upper()}</code>\n<b>🕒 ᴛɪᴍᴇ :</b> <code>{message.date}</code>"
                    await client.send_message(chat_id=LOG_CHANNEL, text=log_text, parse_mode=enums.ParseMode.HTML, disable_web_page_preview=True)
                except Exception:
                    pass
        else:
            await status_msg.edit("<b>❌ ᴜᴘʟᴏᴀᴅ ғᴀɪʟᴇᴅ ᴏɴ ʙᴏᴛʜ sᴇʀᴠᴇʀs !</b>")
    except Exception as e:
        await status_msg.edit(f"<b>❌ ᴇʀʀᴏʀ :</b> {e}")
    finally:
        if os.path.exists(filename): os.remove(filename)
            
