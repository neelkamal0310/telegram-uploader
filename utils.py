import PySimpleGUI as sg
from config import font_size
import os

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
    frame_name,
    items,
    key_prefix,
    select_all=True,
):
    layout = []
    if select_all:
        layout.append(
            [
                sg.Checkbox(
                    "Select all",
                    key=get_key("select_all", key_prefix),
                    enable_events=True,
                )
            ]
        )
    for item in items:
        element = [
            sg.Checkbox(
                item,
                key=get_key(item, key_prefix),
                font=font_size
            )
        ]
        layout.append(element)
    return sg.Column(layout, scrollable=True, vertical_scroll_only=True, expand_y=True, expand_x=True)


def create_text_frame(
    frame_name,
    items,
):
    layout = []
    for item in items:
        element = [sg.Text(item.replace("/home/neel", "~"), font=font_size)]
        layout.append(element)
    return sg.Column(layout, scrollable=True, vertical_scroll_only=True, expand_y=True, expand_x=True)

