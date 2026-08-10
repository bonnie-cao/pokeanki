import importlib

from aqt import gui_hooks
from aqt.utils import showWarning


opened = False


def startup():
    global opened
    if opened:
        warning_text = "\n".join((
            "Please use Pokeanki for one session at a time",
        ))
        showWarning(warning_text, title="Pokeanki - Multiple sessions detected")
        return


    opened = True
    from . import hooks


gui_hooks.profile_did_open.append(startup)
