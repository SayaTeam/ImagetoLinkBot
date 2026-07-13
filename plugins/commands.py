from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from info import ADMINS

@Client.on_message(filters.command(["commands", "help", "list"]))
async def show_all_commands(client, message):
    
    

    text = (
        "<b>📜 ᴀʟʟ ᴀᴠᴀɪʟᴀʙʟᴇ ᴄᴏᴍᴍᴀɴᴅs</b>\n"
        "➖➖➖➖➖➖➖➖➖➖➖\n\n"
        "<b>👤 ᴜsᴇʀ ᴄᴏᴍᴍᴀɴᴅs :</b>\n"
        "➤ <code>/start</code> : sᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ\n"
        "➤ <code>/remote</code> : ᴜᴘʟᴏᴀᴅ ғʀᴏᴍ ᴜʀʟ\n"
        "➤ <code>/myfiles</code> : ʏᴏᴜʀ ᴜᴘʟᴏᴀᴅ ʜɪsᴛᴏʀʏ\n"
        "➤ <code>/delete</code> : ᴅᴇʟᴇᴛᴇ ᴀ ғɪʟᴇ\n"
        "➤ <code>/delall</code> : ᴅᴇʟᴇᴛᴇ ᴀʟʟ ʜɪsᴛᴏʀʏ\n\n"
        "<b>👮‍♂️ ᴀᴅᴍɪɴ ᴄᴏᴍᴍᴀɴᴅs :</b>\n"
        "➤ <code>/mode</code> : ᴄʜᴀɴɢᴇ sᴇʀᴠᴇʀ (ᴄᴀᴛ/ᴜɢᴜᴜ)\n"
        "➤ <code>/stats</code> : ᴄʜᴇᴄᴋ ʙᴏᴛ sᴛᴀᴛs\n"
        "➤ <code>/check</code> : ᴄʜᴇᴄᴋ ᴜsᴇʀ ɪɴғᴏ\n"
        "➤ <code>/ban</code> : ʙᴀɴ ᴀ ᴜsᴇʀ\n"
        "➤ <code>/unban</code> : ᴜɴʙᴀɴ ᴀ ᴜsᴇʀ\n"
        "➤ <code>/banned</code> : ʙᴀɴɴᴇᴅ ᴜsᴇʀ ʟɪsᴛ\n"
        "➤ <code>/broadcast</code> : sᴇɴᴅ ᴍᴇssᴀɢᴇ ᴛᴏ ᴀʟʟ\n"
        "➤ <code>/maintenance</code> : ᴏɴ/ᴏғғ ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ\n"
        "➤ <code>/top</code> : ᴛᴏᴘ ᴜᴘʟᴏᴀᴅᴇʀs ʟɪsᴛ\n"
        "➖➖➖➖➖➖➖➖➖➖➖"
    )

    

    buttons = [[InlineKeyboardButton("✖️ ᴄʟᴏsᴇ", callback_data="close_data")]]
    
    
    
    await message.reply_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(buttons),
        quote=True,
        parse_mode=enums.ParseMode.HTML
    )
  
