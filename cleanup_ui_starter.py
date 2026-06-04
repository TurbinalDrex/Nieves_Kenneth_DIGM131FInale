"""cleanup_ui_starter.py  --  UI starter for the Safe Cleanup Tool.
=============================================================================
DIGM 131 - Week 10

A LIGHTWEIGHT scaffold for the Week-10 UI on top of your existing dispatcher-
driven backbone (`Config_Data.safe_cleanup` / `freeze_transforms` /
`delete_non_deformer_history` / `delete_all_history` + `BUILDERS` +
`create_element`).

This is a *parallel reference* -- it does NOT replace your existing
`main.py` PySide6 window. Compare against it, or fold the same widget list
into your `CleanupWindow` class. Both routes are graded equally.

What's already done for you here:
    * `default_settings()`  -- the settings dict shape (which steps to run +
                               selection-vs-preset toggle + debug)
    * `do_the_work(settings)` -- wired straight to your `safe_cleanup()`
                                 and friends; respects the selection
                                 toggle and the preset CLEANUP_CONFIG.

What you fill in (or fold into your QWidget):
    * `build_ui()`     -- pick controls and lay them out (checkBox-heavy)
    * `read_settings()` -- query each control into the same dict shape

See UI_DESIGN.md for the suggested controls.
"""

import os
import sys

import maya.cmds as cmds

try:
    _THIS_DIR = os.path.dirname(os.path.abspath(__file__))
except NameError:
    _THIS_DIR = cmds.workspace(query=True, rootDirectory=True)
if _THIS_DIR not in sys.path:
    sys.path.insert(0, _THIS_DIR)

# Your existing modules -- DO NOT duplicate the logic, import it.
import Config_Data as tool                 # noqa: E402
import Data_Driven_Config as preset_cfg    # noqa: E402


# =====================================================================
# LAYER 3 -- LOGIC  (wired to your existing safe_cleanup; usually no edits)
# =====================================================================

def default_settings():
    """The dict shape this tool consumes. Each key maps to one UI control."""
    return {
        "freeze_transforms":  True,
        "delete_history":     True,
        "preserve_deformers": True,
        "use_selection":      True,   # False -> walk CLEANUP_CONFIG instead
        "debug":              True,
    }


def _targets_from_selection():
    """Build a list of data dicts from the current Maya selection."""
    selection = cmds.ls(selection=True) or []
    if not selection:
        raise ValueError("Nothing selected. Select one or more objects first.")
    return [{"object": obj} for obj in selection]


def _operate_on(data, settings):
    """Run the chosen safe-cleanup steps on a single object dict."""
    if settings.get("freeze_transforms", True):
        tool.freeze_transforms(data)
    if settings.get("delete_history", True):
        if settings.get("preserve_deformers", True):
            tool.delete_non_deformer_history(data, preserve_deformers=True)
        else:
            tool.delete_all_history(data)


def do_the_work(settings):
    """Honour the settings dict and dispatch through your existing builders.

    Two modes:
        * use_selection=True  -> operate on the current Maya selection
        * use_selection=False -> walk CLEANUP_CONFIG via your dispatcher
    """
    # Wire the UI's `debug` toggle through to your module flag so the
    # builder `[DEBUG] ...` prints actually appear when the artist asks.
    tool.DEBUG = bool(settings.get("debug", False))

    if settings.get("use_selection", True):
        targets = _targets_from_selection()
        for data in targets:
            _operate_on(data, settings)
        return targets

    # Preset path: walk Data_Driven_Config.CLEANUP_CONFIG through the
    # dispatcher you already wrote.
    for entry in preset_cfg.CLEANUP_CONFIG:
        tool.create_element(entry)
    return list(preset_cfg.CLEANUP_CONFIG)


# =====================================================================
# LAYER 1 -- UI  (TODO: YOU fill this in)
# =====================================================================
#
# This scaffold uses `maya.cmds` style so you can compare directly to
# David's / Lillian's starters. If you'd rather keep your PySide6 window,
# add the SAME widget list to `CleanupWindow.__init__` in main.py and
# store each on `self.<name>_checkbox` so `read_settings()` can query
# them.

_ui = {}


def build_ui():
    """Draw the Safe Cleanup window.

    TODO -- fill this in. For each setting in default_settings(), add a
    control and store its name in _ui[<setting_key>].
    """
    window = "safeCleanupWin"
    if cmds.window(window, exists=True):
        cmds.deleteUI(window)
    cmds.window(window, title="Safe Cleanup Tool", widthHeight=(380, 340))
    cmds.columnLayout(adjustableColumn=True, rowSpacing=6,
                      columnOffset=("both", 14))
    cmds.text(label="Pick the steps to run, then press Run.", align="left")
    cmds.separator(height=8, style="in")

    # TODO -- add controls for each key in default_settings(). For example:
    #   _ui["freeze_transforms"]  = cmds.checkBox(label="Freeze transforms", value=True)
    #   _ui["delete_history"]     = cmds.checkBox(label="Delete history", value=True)
    #   _ui["preserve_deformers"] = cmds.checkBox(label="Preserve deformers (safe)", value=True)
    #   _ui["use_selection"]      = cmds.checkBox(label="Use current selection", value=True)
    #   _ui["debug"]              = cmds.checkBox(label="Debug output", value=True)
    #   _ui["report"]             = cmds.scrollField(editable=False, wordWrap=True, height=120)

    cmds.button(label="Run cleanup", height=32, command=lambda *_: on_run())
    cmds.showWindow(window)


# =====================================================================
# LAYER 2 -- DATA + BRIDGE
# =====================================================================

def read_settings():
    """Query every control and return the dict shape from default_settings().

    TODO -- query _ui[<key>] for each setting. Examples:
        "freeze_transforms":  cmds.checkBox(_ui["freeze_transforms"],  query=True, value=True),
        "delete_history":     cmds.checkBox(_ui["delete_history"],     query=True, value=True),
        "preserve_deformers": cmds.checkBox(_ui["preserve_deformers"], query=True, value=True),
        "use_selection":      cmds.checkBox(_ui["use_selection"],      query=True, value=True),
        "debug":              cmds.checkBox(_ui["debug"],              query=True, value=True),
    """
    # Placeholder so partial code still runs while you're filling this in.
    return default_settings()


def on_run():
    """Bridge: gather settings, hand to logic, surface errors politely."""
    settings = read_settings()
    try:
        results = do_the_work(settings)
        summary = "[SafeCleanup] processed {} object(s).".format(len(results))
        print(summary)
        report = _ui.get("report")
        if report and cmds.scrollField(report, exists=True):
            cmds.scrollField(report, edit=True, text=summary + "\n")
    except ValueError as error:
        cmds.warning("Could not run cleanup: {}".format(error))


# =====================================================================
# RUN
# =====================================================================

if __name__ == "__main__":
    # do_the_work(default_settings())  # uncomment to test the LOGIC by itself
    build_ui()
