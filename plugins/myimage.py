import math
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message
from database.users_db import db

@Client.on_message(filters.command(["myimage", "myfiles", "history"]))
async def my_images_handler(client, message):
    await send_history_page(client, message, message.from_user.id, offset=0, edit=False)

@Client.on_callback_query(filters.regex(r"^myfiles_"))
async def myfiles_pagination(client, query: CallbackQuery):
    offset = int(query.data.split("_")[1])
    await send_history_page(client, query.message, query.from_user.id, offset=offset, edit=True)

async def send_history_page(client, message, user_id, offset=0, edit=False):
    limit = 10
    files = await db.get_user_files(user_id, limit=limit, skip=offset)
    total_files = await db.total_files_by_user(user_id)

    

    if total_files == 0:
        text = "<b>❌ ʏᴏᴜ ʜᴀᴠᴇ ɴᴏᴛ ᴜᴘʟᴏᴀᴅᴇᴅ ᴀɴʏ ғɪʟᴇs ʏᴇᴛ !</b>"
        if edit: await message.edit_text(text, parse_mode=enums.ParseMode.HTML)
        else: await message.reply_text(text, quote=True, parse_mode=enums.ParseMode.HTML)
        return

    text = f"<b>📂 ʏᴏᴜʀ ᴜᴘʟᴏᴀᴅs (ᴛᴏᴛᴀʟ : {total_files}) :</b>\n\n"
    for count, file in enumerate(files, start=offset + 1):
        link = file['link']
        text += f"<b>{count}.</b> <a href='{link}'>ᴄʟɪᴄᴋ ᴛᴏ ᴠɪᴇᴡ</a>\n<code>{link}</code>\n\n"
    
    buttons = []
    if total_files > 10:
        nav_row = []
        current_page = int(offset / limit) + 1
        total_pages = math.ceil(total_files / limit)
        if offset >= limit: nav_row.append(InlineKeyboardButton("⬅️ ʙᴀᴄᴋ", callback_data=f"myfiles_{offset - limit}"))
        nav_row.append(InlineKeyboardButton(f"{current_page}/{total_pages}", callback_data="pages_dummy"))
        if offset + limit < total_files: nav_row.append(InlineKeyboardButton("ɴᴇxᴛ ➡️", callback_data=f"myfiles_{offset + limit}"))
        buttons.append(nav_row)
    buttons.append([InlineKeyboardButton("✖️ ᴄʟᴏsᴇ", callback_data="close_data")])
    
    if edit: await message.edit_text(text=text, reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True, parse_mode=enums.ParseMode.HTML)
    else: await message.reply_text(text=text, reply_markup=InlineKeyboardMarkup(buttons), quote=True, disable_web_page_preview=True, parse_mode=enums.ParseMode.HTML)

@Client.on_callback_query(filters.regex("^pages_dummy"))
async def pages_dummy_callback(client, query: CallbackQuery):
    await query.answer("📃 ᴘᴀɢᴇ ᴄᴏᴜɴᴛᴇʀ", show_alert=False)

@Client.on_message(filters.command("delete"))
async def delete_link_handler(client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text(text="<b>⚠️ ᴘʟᴇᴀsᴇ ɢɪᴠᴇ ᴍᴇ ᴀ ʟɪɴᴋ ᴛᴏ ᴅᴇʟᴇᴛᴇ !\n\nᴇxᴀᴍᴘʟᴇ :</b> <code>/delete https://catbox.moe/xyz.jpg</code>", quote=True, parse_mode=enums.ParseMode.HTML)
    
    

    link = message.command[1]
    await db.delete_file(message.from_user.id, link)
    await message.reply_text(text=f"<b>✅ ʟɪɴᴋ ʀᴇᴍᴏᴠᴇᴅ ғʀᴏᴍ ᴅᴀᴛᴀʙᴀsᴇ !</b>\n<code>{link}</code>", quote=True, parse_mode=enums.ParseMode.HTML)

@Client.on_message(filters.command(["delall", "deleteall", "all_del"]))
async def delete_all_command(client, message):
    buttons = [[InlineKeyboardButton("✅ ʏᴇs", callback_data="delall_yes"), InlineKeyboardButton("❌ ɴᴏ", callback_data="delall_no")]]
    await message.reply_text(text="<b>⚠️ ᴀʀᴇ ʏᴏᴜ sᴜʀᴇ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴅᴇʟᴇᴛᴇ ᴀʟʟ ʏᴏᴜʀ ʜɪsᴛᴏʀʏ ?\n\nᴛʜɪs ᴀᴄᴛɪᴏɴ ᴄᴀɴɴᴏᴛ ʙᴇ ᴜɴᴅᴏɴᴇ !</b>", reply_markup=InlineKeyboardMarkup(buttons), quote=True, parse_mode=enums.ParseMode.HTML)

@Client.on_callback_query(filters.regex("^delall_yes"))
async def delete_all_confirm_callback(client, query):
    await db.delete_all_files(query.from_user.id)
    
    

    await query.message.edit_text(text="<b>✅ sᴜᴄᴄᴇssғᴜʟʟʏ ᴅᴇʟᴇᴛᴇᴅ ᴀʟʟ ʏᴏᴜʀ ʜɪsᴛᴏʀʏ !</b>", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✖️ ᴄʟᴏsᴇ", callback_data="close_data")]]), parse_mode=enums.ParseMode.HTML)

@Client.on_callback_query(filters.regex("^delall_no"))
async def delete_all_cancel_callback(client, query):
    await query.message.edit_text(text="<b>❌ ᴘʀᴏᴄᴇss ᴄᴀɴᴄᴇʟʟᴇᴅ !</b>", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✖️ ᴄʟᴏsᴇ", callback_data="close_data")]]), parse_mode=enums.ParseMode.HTML)
    
