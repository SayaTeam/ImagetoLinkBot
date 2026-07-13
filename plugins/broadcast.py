import time
import asyncio
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.users_db import db
from info import ADMINS
from utils import temp, get_readable_time, users_broadcast

lock = asyncio.Lock()

@Client.on_message(filters.command("broadcast") & filters.user(ADMINS))
async def broadcast_command(bot, message):
    if not message.reply_to_message:
        return await message.reply_text("<b>⚠️ ᴘʟᴇᴀsᴇ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ ʙʀᴏᴀᴅᴄᴀsᴛ !</b>", quote=True, parse_mode=enums.ParseMode.HTML)
    if lock.locked():
        return await message.reply("<b>⚠️ ʙʀᴏᴀᴅᴄᴀsᴛ ɪs ᴀʟʀᴇᴀᴅʏ ʀᴜɴɴɪɴɢ !</b>\n\n<i>ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ ғᴏʀ ɪᴛ ᴛᴏ ᴄᴏᴍᴘʟᴇᴛᴇ.</i>", quote=True)
    
    

    msg_id = message.reply_to_message.id
    await message.reply(
        "<b>📌 ᴅᴏ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴘɪɴ ᴛʜɪs ᴍᴇssᴀɢᴇ ?</b>",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✅ ʏᴇs", callback_data=f"broadcast_ask#{msg_id}#yes"), InlineKeyboardButton("❌ ɴᴏ", callback_data=f"broadcast_ask#{msg_id}#no")]]),
        quote=True
    )

@Client.on_callback_query(filters.regex(r'^broadcast_ask'))
async def broadcast_confirm(bot, query):
    _, msg_id, answer = query.data.split("#")
    is_pin = True if answer == 'yes' else False
    if lock.locked():
        return await query.answer("⚠️ ʙʀᴏᴀᴅᴄᴀsᴛ ɪs ᴀʟʀᴇᴀᴅʏ ʀᴜɴɴɪɴɢ !", show_alert=True)
    
    await query.message.delete()
    b_sts = await query.message.reply("<b>⏳ ᴘʀᴏᴄᴇssɪɴɢ ʙʀᴏᴀᴅᴄᴀsᴛ...</b>")
    try:
        b_msg = await bot.get_messages(chat_id=query.message.chat.id, message_ids=int(msg_id))
    except Exception:
        return await b_sts.edit("<b>❌ ᴇʀʀᴏʀ : ᴏʀɪɢɪɴᴀʟ ᴍᴇssᴀɢᴇ ɴᴏᴛ ғᴏᴜɴᴅ !</b>")

    async with lock:
        users = await db.get_all_users()
        total_users = await db.total_users_count()
        start_time = time.time()
        done, success, failed = 0, 0, 0
        temp.USERS_CANCEL = False

        

        async for user in users:
            if temp.USERS_CANCEL:
                temp.USERS_CANCEL = False
                time_taken = get_readable_time(time.time() - start_time)
                return await b_sts.edit(f"<b>❌ ʙʀᴏᴀᴅᴄᴀsᴛ ᴄᴀɴᴄᴇʟʟᴇᴅ !</b>\n\n<b>⏱️ ᴛɪᴍᴇ :</b> {time_taken}\n<b>👥 ᴛᴏᴛᴀʟ :</b> <code>{total_users}</code>\n<b>✅ sᴜᴄᴄᴇss :</b> <code>{success}</code>\n<b>❌ ғᴀɪʟᴇᴅ :</b> <code>{failed}</code>")
            
            success_flag, sts = await users_broadcast(int(user['id']), b_msg, is_pin)
            if sts == 'Success': success += 1
            else: failed += 1
            done += 1

            if done % 20 == 0:
                btn = [[InlineKeyboardButton('✖️ ᴄᴀɴᴄᴇʟ ʙʀᴏᴀᴅᴄᴀsᴛ', callback_data='broadcast_cancel#users')]]
                await b_sts.edit(f"<b>📢 ʙʀᴏᴀᴅᴄᴀsᴛ ɪɴ ᴘʀᴏɢʀᴇss...</b>\n➖➖➖➖➖➖➖➖➖➖➖\n<b>👥 ᴛᴏᴛᴀʟ ᴜsᴇʀs :</b> <code>{total_users}</code>\n<b>✅ sᴜᴄᴄᴇss :</b> <code>{success}</code>\n<b>❌ ғᴀɪʟᴇᴅ :</b> <code>{failed}</code>\n<b>🔄 ᴄᴏᴍᴘʟᴇᴛᴇᴅ :</b> <code>{done}</code>\n➖➖➖➖➖➖➖➖➖➖➖", reply_markup=InlineKeyboardMarkup(btn))
        
        

        time_taken = get_readable_time(time.time() - start_time)
        await b_sts.edit(f"<b>✅ ʙʀᴏᴀᴅᴄᴀsᴛ ᴄᴏᴍᴘʟᴇᴛᴇᴅ !</b>\n➖➖➖➖➖➖➖➖➖➖➖\n<b>⏱️ ᴛɪᴍᴇ ᴛᴀᴋᴇɴ :</b> {time_taken}\n<b>👥 ᴛᴏᴛᴀʟ ᴜsᴇʀs :</b> <code>{total_users}</code>\n<b>✅ sᴜᴄᴄᴇss :</b> <code>{success}</code>\n<b>❌ ғᴀɪʟᴇᴅ :</b> <code>{failed}</code>\n➖➖➖➖➖➖➖➖➖➖➖")

@Client.on_callback_query(filters.regex(r'^broadcast_cancel'))
async def broadcast_cancel(bot, query):
    _, ident = query.data.split("#")
    if ident == 'users':
        await query.message.edit("<b>🛑 sᴛᴏᴘᴘɪɴɢ ʙʀᴏᴀᴅᴄᴀsᴛ...</b>")
        temp.USERS_CANCEL = True
        
