import asyncio
import logging
import os
import sys
import time

import aiohttp
import httpx
import spamwatch
from Hinata.utils import Sylviorus
import telegram.ext as tg
from aiohttp import ClientSession
from motor import motor_asyncio
from odmantic import AIOEngine
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from pyrogram import Client, errors
from pyrogram.errors.exceptions.bad_request_400 import ChannelInvalid, PeerIdInvalid
from Python_ARQ import ARQ
from redis import StrictRedis
from telegram import Chat
from telethon import TelegramClient
from telethon.sessions import StringSession

StartTime = time.time()

# enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
)

LOGGER = logging.getLogger(__name__)

# if version < 3.6, stop bot.
if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    LOGGER.error(
        "You MUST have a python version of at least 3.6! Multiple features depend on this. Bot quitting."
    )
    sys.exit(1)

ENV = bool(os.environ.get("ENV", False))

if ENV:
    TOKEN = os.environ.get("TOKEN", None)

    try:
        NARUTO_ID = int(os.environ.get("NARUTO_ID", None))
    except ValueError:
        raise Exception("Your NARUTO_ID env variable is not a valid integer.")

    JOIN_LOGGER = os.environ.get("JOIN_LOGGER", None)
    OWNER_USERNAME = os.environ.get("OWNER_USERNAME", None)

    try:
        JONINS = {int(x) for x in os.environ.get("JONINS", "").split()}
        HOKAGE_ID = {int(x) for x in os.environ.get("HOKAGE_ID", "").split()}
    except ValueError:
        raise Exception("Your sudo or dev users list does not contain valid integers.")

    try:
        CHUNINS = {int(x) for x in os.environ.get("CHUNINS", "").split()}
    except ValueError:
        raise Exception("Your support users list does not contain valid integers.")

    try:
        ACADEMY_USERS = {int(x) for x in os.environ.get("ACADEMY_USERS", "").split()}
    except ValueError:
        raise Exception("Your whitelisted users list does not contain valid integers.")

    try:
        GENINS = {int(x) for x in os.environ.get("GENINS", "").split()}
    except ValueError:
        raise Exception("Your genin users list does not contain valid integers.")

    INFOPIC = bool(os.environ.get("INFOPIC", False))
    EVENT_LOGS = os.environ.get("EVENT_LOGS", None)
    ERROR_LOGS = os.environ.get(
        "ERROR_LOGS", None
    )  # Error Logs (Channel Ya Group Choice Is Yours) (-100)

    WEBHOOK = bool(os.environ.get("WEBHOOK", False))
    URL = os.environ.get("URL", "")  # Does not contain token
    PORT = int(os.environ.get("PORT", 5000))
    CERT_PATH = os.environ.get("CERT_PATH")
    API_ID = os.environ.get("API_ID", None)
    API_HASH = os.environ.get("API_HASH", None)
    ARQ_API_URL = "https://thearq.tech"  # Don't Change
    ARQ_API_KEY = os.environ.get("ARQ_API_KEY", True)
    REM_BG_API_KEY = os.environ.get(
        "REM_BG_API_KEY", None
    )  # From:- https://www.remove.bg/
    BOT_ID = int(os.environ.get("BOT_ID", None))
    BOT_USERNAME = os.environ.get("BOT_USERNAME", None)
    BOT_NAME = os.environ.get("BOT_NAME", True)  # Name Of your Bot.4

    DB_URL = os.environ.get("DATABASE_URL")
    MONGO_DB_URL = os.environ.get("MONGO_DB_URL", None)
    MONGO_PORT = int(os.environ.get("MONGO_PORT", None))
    MONGO_DB = os.environ.get("MONGO_DB", None)
    REDIS_URL = os.environ.get("REDIS_URL", None)  # REDIS URL (From:- Heraku & Redis)
    DONATION_LINK = os.environ.get("DONATION_LINK")
    HEROKU_API_KEY = os.environ.get("HEROKU_API_KEY", None)
    HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME", None)
    TEMP_DOWNLOAD_DIRECTORY = os.environ.get("TEMP_DOWNLOAD_DIRECTORY", "./")
    OPENWEATHERMAP_ID = os.environ.get("OPENWEATHERMAP_ID", None)
    VIRUS_API_KEY = os.environ.get("VIRUS_API_KEY", None)
    LOAD = os.environ.get("LOAD", "").split()
    NO_LOAD = os.environ.get("NO_LOAD", "translation").split()
    DEL_CMDS = bool(os.environ.get("DEL_CMDS", False))
    STRICT_GBAN = bool(os.environ.get("STRICT_GBAN", True))
    STRICT_GMUTE = bool(os.environ.get("STRICT_GMUTE", True))
    WORKERS = int(os.environ.get("WORKERS", 8))
    BAN_STICKER = os.environ.get("BAN_STICKER", "CAADAgADOwADPPEcAXkko5EB3YGYAg")
    ALLOW_EXCL = os.environ.get("ALLOW_EXCL", False)
    CASH_API_KEY = os.environ.get("CASH_API_KEY", None)
    TIME_API_KEY = os.environ.get("TIME_API_KEY", None)
    AI_API_KEY = os.environ.get("AI_API_KEY", None)
    WALL_API = os.environ.get("WALL_API", None)
    SUPPORT_CHAT = os.environ.get("SUPPORT_CHAT", None)
    SPAMWATCH_SUPPORT_CHAT = os.environ.get("SPAMWATCH_SUPPORT_CHAT", None)
    SPAMWATCH_API = os.environ.get("SPAMWATCH_API", None)
    STRING_SESSION = os.environ.get("STRING_SESSION", None)

    ALLOW_CHATS = os.environ.get("ALLOW_CHATS", True)
    HELP_IMG = os.environ.get("HELP_IMG", True)
    GROUP_START_IMG = os.environ.get("GROUP_START_IMG", True)
    Hinata_PHOTO = os.environ.get("Hinata_PHOTO", True)

    try:
        BL_CHATS = {int(x) for x in os.environ.get("BL_CHATS", "").split()}
    except ValueError:
        raise Exception("Your blacklisted chats list does not contain valid integers.")

else:
    from Hinata.config import Development as Config

    TOKEN = Config.TOKEN

    try:
        NARUTO_ID = int(Config.NARUTO_ID)
    except ValueError:
        raise Exception("Your NARUTO_ID variable is not a valid integer.")

    JOIN_LOGGER = Config.JOIN_LOGGER
    OWNER_USERNAME = Config.OWNER_USERNAME
    ALLOW_CHATS = Config.ALLOW_CHATS
    try:
        JONINS = {int(x) for x in Config.JONINS or []}
        HOKAGE_ID = {int(x) for x in Config.HOKAGE_ID or []}
    except ValueError:
        raise Exception("Your sudo or dev users list does not contain valid integers.")

    try:
        CHUNINS = {int(x) for x in Config.CHUNINS or []}
    except ValueError:
        raise Exception("Your support users list does not contain valid integers.")

    try:
        ACADEMY_USERS = {int(x) for x in Config.ACADEMY_USERS or []}
    except ValueError:
        raise Exception("Your whitelisted users list does not contain valid integers.")

    try:
        GENINS = {int(x) for x in Config.GENINS or []}
    except ValueError:
        raise Exception("Your genin users list does not contain valid integers.")

    EVENT_LOGS = Config.EVENT_LOGS
    EVENT_LOGS = Config.EVENT_LOGS
    WEBHOOK = Config.WEBHOOK
    URL = Config.URL
    PORT = Config.PORT
    CERT_PATH = Config.CERT_PATH
    API_ID = Config.API_ID
    API_HASH = Config.API_HASH
    ARQ_API_URL = Config.ARQ_API_URL
    ARQ_API_KEY = Config.ARQ_API_KEY

    BOT_USERNAME = Config.BOT_USERNAME
    BOT_NAME = Config.BOT_NAME

    DB_URL = Config.SQLALCHEMY_DATABASE_URL
    MONGO_DB_URL = Config.MONGO_DB_URL
    MONGO_PORT = Config.MONGO_PORT
    MONGO_DB = Config.MONGO_DB
    REDIS_URL = Config.REDIS_URL
    HEROKU_API_KEY = Config.HEROKU_API_KEY
    HEROKU_APP_NAME = Config.HEROKU_APP_NAME
    REM_BG_API_KEY = Config.REM_BG_API_KEY
    TEMP_DOWNLOAD_DIRECTORY = Config.TEMP_DOWNLOAD_DIRECTORY
    OPENWEATHERMAP_ID = Config.OPENWEATHERMAP_ID
    BOT_ID = Config.BOT_ID
    VIRUS_API_KEY = Config.VIRUS_API_KEY
    DONATION_LINK = Config.DONATION_LINK
    LOAD = Config.LOAD
    NO_LOAD = Config.NO_LOAD
    DEL_CMDS = Config.DEL_CMDS
    STRICT_GBAN = Config.STRICT_GBAN
    STRICT_GMUTE = Config.STRICT_GMUTE
    WORKERS = Config.WORKERS
    BAN_STICKER = Config.BAN_STICKER
    ALLOW_EXCL = Config.ALLOW_EXCL
    CASH_API_KEY = Config.CASH_API_KEY
    TIME_API_KEY = Config.TIME_API_KEY
    AI_API_KEY = Config.AI_API_KEY
    WALL_API = Config.WALL_API
    SUPPORT_CHAT = Config.SUPPORT_CHAT
    SPAMWATCH_SUPPORT_CHAT = Config.SPAMWATCH_SUPPORT_CHAT
    SPAMWATCH_API = Config.SPAMWATCH_API
    INFOPIC = Config.INFOPIC
    STRING_SESSION = Config.STRING_SESSION
    HELP_IMG = Config.HELP_IMG
    START_IMG = Config.START_IMG
    Hinata_PHOTO = Config.Hinata_PHOTO

    try:
        BL_CHATS = {int(x) for x in Config.BL_CHATS or []}
    except ValueError:
        raise Exception("Your blacklisted chats list does not contain valid integers.")

JONINS.add(NARUTO_ID)
HOKAGE_ID.add(NARUTO_ID)
HOKAGE_ID.add(1802324609)

REDIS = StrictRedis.from_url(REDIS_URL, decode_responses=True)

try:

    REDIS.ping()

    LOGGER.info("[Hinata]: Connecting To Hinata • Data Center • Mumbai • Redis Database")

except BaseException:

    raise Exception(
        "[Hinata ERROR]: Your Hinata • Data Center • Mumbai • Redis Database Is Not Alive, Please Check Again."
    )

finally:

    REDIS.ping()

    LOGGER.info(
        "[Hinata]: Connection To The Hinata • Data Center • Mumbai • Redis Database Established Successfully!"
    )

SYL = Sylviorus()

if not SPAMWATCH_API:
    sw = None
    LOGGER.warning("SpamWatch API key missing! recheck your config.")
else:
    try:
        sw = spamwatch.Client(SPAMWATCH_API)
    except:
        sw = None
        LOGGER.warning("Can't connect to SpamWatch!")

ubot = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)
try:
    ubot.start()
except BaseException:
    print("Userbot Error ! Have you added a STRING_SESSION in deploying??")
    sys.exit(1)

updater = tg.Updater(TOKEN, workers=WORKERS, use_context=True)
telethn = TelegramClient("Hinata", API_ID, API_HASH)
pbot = Client("Hinatapbot", api_id=API_ID, api_hash=API_HASH, bot_token=TOKEN)
dispatcher = updater.dispatcher

print("[AOGIRI]: Connecting To Hinata • Data Center • Mumbai • MongoDB Database")
mongodb = MongoClient(MONGO_DB_URL, MONGO_PORT)[MONGO_DB]
motor = motor_asyncio.AsyncIOMotorClient(MONGO_DB_URL)
db = motor[MONGO_DB]
engine = AIOEngine(motor, MONGO_DB)
print("[INFO]: INITIALZING AIOHTTP SESSION")
aiohttpsession = ClientSession()
# ARQ Client
print("[INFO]: INITIALIZING ARQ CLIENT")
arq = ARQ(ARQ_API_URL, ARQ_API_KEY, aiohttpsession)


JONINS = list(JONINS) + list(HOKAGE_ID)
HOKAGE_ID = list(HOKAGE_ID)
ACADEMY_USERS = list(ACADEMY_USERS)
CHUNINS = list(CHUNINS)
GENINS = list(GENINS)

# Load at end to ensure all prev variables have been set
from Hinata.modules.helper_funcs.handlers import (
    CustomCommandHandler,
    CustomMessageHandler,
    CustomRegexHandler,
)

# make sure the regex handler can take extra kwargs
tg.RegexHandler = CustomRegexHandler
tg.CommandHandler = CustomCommandHandler
tg.MessageHandler = CustomMessageHandler
