import os

import PySimpleGUI as sg

from config import font
from ui import Checkbox, Column, Text


def get_filename(path, trim_ext=False):
    basename = os.path.basename(path)
    filename = os.path.splitext(basename)
    return filename[0] if trim_ext else basename


def get_key(string, prefix="", suffix=""):
    result = string
    if suffix:
        result = f"{result}:{suffix}"
    if prefix:
        result = f"{prefix}:{result}"
    return result


def create_checkbox_frame(
    items,
    key_prefix,
    select_all=True,
):
    layout = []
    if select_all:
        layout.append(
            [
                Checkbox(
                    "Select all",
                    get_key("select_all", key_prefix),
                )
            ]
        )
    for item in items:
        element = [sg.Checkbox(item, key=get_key(item, key_prefix), font=font)]
        layout.append(element)
    return Column(layout)


def create_text_frame(
    items,
):
    layout = []
    for item in items:
        item_name = item.replace("/home/neel", "~")
        element = [Text(item_name)]
        layout.append(element)
    return Column(layout)
