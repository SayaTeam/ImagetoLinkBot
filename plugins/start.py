

from pyrogram import Client, filters, enums
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from database.users_db import db
from Script import script
from info import START_PIC, LOG_CHANNEL, CHANNEL, SUPPORT, FSUB, ADMINS, APP_URL
from utils import temp
from plugins.fsub import is_user_joined

@Client.on_message(filters.command("start") & filters.private)
async def start_command(client, message: Message):
    user_id = message.from_user.id
    mention = message.from_user.mention
    if FSUB and not await is_user_joined(client, message):
        return
    if not await db.is_user_exist(user_id):
        await db.add_user(user_id, message.from_user.first_name)
        if LOG_CHANNEL:
            try:
                bot_name = temp.B_NAME
                log_text = script.LOG_TEXT.format(bot_name, user_id, mention)
                await client.send_message(LOG_CHANNEL, log_text)
            except Exception as e:
                print(f"Log Error: {e}")

    buttons = [
        [
            InlineKeyboardButton("ℹ️ ʜᴇʟᴘ", callback_data="help"),
            InlineKeyboardButton("👨‍💻 ᴀʙᴏᴜᴛ", callback_data="about")
        ],
        [
            InlineKeyboardButton("📢 ᴜᴘᴅᴀᴛᴇs", url=CHANNEL),
            InlineKeyboardButton("💬 sᴜᴘᴘᴏʀᴛ", url=SUPPORT)
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(buttons)

    if START_PIC:
        await message.reply_photo(
            photo=START_PIC,
            caption=script.START_TXT.format(mention, APP_URL),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    else:
        await message.reply_text(
            text=script.START_TXT.format(mention, APP_URL),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )

@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    data = query.data
    
    if data == "close_data":
        await query.message.delete()

    elif data == "about":
        buttons = [[
            InlineKeyboardButton('💻 sᴏᴜʀᴄᴇ ᴄᴏᴅᴇ', url='https://github.com/SayaTeam')
        ],[
            InlineKeyboardButton('🏠 ʜᴏᴍᴇ', callback_data='start'),
            InlineKeyboardButton('✖️ ᴄʟᴏsᴇ', callback_data='close_data')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        
        if query.message.photo:
            await query.message.edit_caption(
                caption=script.ABOUT_TXT.format(temp.B_NAME, temp.B_NAME),
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML
            )
        else:
            await query.message.edit_text(
                text=script.ABOUT_TXT.format(temp.B_NAME, temp.B_NAME),
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML
            )
    
    elif data == "start":
        buttons = [
            [
                InlineKeyboardButton("ℹ️ ʜᴇʟᴘ", callback_data="help"),
                InlineKeyboardButton("👨‍💻 ᴀʙᴏᴜᴛ", callback_data="about")
            ],
            [
                InlineKeyboardButton("📢 ᴜᴘᴅᴀᴛᴇs", url=CHANNEL),
                InlineKeyboardButton("💬 sᴜᴘᴘᴏʀᴛ", url=SUPPORT)
            ]
        ]
        reply_markup = InlineKeyboardMarkup(buttons)
        
        if query.message.photo:
            await query.message.edit_caption(
                caption=script.START_TXT.format(query.from_user.mention, APP_URL),
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML
            )
        else:
            await query.message.edit_text(
                text=script.START_TXT.format(query.from_user.mention, APP_URL),
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML
            )
        
    elif data == "help":
        buttons = [[
            InlineKeyboardButton('👮‍♂️ ᴀᴅᴍɪɴ', callback_data='admin-help')
        ],[
            InlineKeyboardButton('🏠 ʜᴏᴍᴇ', callback_data='start'),
            InlineKeyboardButton('✖️ ᴄʟᴏsᴇ', callback_data='close_data')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        
        if query.message.photo:
            await query.message.edit_caption(
                caption=script.HELP_TXT,
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML
            )
        else:
            await query.message.edit_text(
                text=script.HELP_TXT,
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML
            )
          
    elif data == "admin-help":
        if not query.from_user.id in ADMINS:
            return await query.answer('Tʜɪs Fᴇᴀᴛᴜʀᴇ Is Oɴʟʏ Fᴏʀ Aᴅᴍɪɴ !' , show_alert=True)
        buttons = [[
            InlineKeyboardButton('🏠 ʜᴏᴍᴇ', callback_data='start')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        
        if query.message.photo:
            await query.message.edit_caption(
                caption=script.ADMIN_HELP_TXT,
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML
            )
        else:
            await query.message.edit_text(
                text=script.ADMIN_HELP_TXT,
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML
    )
                                     
