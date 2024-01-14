import asyncio
import os
import threading

import PySimpleGUI as sg

from config import font
from ui import Checkbox, Column, Text


def get_filename(path, trim_ext=False):
    basename = os.path.basename(path)
    filename = os.path.splitext(basename)
    return filename[0] if trim_ext else basename


async def get_chats(client):
    """
    Return list of chats available to the client.
    """

    chats = []
    async for dialog in client.iter_dialogs():
        if dialog.name:
            chats.append(dialog.name)
    chats.sort()
    return chats


def create_thread(func, *args, **kwargs):
    return threading.Thread(target=func, args=args, kwargs=kwargs, daemon=True)


def threaded(func):
    # A decorator that runs the function as threaded. It also creates a eventloop for asyncio operations
    def wrapper(func, *args, **kwargs):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        def run_thread():
            # result = func(*args, **kwargs)
            loop.run_until_complete(func(*args, **kwargs))

        thread = threading.Thread(target=run_thread, daemon=True)
        thread.start()

    return wrapper
