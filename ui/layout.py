from ui.base import Checkbox


def ChatBox(items, prefix=""):
    layout = [[Checkbox(item, f"{prefix}:{item}")] for item in items]
    return layout


def FileBox(items, prefix=""):
    layout = [[Checkbox(item, f"{prefix}:{item}")] for item in items]
    return layout


def StartPage():
    pass
