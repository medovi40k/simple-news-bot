import os

import aiosqlite
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv

load_dotenv("project.env")
# Initialize the bot with your API token

bot = Bot(os.environ.get('TELEGRAM_BOT_TOKEN'))

dp = Dispatcher(bot, storage=MemoryStorage())
# Define the group chat ID where messages will be forwarded
group_chat_id = int(os.environ.get('TELEGRAM_GROUP_ID'))  # Replace with your group chat ID
# Define the name of the SQLite DB file
file_of_db = ""  # Replace with your SQLite DB file


@dp.message_handler(commands=['sendmessage'])
async def sendmessage(message):
    if message.chat.id == group_chat_id:
        arguments = message.get_args()
        checkrow = []
        argssplit = arguments.split()
        try:
            async with aiosqlite.connect(file_of_db) as db:
                async with db.execute(f"SELECT TelegramID from ids WHERE PersonID={argssplit[0]}") as cursor:
                    async for row in cursor:
                        checkrow = row
            message_to_output = arguments.replace(f"{argssplit[0]} ", "")
            await bot.send_message(checkrow[0], f"You've got a message from admin: \n\n`{message_to_output}`",
                                   parse_mode="markdown")
        except:
            print("Error while connecting to the database #1")


@dp.message_handler(commands=['start'])
async def start_mess(message):
    if (message.chat.id != group_chat_id):
        await bot.send_message(message.chat.id,"Hi! Here you can suggest us news.")

# Ban command
@dp.message_handler(commands=['ban'])
async def ban_user(message):
    if message.chat.id == group_chat_id:
        arguments = message.get_args()
        checkrow = []
        async with aiosqlite.connect(file_of_db) as db:
            try:
                async with db.execute(f"SELECT TelegramID from ids WHERE PersonID={arguments}") as cursor:
                    async for row in cursor:
                        checkrow = row
                        await db.execute(f"INSERT INTO bans(TelegramID) VALUES ({checkrow[0]})")
                        await db.commit()
                        print(f"Banned {checkrow[0]}")
            except:
                print("Error while connecting to the database #4")


# Unban command
@dp.message_handler(commands=['unban'])
async def unban_user(message):
    if message.chat.id == group_chat_id:
        arguments = message.get_args()
        checkrow = []
        async with aiosqlite.connect(file_of_db) as db:
            try:
                async with db.execute(f"SELECT TelegramID from ids WHERE PersonID={arguments}") as cursor:
                    async for row in cursor:
                        checkrow = row
                        await db.execute(f"DELETE FROM bans WHERE TelegramID=({checkrow[0]})")
                        await db.commit()
                        print(f"Unbanned {checkrow[0]}")
            except:
                print("Error while connecting to the database #6")

# Handle private messages
@dp.message_handler(content_types=['text', 'photo', 'video', 'gif', 'sticker'])
async def handle_private_message(message):
    # Forward the message to the group chat
    is_allowed = True
    print(message.chat.id)
    print(message.text)
    try:
        async with aiosqlite.connect(file_of_db) as db:
            async with db.execute(f"SELECT * FROM bans WHERE TelegramID={message.chat.id}") as cursor:
                async for row in cursor:
                    if row!='':
                        is_allowed = False
    except:
        print("Error while connecting to the database #5")
    if (message.chat.id != group_chat_id and is_allowed):
        checkrow = []
        try:
            async with aiosqlite.connect(file_of_db) as db:
                async with db.execute(f"SELECT * FROM ids WHERE TelegramID={message.chat.id}") as cursor:
                    async for row in cursor:
                        checkrow = row
                        print(row)
        except:
            print("Error while connecting to the database #2")

        if checkrow == []:
            try:
                async with aiosqlite.connect(file_of_db) as db:
                    await db.execute(f"INSERT INTO ids(TelegramID) VALUES ({message.chat.id})")
                    await db.commit()
                    async with db.execute(f"SELECT * FROM ids WHERE TelegramID={message.chat.id}") as cursor:
                        async for row in cursor:
                            checkrow = row
                            print(row)
            except:
                print("Error while connecting to the database #2")

        await bot.send_message(message.chat.id, "Thanks for suggesting news!")
        await bot.send_message(group_chat_id, f"ID of sender: `{checkrow[0]}`", parse_mode="markdown")
        await bot.forward_message(group_chat_id, message.chat.id, message.message_id)
    else:
        await bot.send_message(message.chat.id, "You are banned")

async def initialize():
    async with aiosqlite.connect(file_of_db) as db:
        try:
            await db.execute(f"SELECT * FROM ids")
        except:
            await db.execute("""CREATE TABLE "ids" (PersonID INTEGER PRIMARY KEY AUTOINCREMENT, TelegramID int)""")
            await db.execute("""CREATE TABLE "bans" (JustID INTEGER PRIMARY KEY AUTOINCREMENT, TelegramID int)""")
            await db.commit()


# Start the bot
if __name__ == '__main__':
    executor.start(dp, initialize())
    executor.start_polling(dp, skip_updates=False)
