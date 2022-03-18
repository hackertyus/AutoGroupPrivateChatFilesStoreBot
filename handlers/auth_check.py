# (c) @AbirHasan2005 & @HuzunluArtemis

from configs import Config

async def AuthCheck(chat_id: int, user_id: int):
    if 0 in Config.AUTH_IDS:
        return True
    elif user_id in Config.AUTH_IDS:
        return True
    elif chat_id in Config.AUTH_IDS:
        return True
    else:
        print("AuthCheck - nothing found. returning false. if you did somethign wrong, read all readme")
        return False
        
