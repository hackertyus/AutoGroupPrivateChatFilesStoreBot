# (c) @AbirHasan2005 & @HuzunluArtemis

import asyncio
from pyrogram import Client, filters, idle
import pyrogram
from pyrogram.errors import UserNotParticipant
from pyrogram.types import Message, ChatPermissions
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from configs import Config
from handlers.database.access_db import db
from handlers.forcesub_handler import ForceSub
from handlers.forwarder_handler import forwardMessage
from handlers.send_mesage_handler import sendMessage
from handlers.database.add_user import AddUserToDatabase
from handlers.auth_check import AuthCheck

if not Config.ONLY_BOT_MODE:
    User = Client( session_name=Config.STRING_SESSION, api_id=Config.API_ID,  api_hash=Config.API_HASH)
Bot = Client( session_name="Auto Group - Private Chat Files Store Bot", api_id=Config.API_ID, api_hash=Config.API_HASH, bot_token=Config.BOT_TOKEN)

# Start User Client
if not Config.ONLY_BOT_MODE:
    User.start()
    print("Userbot Started!")
# Start Bot Client
Bot.start()
print("Bot Started!")
# Loop Clients till Disconnects

def humanbytes(size):
    # https://stackoverflow.com/a/49361727/4723940
    # 2**10 = 1024
    if not size:
        return ""
    power = 2 ** 10
    n = 0
    Dic_powerN = {0: " ", 1: "K", 2: "M", 3: "G", 4: "T"}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n] + "B"

@Bot.on_message(filters.private & (filters.document | filters.video | filters.audio | filters.photo | filters.voice))
async def private_handler(bot: Client, cmd: Message):
    if not await AuthCheck(cmd.chat.id, cmd.from_user.id):
        print("not authorized chat. read readme!")
        return
    if Config.ACCEPT_FROM_PRIVATE:
        # take caption of message +
        caption = None
        try:
            caption = cmd.caption
        except:
            caption = None
        # take caption of message -
        media = cmd.document or cmd.video or cmd.audio or cmd.photo or cmd.voice
        try:
            comingfilename = media.file_name
            if comingfilename.rsplit(".", 1)[-1] in Config.BLOCKED_EXTENSIONS:
                return
        except AttributeError:
            comingfilename = None
        if media.file_size < int(Config.MIN_FILE_SIZE):
            return
        if (Config.FORCE_SUB_CHANNEL is not None) and (cmd.from_user.is_bot is False):
            await AddUserToDatabase(cmd)
            Fsub = await ForceSub(Bot, cmd)
            if Fsub == 400:
                await db.set_joined_channel(cmd.from_user.id, joined_channel=False)
                await db.set_group_id(cmd.from_user.id, group_id=cmd.chat.id)
                try:
                    await bot.restrict_chat_member(
                        chat_id=cmd.chat.id,
                        user_id=cmd.from_user.id,
                        permissions=ChatPermissions(can_send_messages=False)
                    )
                except:
                    pass
                return
            elif Fsub == 404:
                try:
                    await bot.kick_chat_member(chat_id=cmd.chat.id, user_id=cmd.from_user.id)
                except:
                    pass
            else:
                await db.delete_user(cmd.from_user.id)
        #
        forward = await forwardMessage(cmd)
        
        size = humanbytes(media.file_size)
        if Config.AUTO_DELETE:
            text = ""
            if not Config.SKIP_SAVED_INFO_MESSAGE:
                text += f"""
Bu dosya {Config.AUTO_DELETE_TIME} saniye içinde silinecektir\nAncak veritabanında saklanacaktır!"""
            text += "\n"
            text += f"""
🌈 File: `{comingfilename}`
🍏 Size: `{size}`
🐇 Caption: `{caption}`
[☀️ Link](https://t.me/{Config.BOT_USERNAME}?start={Config.URL_PREFIX}_{str(forward.message_id)}): `https://t.me/{Config.BOT_USERNAME}?start={Config.URL_PREFIX}_{str(forward.message_id)}`"""
            if Config.DELETE_SENT_MESSAGE:
                text += f"\n\nAyrıca bu mesaj da {str(Config.DELETE_SENT_MESSAGE_TIME)} saniye sonra silinecek. yedeklersen iyi olur."
            if Config.USE_BUTTON_FOR_LINK:
                sentmessage = await sendMessage(
                    bot=bot,
                    message_id=cmd.message_id,
                    chat_id=cmd.chat.id,
                    text=text,
                    reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton(Config.BUTTON_FOR_LINK_STR, url=f"https://t.me/{Config.BOT_USERNAME}?start={Config.URL_PREFIX}_{str(forward.message_id)}")]
                    ])
                )
            else:
                sentmessage = await sendMessage(
                    bot=bot,
                    message_id=cmd.message_id,
                    chat_id=cmd.chat.id,
                    text=text
                )
            await asyncio.sleep(int(Config.AUTO_DELETE_TIME))
            try:
                await cmd.delete(True)
            except Exception as err:
                await sendMessage(
                bot=bot,
                message_id=cmd.message_id,
                chat_id=cmd.chat.id,
                text=f"Unable to Delete Media Message!\nError: {err}\n\nMessage ID: {cmd.message_id}"
            )
        #
        else:
            text = f"""
🌈 File: `{comingfilename}`
🍏 Size: `{size}`
🐇 Caption: `{caption}`
[☀️ Link](https://t.me/{Config.BOT_USERNAME}?start={Config.URL_PREFIX}_{str(forward.message_id)}): `https://t.me/{Config.BOT_USERNAME}?start={Config.URL_PREFIX}_{str(forward.message_id)}`"""
            if Config.DELETE_SENT_MESSAGE:
                text += f"\n\nAyrıca bu mesaj da {str(Config.DELETE_SENT_MESSAGE_TIME)} saniye sonra silinecek. yedeklersen iyi olur."
            if Config.USE_BUTTON_FOR_LINK:
                sentmessage = await sendMessage(
                    bot=bot,
                    message_id=cmd.message_id,
                    chat_id=cmd.chat.id,
                    text=text,
                    reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton(Config.BUTTON_FOR_LINK_STR, url=f"https://t.me/{Config.BOT_USERNAME}?start={Config.URL_PREFIX}_{str(forward.message_id)}")]
                    ])
                )
            else:
                sentmessage = await sendMessage(
                    bot=bot,
                    message_id=cmd.message_id,
                    chat_id=cmd.chat.id,
                    text=text
                )
        if Config.DELETE_SENT_MESSAGE:
            await asyncio.sleep(int(Config.DELETE_SENT_MESSAGE_TIME))
            await sentmessage.delete(True)
        #
        
        #            




if not Config.ONLY_BOT_MODE:
    @User.on_message(filters.group & (filters.document | filters.video | filters.audio))
    async def files_handler(bot: Client, cmd: Message):
        if not await AuthCheck(cmd.chat.id, cmd.from_user.id):
            print("not authorized chat. read readme!")
            return
        # take caption of message +
        caption = None
        try:
            caption = cmd.caption
        except:
            caption = None
        # take caption of message -
        media = cmd.document or cmd.video or cmd.audio
        if not cmd.from_user.is_bot:
            if cmd.edit_date is not None:
                return
        try:
            cammingfilename = media.file_name
            if cammingfilename.rsplit(".", 1)[-1] in Config.BLOCKED_EXTENSIONS:
                return
        except:
            cammingfilename = None
        if media.file_size < int(Config.MIN_FILE_SIZE):
            return
        if (Config.FORCE_SUB_CHANNEL is not None) and (cmd.from_user.is_bot is False):
            await AddUserToDatabase(cmd)
            Fsub = await ForceSub(Bot, cmd)
            if Fsub == 400:
                await db.set_joined_channel(cmd.from_user.id, joined_channel=False)
                await db.set_group_id(cmd.from_user.id, group_id=cmd.chat.id)
                try:
                    await bot.restrict_chat_member(
                        chat_id=cmd.chat.id,
                        user_id=cmd.from_user.id,
                        permissions=ChatPermissions(can_send_messages=False)
                    )
                except:
                    pass
                return
            elif Fsub == 404:
                try:
                    await bot.kick_chat_member(chat_id=cmd.chat.id, user_id=cmd.from_user.id)
                except:
                    pass
            else:
                await db.delete_user(cmd.from_user.id)
        #
        forward = await forwardMessage(cmd)
        
        #
        size = humanbytes(media.file_size)
        if Config.AUTO_DELETE:
            text = ""
            if not Config.SKIP_SAVED_INFO_MESSAGE:
                text += f"""
Bu dosya {Config.AUTO_DELETE_TIME} saniye içinde silinecektir\nAncak veritabanında saklanacaktır!"""
            text += "\n"
            text += f"""
🌈 File: `{cammingfilename}`
🍏 Size: `{size}`
🐇 Caption: `{caption}`
[☀️ Link](https://t.me/{Config.BOT_USERNAME}?start={Config.URL_PREFIX}_{str(forward.message_id)}): `https://t.me/{Config.BOT_USERNAME}?start={Config.URL_PREFIX}_{str(forward.message_id)}`"""
            #
            if Config.DELETE_SENT_MESSAGE:
                text += f"\n\nAyrıca bu mesaj da {str(Config.DELETE_SENT_MESSAGE_TIME)} saniye sonra silinecek. yedeklersen iyi olur."
            if Config.USE_BUTTON_FOR_LINK:
                # try buttons
                if Config.USE_BOT_INSTEAD_USER:
                    sentmessage = await sendMessage(
                        bot=Bot,
                        message_id=cmd.message_id,
                        chat_id=cmd.chat.id,
                        text=text,
                        reply_markup=InlineKeyboardMarkup(
                        [
                            [InlineKeyboardButton(Config.BUTTON_FOR_LINK_STR, url=f"https://t.me/{Config.BOT_USERNAME}?start={Config.URL_PREFIX}_{str(forward.message_id)}")]
                        ])
                    )
                else:
                    sentmessage = await sendMessage(
                            bot=bot,
                            message_id=cmd.message_id,
                            chat_id=cmd.chat.id,
                            text=text,
                            reply_markup=InlineKeyboardMarkup(
                            [
                                [InlineKeyboardButton(Config.BUTTON_FOR_LINK_STR, url=f"https://t.me/{Config.BOT_USERNAME}?start={Config.URL_PREFIX}_{str(forward.message_id)}")]
                            ])
                        )
            else:
                if Config.USE_BOT_INSTEAD_USER:
                    sentmessage = await sendMessage(
                        bot=Bot,
                        message_id=cmd.message_id,
                        chat_id=cmd.chat.id,
                        text=text
                    )
                else:
                    sentmessage = await sendMessage(
                        bot=bot,
                        message_id=cmd.message_id,
                        chat_id=cmd.chat.id,
                        text=text
                    )
            #
            await asyncio.sleep(int(Config.AUTO_DELETE_TIME))
            try:
                await cmd.delete(True)
            except Exception as err:
                if Config.USE_BOT_INSTEAD_USER:
                    await sendMessage(
                    bot=Bot,
                    message_id=cmd.message_id,
                    chat_id=cmd.chat.id,
                    text=f"Unable to Delete Media Message!\nError: {err}\n\nMessage ID: {cmd.message_id}")
                else:
                    await sendMessage(
                    bot=bot,
                    message_id=cmd.message_id,
                    chat_id=cmd.chat.id,
                    text=f"Unable to Delete Media Message!\nError: {err}\n\nMessage ID: {cmd.message_id}")
            #
        else:
            text = f"""
🌈 File: `{cammingfilename}`
🍏 Size: `{size}`
🐇 Caption: `{caption}`
[☀️ Link](https://t.me/{Config.BOT_USERNAME}?start={Config.URL_PREFIX}_{str(forward.message_id)}): `https://t.me/{Config.BOT_USERNAME}?start={Config.URL_PREFIX}_{str(forward.message_id)}`"""
            #
            if Config.DELETE_SENT_MESSAGE:
                text += f"\n\nAyrıca bu mesaj da {str(Config.DELETE_SENT_MESSAGE_TIME)} saniye sonra silinecek. yedeklersen iyi olur."
            if Config.USE_BUTTON_FOR_LINK:
                if Config.USE_BOT_INSTEAD_USER:
                    sentmessage = await sendMessage(
                        bot=Bot,
                        message_id=cmd.message_id,
                        chat_id=cmd.chat.id,
                        text=text,
                        reply_markup=InlineKeyboardMarkup(
                        [
                            [InlineKeyboardButton(Config.BUTTON_FOR_LINK_STR, url=f"https://t.me/{Config.BOT_USERNAME}?start={Config.URL_PREFIX}_{str(forward.message_id)}")]
                        ]))
                else:
                    sentmessage = await sendMessage(
                        bot=bot,
                        message_id=cmd.message_id,
                        chat_id=cmd.chat.id,
                        text=text,
                        reply_markup=InlineKeyboardMarkup(
                        [
                            [InlineKeyboardButton(Config.BUTTON_FOR_LINK_STR, url=f"https://t.me/{Config.BOT_USERNAME}?start={Config.URL_PREFIX}_{str(forward.message_id)}")]
                        ]))
            else:
                if Config.USE_BOT_INSTEAD_USER:
                    sentmessage = await sendMessage(
                        bot=Bot,
                        message_id=cmd.message_id,
                        chat_id=cmd.chat.id,
                        text=text)
                else:
                    sentmessage = await sendMessage(
                        bot=bot,
                        message_id=cmd.message_id,
                        chat_id=cmd.chat.id,
                        text=text)
        #
        if Config.DELETE_SENT_MESSAGE:
                await asyncio.sleep(int(Config.DELETE_SENT_MESSAGE_TIME))
                await sentmessage.delete(True)
        #
        


@Bot.on_message(filters.private & filters.command("start") & ~filters.edited)
async def start_handler(bot: Client, event: Message):
    try:
        __data = event.text.split("_")[1]
    except:
        __data = "/start"
    if __data == "/start":
        await sendMessage(bot, Config.START_MESSAGE, event.message_id, event.chat.id)
    else:
        file_id = int(__data)
        print("data was: " + __data)
        try:
            if Config.SEND_AS_COPY:
                sentfile = await bot.copy_message(chat_id=event.chat.id, from_chat_id=int(Config.DB_CHANNEL_ID), message_id=file_id)
            else:
                sentfile = await bot.forward_messages(chat_id=event.chat.id, from_chat_id=int(Config.DB_CHANNEL_ID), message_ids=file_id)
            tex = ""
            # filename exc.
            try:
                comingfilename = sentfile.document.file_name
            except:
                comingfilename = None
            #
            # caption exc.
            try:
                capton = sentfile.caption
            except:
                capton = None
            #       
            if Config.SEND_LINK_AGAIN:
                tex += "Bu linkle istediğiniz zaman tekrar dosyanıza ulaşabilirsiniz:\n\n" + \
                    f"🎁 `{capton}`\n" \
                    f"🎲 https://t.me/{Config.BOT_USERNAME}?start={Config.URL_PREFIX}_{str(file_id)}"
            if Config.DELETE_SENT_FILE:
                tex += f"\n\nBu dosya {str(Config.DELETE_SENT_FILE_TIME)} saniye sonra silinecek. Dosyanı yedeklersen iyi olur."
            await sentfile.reply_text(tex, reply_to_message_id = sentfile.message_id, disable_web_page_preview=True) 
            # delete send file +
            if Config.DELETE_SENT_FILE:
                await asyncio.sleep(int(Config.DELETE_SENT_FILE_TIME))
                await sentfile.delete(True)
            # delete send file -
        except:
            await sendMessage(bot, f"Unable to Get Message!\n\nBildir: {Config.CONTACT_ADRESS}", event.message_id, event.chat.id)

@Bot.on_message(filters.group & filters.text & ~filters.edited)
async def Fsub_handler(bot: Client, event: Message):
    if not await AuthCheck(event.chat.id, event.from_user.id):
        print("not authorized chat. read readme!")
        return
    if (Config.FORCE_SUB_CHANNEL is not None) and (event.from_user.is_bot is False):
        await AddUserToDatabase(event)
        Fsub = await ForceSub(Bot, event)
        if Fsub == 400:
            await db.set_joined_channel(event.from_user.id, joined_channel=False)
            await db.set_group_id(event.from_user.id, group_id=event.chat.id)
            try:
                await bot.restrict_chat_member(
                    chat_id=event.chat.id,
                    user_id=event.from_user.id,
                    permissions=ChatPermissions(can_send_messages=False)
                )
            except:
                pass
        elif Fsub == 404:
            try:
                await bot.kick_chat_member(chat_id=event.chat.id, user_id=event.from_user.id)
            except:
                pass
        else:
            await db.delete_user(event.from_user.id)

if not Config.ONLY_BOT_MODE:
    @User.on_chat_member_updated()
    async def handle_Fsub_Join(bot: Client, event: Message):
        """
        Auto Unmute Member after joining channel.

        :param bot: pyrogram.Client
        :param event: pyrogram.types.Message
        """

        if Config.FORCE_SUB_CHANNEL:
            try:
                user_ = await bot.get_chat_member(event.chat.id, event.from_user.id)
                if user_.is_member is False:
                    return
            except UserNotParticipant:
                return
            group_id = await db.get_group_id(event.from_user.id)
            group_message_id = await db.get_group_message_id(event.from_user.id)
            if group_id:
                try:
                    await bot.unban_chat_member(chat_id=int(group_id), user_id=event.from_user.id)
                    try:
                        await bot.delete_messages(chat_id=int(group_id), message_ids=group_message_id, revoke=True)
                    except Exception as err:
                        print(f"Unable to Delete Message!\nError: {err}")
                    await db.delete_user(user_id=event.from_user.id)
                except Exception as e:
                    print(f"Skipping FSub ...\nError: {e}")


pyrogram.idle()
# Stop User Client
if not Config.ONLY_BOT_MODE:
    User.stop()
    print("\n")
    print("Userbot Stopped!")
# Stop Bot Client
Bot.stop()
print("Bot Stopped!")
