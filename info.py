from os import environ

def str_to_bool(val):
    return str(val).lower() in {"true", "yes", "1", "t", "y"}

API_ID = int(environ.get('API_ID', '80656'))
API_HASH = environ.get('API_HASH', 'd927c13beaaf5110f27c071273')
BOT_TOKEN = environ.get("BOT_TOKEN", "85449448:AAFWldQobm7UhOqH7WPFaSc9bulEWk")
PORT = environ.get("PORT", "8080")
START_PIC = environ.get("START_PIC", "https://files.catbox.moe/gbuf6w.jpg")

ADMINS = list(map(int, environ.get("ADMINS", "5940554521").split()))
LOG_CHANNEL = int(environ.get("LOG_CHANNEL", "-1004334280347"))
DB_URL = environ.get('DATABASE_URI', "mongodb+srv://-TOT:IMGT@cluster0.1rr6x.mongodb.net/?appName=Cluster0")

AUTH_CHANNEL = list(map(int, environ.get("AUTH_CHANNEL", "-1003372208272 -1003372208272").split()))
AUTH_REQ_CHANNEL = list(map(int, environ.get("AUTH_REQ_CHANNELS", "-1003372208272").split()))
FSUB = str_to_bool(environ.get("FSUB", "True"))
AUTH_PICS = environ.get("AUTH_PICS", "https://files.catbox.moe/gbuf6w.jpg")
CHANNEL = environ.get("CHANNEL", "https://t.me/SayaProject")
SUPPORT = environ.get("SUPPORT", "https://t.me/SayaProject")
APP_URL = environ.get("APP_URL", "https://manual-nikolia-totzvvv-5115e05f.koyeb.app/")

