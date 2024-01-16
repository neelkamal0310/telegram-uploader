import asyncio
import os
import sys

import PySimpleGUI as sg
from telethon import TelegramClient

from creds import api_hash, api_id, session_path
from ui import Button, Checkbox, Spacer, Window
from ui.base import CheckboxList, Column, Text, TextList
from utils import get_chats, get_filename, run_async_concurrent, threaded

client = TelegramClient(session_path, api_id, api_hash)


async def main():
    await client.start()
    chats = await get_chats(client)
    files = sys.argv[1:]
    files = [path for path in files if os.path.isfile(path)]

    layout = [
        [CheckboxList(chats, "chat"), TextList(files, "file")],
        [Spacer(), Checkbox("Send as document", "send_as_document"), Spacer()],
        [Spacer(), Button("Start Upload", "upload"), Button("Cancel", "cancel"), Spacer()],
    ]

    window = Window("Telegram Uploader - Upload to channel", layout)
    upload_to_chats = None
    as_document = None

    while True:
        event, values = window.read()
        if event == "upload":
            upload_to_chats = [chat for chat in chats if values[f"chat:{chat}"]]
            as_document = values["send_as_document"]
            window.close()
            await client.disconnect()
            await show_upload_window(upload_to_chats, files, as_document)
            break
        if event == sg.WIN_CLOSED or event == "cancel":
            break


async def create_upload_task(client, window, chat, file, force_document):
    def report_status(sent, total):
        key = f"{file}:{chat}:progress"
        percentage = (sent / total) * 100
        window.write_event_value(key, percentage)

    await client.send_file(
        chat,
        file,
        caption=get_filename(file, trim_ext=True),
        force_document=force_document,
        progress_callback=report_status,
        silent=True,
    )


@threaded
async def start_upload(window, files_to_upload, force_document=False):
    # client needs to be redeclared here since code in this block is threaded
    # and running in different loop
    client = TelegramClient(session_path, api_id, api_hash)
    await client.start()

    tasks = [
        create_upload_task(client, window, chat, file, force_document)
        for chat, file in files_to_upload
    ]

    await run_async_concurrent(*tasks, max=16)
    await client.disconnect()
    window.write_event_value("exit_app", "1")


async def show_upload_window(chats, files, force_document=False):
    client = TelegramClient(session_path, api_id, api_hash)
    await client.start()
    layout = [
        [Text("Filename"), Text("Channel/Chat")],
    ]

    files_to_upload = []
    for chat in chats:
        for file in files:
            key = f"{file}:{chat}:progress"
            layout.extend(
                [
                    [Text(get_filename(file)), Text("->"), Text(chat)],
                    [
                        sg.ProgressBar(100, key=key, size=(50, 5), expand_x=True),
                        Text("----", f"{key}:text"),
                    ],
                ]
            )
            files_to_upload.append((chat, file))
    layout = [
        [Column(layout)],
    ]
    window = Window("Uploading...", layout)
    window.read(False)
    window.move_to_center()
    await client.disconnect()

    start_upload(window, files_to_upload, force_document)

    while True:
        event, values = window.read()
        if event and event.endswith("progress"):
            window[event].update(values[event])
            window[f"{event}:text"].update(f"{int(values[event])}%")
        if event == "exit_app" or event == sg.WIN_CLOSED or event == "Cancel" or event is None:
            break


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
