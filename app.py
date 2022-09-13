import asyncio
import os
import sys
import threading

import PySimpleGUI as sg
from telethon import TelegramClient

from config import font_size
from creds import api_hash, api_id, session_path
from utils import create_checkbox_frame, create_text_frame, get_filename

sg.theme("DarkAmber")

client = TelegramClient(
    session_path,
    api_id,
    api_hash,
)


async def get_chats():
    """
    Return list of chats available to the client.
    """

    chats = []
    async for dialog in client.iter_dialogs():
        chats.append(dialog.id)
    chats.sort()
    return chats


async def main():
    chats = await get_chats()
    files = sys.argv[1:]
    selected_files = []
    for file in files:
        if not os.path.exists(file):
            continue
        selected_files.append(file)
    files = selected_files

    layout = [
        [
                    create_checkbox_frame("Chats", chats, "chat", select_all=False),
                    create_text_frame("Files", files),
        ],
    ]

    layout.append(
        [
            sg.Push(),
            sg.Checkbox(
                "Send as document",
                key="send_as_document",
                font=font_size,
                size=(10, 10),
            ),
            sg.Push(),
        ])
    layout.append(
        [
            sg.Push(),
            sg.Button("Start Upload", key="upload", font=font_size),
            sg.Button("Cancel", key="cancel", font=font_size),
            sg.Push(),
        ]
    )

    window = sg.Window("Upload to channel...", layout=layout, resizable=True, size=(1280, 720))

    while True:
        event, values = window.read()
        if event and event.endswith("select_all"):
            category = event.split(":")[0]
            for key in values:
                if key.startswith(category):
                    window[key].update(values[event])
        if event == "upload":
            upload_to_chats = [chat for chat in chats if values[f"chat:{chat}"]]
            as_document = values["send_as_document"]
            window.close()
            break
        if (
            event == sg.WIN_CLOSED or event == "cancel"
        ):  # if user closes window or clicks cancel
            break

    await start_upload(upload_to_chats, files, as_document)


async def upload_handler(client, window, chat, file, force_document):
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


async def start_uploading(window, files_to_upload, force_document=False):
    client = TelegramClient(
        session_path,
        api_id,
        api_hash,
    )
    await client.start()
    tasks = []
    for chat, file in files_to_upload:
        task = upload_handler(client, window, chat, file, force_document)
        tasks.append(task)
    await asyncio.gather(*tasks)
    await client.disconnect()


def create_async_tasks(window, files_to_upload, force_document=False):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_uploading(window, files_to_upload, force_document))
    print("loop finished")
    window.write_event_value("exit_app", "1")

async def start_upload(chats, files, force_document=False):
    layout = [
        [
            sg.Text("Filename", font=font_size, size=50),
            sg.Text("Channel/Chat", font=font_size),
        ]
    ]

    files_to_upload = []
    for chat in chats:
        for file in files:
            key = f"{file}:{chat}:progress"
            layout.extend(
                [
                    [
                        sg.Text(get_filename(file), font=font_size),
                        sg.Text("->"),
                        sg.Text(chat, font=font_size),
                    ],
                    [
                        sg.ProgressBar(100, key=key, size=(50, 5), expand_x=True),
                        sg.Text(f"----", key=f"{key}:text", font=font_size),
                    ],
                    [
                        sg.T("                                    "),
                    ],
                ]
            )
            files_to_upload.append((chat, file))
    layout = [
        [
            sg.Column(
                layout,
                scrollable=True,
                vertical_scroll_only=True,
                expand_x=True,
                expand_y=True,
                size=(800, 600)
            )
        ]
    ]
    window = sg.Window("Uploading...", layout=layout, resizable=True, finalize=True)
    window.bind("<Configure>", "Event")
    await client.disconnect()

    upload_thread = threading.Thread(
        target=create_async_tasks,
        args=(
            window,
            files_to_upload,
            force_document,
        ),
        daemon=True,
    )
    upload_thread.start()

    while True:
        event, values = window.read()
        if event and event.endswith("progress"):
            window[event].update(values[event])
            window[f"{event}:text"].update(f"{int(values[event])}%")
        if event == "exit_app":
            upload_thread.join()
            break
        if event == sg.WIN_CLOSED or event == "Cancel" or event is None:
            upload_thread.join()
            break


with client:
    client.loop.run_until_complete(main())
