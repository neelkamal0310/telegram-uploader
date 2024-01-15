import asyncio
import inspect
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
    def wrapper(*args, **kwargs):
        def run_thread():
            if inspect.iscoroutinefunction(func):
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(func(*args, **kwargs))
            else:
                func(*args, **kwargs)

        thread = threading.Thread(target=run_thread, daemon=True)
        thread.start()

    return wrapper


async def run_async_concurrent(*tasks, max=1):
    """Runs a list of `tasks` concurrently using async. Works similar to
    gather. Gather tries to run all the tasks in one go, while this
    function uses a semaphore to control the number of tasks running at
    a given point of time.

    Parameters
    ----------
    tasks: list[async func]
        List of async tasks to be run.

    max: int
        Max number of async tasks to be run concurrently.

    Returns
    -------
    result
        The result of all tasks in same order of passing.
    """
    semaphore = asyncio.Semaphore(max)

    async def handle_with_semaphore(func):
        async with semaphore:
            await func

    tasks = [handle_with_semaphore(task) for task in tasks]
    result = await asyncio.gather(*tasks)
    return result
