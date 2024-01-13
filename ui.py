import PySimpleGUI as sg

from config import font

sg.theme("DarkAmber")

window_size = (1280, 720)
column_default_size = (0, 0)


def Spacer():
    return sg.Push()


def Button(text, key):
    return sg.Button(
        text,
        key=key,
        font=font,
    )


def Checkbox(text, key):
    return sg.Checkbox(
        text,
        key,
        expand_x=True,
        expand_y=True,
        enable_events=True,
        font=font,
    )


def Column(layout):
    return sg.Column(
        layout,
        scrollable=True,
        vertical_scroll_only=True,
        expand_x=True,
        expand_y=True,
        size=column_default_size,
    )


def Text(text):
    return sg.Text(text, font=font)


def Window(title, layout):
    return sg.Window(
        title,
        layout=layout,
        resizable=True,
        size=window_size,
    )
