from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from database.users_db import db
from utils import temp
from info import ADMINS, AUTH_CHANNEL, LOG_CHANNEL

BYPASS_IDS = ADMINS + [LOG_CHANNEL]
if isinstance(AUTH_CHANNEL, list): BYPASS_IDS.extend(AUTH_CHANNEL)
elif AUTH_CHANNEL: BYPASS_IDS.append(AUTH_CHANNEL)

@Client.on_message(filters.incoming, group=-1)
async def maintenance_check(client, message: Message):
    if not temp.MAINTENANCE: return
    user_id = message.from_user.id if message.from_user else None
    if user_id in ADMINS or message.chat.id in BYPASS_IDS: return

    

    buttons = [[InlineKeyboardButton("💬 sᴜᴘᴘᴏʀᴛ", url="https://t.me/SayaProject")]]
    await message.reply_text(
        text="<b>🚧 ʙᴏᴛ ɪs ᴜɴᴅᴇʀ ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ !\n\n⚠️ ᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ ʟᴀᴛᴇʀ.\n⏳ ᴡᴇ ᴀʀᴇ ᴜᴘᴅᴀᴛɪɴɢ ᴛʜᴇ sᴇʀᴠᴇʀ...</b>",
        reply_markup=InlineKeyboardMarkup(buttons),
        quote=True,
        parse_mode=enums.ParseMode.HTML
    )
    message.stop_propagation()

@Client.on_message(filters.command("maintenance") & filters.user(ADMINS))
async def maintenance_command(client, message):
    status = "ᴇɴᴀʙʟᴇᴅ" if temp.MAINTENANCE else "ᴅɪsᴀʙʟᴇᴅ"
    buttons = [
        [InlineKeyboardButton("✅ ᴇɴᴀʙʟᴇ", callback_data="main_on"), InlineKeyboardButton("❌ ᴅɪsᴀʙʟᴇ", callback_data="main_off")],
        [InlineKeyboardButton("🗑️ ᴄʟᴏsᴇ", callback_data="close_data")]
    ]
    
    

    await message.reply_text(
        text=f"<b>🛠 ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ ᴍᴏᴅᴇ\n\n📊 ᴄᴜʀʀᴇɴᴛ sᴛᴀᴛᴜs : <code>{status}</code>\n\n⚙️ sᴇʟᴇᴄᴛ ᴀɴ ᴏᴘᴛɪᴏɴ ʙᴇʟᴏᴡ :</b>",
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode=enums.ParseMode.HTML
    )

@Client.on_callback_query(filters.regex("^main_"))
async def maintenance_callback(client, query: CallbackQuery):
    data = query.data
    if data == "main_on":
        if temp.MAINTENANCE: return await query.answer("⚠️ ᴀʟʀᴇᴀᴅʏ ᴇɴᴀʙʟᴇᴅ !", show_alert=True)
        temp.MAINTENANCE = True
        await db.set_maintenance_mode(True)
        await query.message.edit_text("<b>✅ ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ ᴍᴏᴅᴇ ᴇɴᴀʙʟᴇᴅ !</b>", parse_mode=enums.ParseMode.HTML)
    elif data == "main_off":
        if not temp.MAINTENANCE: return await query.answer("⚠️ ᴀʟʀᴇᴀᴅʏ ᴅɪsᴀʙʟᴇᴅ !", show_alert=True)
        temp.MAINTENANCE = False
        await db.set_maintenance_mode(False)

        

        await query.message.edit_text("<b>❌ ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ ᴍᴏᴅᴇ ᴅɪsᴀʙʟᴇᴅ !</b>", parse_mode=enums.ParseMode.HTML)
        
