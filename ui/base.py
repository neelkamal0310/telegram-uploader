import PySimpleGUI as sg

from config import font

sg.theme("DarkAmber")

window_size = (1366, 768)
column_default_size = (0, 0)


def Spacer():
    return sg.Push()


def Button(text, key):
    return sg.Button(
        text,
        key=key,
        font=font,
    )


def Checkbox(text, key, **kwargs):
    return sg.Checkbox(
        text,
        key=key,
        enable_events=True,
        font=font,
    )


def Column(layout):
    return sg.Column(
        layout,
        scrollable=True,
        vertical_scroll_only=False,
        expand_x=True,
        expand_y=True,
        size=column_default_size,
    )


def Text(text, key=None):
    return sg.Text(text, key=key, font=font)


def Window(title, layout):
    return sg.Window(
        title,
        layout=layout,
        resizable=True,
        size=window_size,
    )


def CheckboxList(items, prefix):
    layout = [[Checkbox(item, f"{prefix}:{item}")] for item in items]
    return Column(layout)


def TextList(items, prefix):
    layout = [[Text(item, f"{prefix}:{item}")] for item in items]
    return Column(layout)


def VTop(items):
    return sg.vtop(items)


def VBottom(items):
    return sg.vbottom(items)


def VCenter(items):
    return sg.vcenter(items)
