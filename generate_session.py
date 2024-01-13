import asyncio
import os
import uuid
from turtle import clear

from telethon import TelegramClient

from creds import api_hash, api_id


async def main():
    cwd = os.getcwd()
    uid = str(uuid.uuid4())
    client = TelegramClient(uid, api_id, api_hash)
    phone_number = input("Phone number: ")
    await client.start(phone_number)
    path = f"{cwd}/{uid}.session"
    print(f"\n\nPath to you session file is:\n{path}\n\n")
    print("Please add this path to the session_path variable in creds.py!!")


asyncio.run(main())
