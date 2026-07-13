import os
import time
from aiohttp import web
from pyrogram import enums
from info import LOG_CHANNEL
from utils import upload_to_catbox, upload_to_uguu, temp
from database.users_db import db

routes = web.RouteTableDef()

@routes.get("/", allow_head=True)
async def root_route_handler(request):
    # FIX: Yahan pehle get_upload_mode() tha, jo galat tha.
    # Ab ye sahi function call kar raha hai jo True/False return karega.
    maintenance_mode = await db.get_maintenance_mode()
    
    if maintenance_mode: 
        return web.Response(text="🚧 Site is Under Maintenance. Please try again later.", status=503)
    return web.FileResponse("templates/upload.html")

@routes.post("/upload")
async def upload_route_handler(request):
    # FIX: Yahan bhi same fix kiya hai maintenance check ke liye
    maintenance_mode = await db.get_maintenance_mode()
    
    if maintenance_mode: 
        return web.Response(text="🚧 Maintenance Mode Active", status=503)
    
    
    
    # Yahan humein actual upload mode chahiye (catbox/uguu)
    upload_mode = await db.get_upload_mode()
    filename = None
    try:
        reader = await request.multipart()
        field = await reader.next()
        if not field: return web.Response(text="❌ No file selected", status=400)
        
        filename = f"web_upload_{int(time.time())}_{field.filename}"
        with open(filename, 'wb') as f:
            while True:
                chunk = await field.read_chunk()
                if not chunk: break
                f.write(chunk)
        
        link = None
        if upload_mode == "uguu":
            link = await upload_to_uguu(filename)
            if not link: link = await upload_to_catbox(filename)
        else:
            link = await upload_to_catbox(filename)
            if not link: link = await upload_to_uguu(filename)

        

        if link:
            await db.add_web_upload()
            client = request.app.get('bot_client')
            if client and LOG_CHANNEL:
                try:
                    # Log message mein current server show karne ke liye logic update
                    server_name = upload_mode.upper() if upload_mode else temp.UPLOAD_MODE.upper()
                    
                    log_text = f"<b>#WebUpload</b>\n\n<b>👤 ᴜsᴇʀ :</b> <code>Website User</code>\n<b>🔗 ʟɪɴᴋ :</b> <code>{link}</code>\n<b>⚙️ sᴇʀᴠᴇʀ :</b> <code>{server_name}</code>\n<b>🕒 ᴛɪᴍᴇ :</b> <code>{time.strftime('%Y-%m-%d %H:%M:%S')}</code>"
                    await client.send_message(chat_id=LOG_CHANNEL, text=log_text, parse_mode=enums.ParseMode.HTML, disable_web_page_preview=True)
                except Exception: pass
            
            template_path = os.path.join(os.getcwd(), "templates", "result.html")
            with open(template_path, "r", encoding="utf-8") as f: html_content = f.read()
            final_html = html_content.replace("REPLACELINK", link)
            return web.Response(text=final_html, content_type='text/html')
        else:
            return web.Response(text="❌ Upload Failed on both servers.", status=500)
    except Exception as e:
        return web.Response(text=f"❌ Error: {str(e)}", status=500)
    finally:
        if filename and os.path.exists(filename): os.remove(filename)

async def web_server(client):
    web_app = web.Application(client_max_size=30000000)
    web_app['bot_client'] = client
    web_app.add_routes(routes)
    return web_app
    
