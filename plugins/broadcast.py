import logging
from info import ADMINS
from pyrogram import Client, filters
from utils import collection_user

logger = logging.getLogger(__name__)

@Client.on_message(filters.command('broadcast') & filters.user(ADMINS))
async def broadcastHandler(bot, message):
    try:
        #Extracting Broadcasting Message
        message = message.text.split('/broadcast ')[1]
    except IndexError:
        await message.reply_text("Broadcasting can't be empty", parse_mode = 'html')
    except Exception as e:
        await bot.send_message(int(ADMINS), f"Broadcasting Failed {e}")
    else:
        #Getting User`s Id from Database
        countFailed = 0
        countSuccess = 0
        for userid in [document['userid'] for document in collection_user.find()]:
            try:
                #Sending Message One By One
                await bot.send_message(userid, message)
            except Exception as e:
                countFailed += 1
            else:
                countSuccess += 1
        else:
            await bot.send_message(int(ADMINS), f"Broadcasting Done\n\n{countSuccess} message broadcasted successfully.\n\n{countFailed} message failed to broadcast.")
    return
