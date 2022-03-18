# (c) @AbirHasan2005 & @HuzunluArtemis

import os

# If it works on a cloud platform like heroku, you can use enviroment variables.
# If you use environmental variables, you should not make any changes to this file.

class Config(object):
    # if you will use enviroment variable, dont touch anything from here.
    DEFAULT_BLOCKED_EXTENSIONS = "srt txt html aio pdf lnk url"
    # DEFAULT_BLOCKED_EXTENSIONS = "srt txt jpg jpeg png torrent html aio pdf"
    
    
    #
    BOT_TOKEN = os.environ.get('BOT_TOKEN', '')
    API_ID = int(os.environ.get('API_ID', 1111111))
    API_HASH = os.environ.get('API_HASH', None)
    STRING_SESSION = os.environ.get("STRING_SESSION", None)
    DB_CHANNEL_ID = int(os.environ.get('DB_CHANNEL_ID', ''))
    FORCE_SUB_CHANNEL = os.environ.get('FORCE_SUB_CHANNEL', None)
    MONGODB_URI = os.environ.get('MONGODB_URI', '')
    BLOCKED_EXTENSIONS = list(set(x for x in os.environ.get("BLOCKED_EXTENSIONS", DEFAULT_BLOCKED_EXTENSIONS).split()))
    BOT_USERNAME = os.environ.get('BOT_USERNAME', 'SaverBot')
    MIN_FILE_SIZE = int(os.environ.get('MIN_FILE_SIZE', 0)) # for save everything:0 for save nothing:200000 5242880
    SEND_AS_COPY = os.environ.get('SEND_AS_COPY', True) # if you want to send files to users as a copy
    SAVE_AS_COPY = os.environ.get('SAVE_AS_COPY', True) # if you want to save files to db as a copy
    CONTACT_ADRESS = os.environ.get('CONTACT_ADRESS', None)
    URL_PREFIX = os.environ.get('URL_PREFIX', 'HA')
    AUTO_DELETE = os.environ.get('AUTO_DELETE', True)
    AUTO_DELETE_TIME = int(os.environ.get('AUTO_DELETE_TIME', 10))
    AUTO_KICK_TIME = int(os.environ.get('AUTO_KICK_TIME', 10))
    ACCEPT_FROM_PRIVATE = os.environ.get('ACCEPT_FROM_PRIVATE', False)
    DELETE_SENT_MESSAGE = os.environ.get('DELETE_SENT_MESSAGE', False) # delete bots message
    DELETE_SENT_MESSAGE_TIME = int(os.environ.get('DELETE_SENT_MESSAGE_TIME', 60))
    DELETE_SENT_FILE = os.environ.get('DELETE_SENT_FILE', False) # delete bot send message
    DELETE_SENT_FILE_TIME = int(os.environ.get('DELETE_SENT_FILE_TIME', 60))
    START_MESSAGE = os.environ.get('START_MESSAGE', "Bot is running.")
    SKIP_SAVED_INFO_MESSAGE = os.environ.get('SKIP_SAVED_INFO_MESSAGE', False)
    USE_BUTTON_FOR_LINK = os.environ.get('USE_BUTTON_FOR_LINK', True)
    BUTTON_FOR_LINK_STR = os.environ.get('USE_BUTTON_FOR_LINK', "👉 Tıkla")
    SEND_LINK_AGAIN = os.environ.get('SEND_LINK_AGAIN', True)
    USE_BOT_INSTEAD_USER = os.environ.get('USE_BOT_INSTEAD_USER', True)
    AUTH_IDS = [int(x) for x in os.environ.get("AUTH_IDS", "0").split()] # 0 = everyone
    ONLY_BOT_MODE = os.environ.get('ONLY_BOT_MODE', False)

    # if you want to config from here, uncomment this lines and edit:

    # BOT_TOKEN = "315269696969:sdv31imamhatiplerhapatılsın-dfg"
    # API_ID = 313131
    # API_HASH = "sdfsdfvssv65s56v"
    # STRING_SESSION = "asdf+63sadf+6sadf26sadf262asdf"
    # DB_CHANNEL_ID = -100232626
    # FORCE_SUB_CHANNEL = "@HuzunluArtemis" # example: -10026526 example: @HuzunluArtemis
    # MONGODB_URI = "mongodb+srv://hgg-gh-h:ghg@fghfgh.fgh.mongodb.net/fhgfh?retryWrites=true&w=majority"
    # BLOCKED_EXTENSIONS = "srt txt html aio pdf lnk url"
    # BOT_USERNAME = "SaverBot"
    # MIN_FILE_SIZE = 0 # for save everything:0 for save nothing:200000 5242880
    # SEND_AS_COPY = True # if you want to send files to users as a copy
    # SAVE_AS_COPY = True # if you want to save files to db as a copy
    # CONTACT_ADRESS = "@HuzunluArtemis"
    # URL_PREFIX = "HA"
    # AUTO_DELETE = True
    # AUTO_DELETE_TIME = 10
    # AUTO_KICK_TIME = 10
    # ACCEPT_FROM_PRIVATE = False
    # DELETE_SENT_MESSAGE = os.environ.get('DELETE_SENT_MESSAGE', False) # delete bots message
    # DELETE_SENT_MESSAGE_TIME = int(os.environ.get('DELETE_SENT_MESSAGE_TIME', 60))
    # DELETE_SENT_FILE = os.environ.get('DELETE_SENT_FILE', False) # delete bot send message
    # DELETE_SENT_FILE_TIME = int(os.environ.get('DELETE_SENT_FILE_TIME', 60))
    # START_MESSAGE = "Bot is running."
    # SKIP_SAVED_INFO_MESSAGE = False
    # USE_BUTTON_FOR_LINK = True
    # BUTTON_FOR_LINK_STR = "🇬🇧 Click Me / 🇹🇷 Bana Tıkla"
    # SEND_LINK_AGAIN = True
    # USE_BOT_INSTEAD_USER = True
    # AUTH_IDS = "-100428772 1242 785785 -757575" # sadece "0" verirseniz herkese açık hale gelir.
    # ONLY_BOT_MODE = False


    # dont touch this lines
    if STRING_SESSION is None: ONLY_BOT_MODE = True 
    if CONTACT_ADRESS is not None and CONTACT_ADRESS is not "" and CONTACT_ADRESS is not " ":
        START_MESSAGE += f"\n\n💎 {CONTACT_ADRESS}"
