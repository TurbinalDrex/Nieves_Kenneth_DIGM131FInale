import maya.cmds as cmds
import os
import sys

"""
Entry point for Safe Cleanup Tool.
By Kenneth Nieves
"""

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))

if _THIS_DIR not in sys.path:
    sys.path.insert(0, _THIS_DIR)

import Config_Data as tool
import Data_Driven_Config as presets


def run_cleanup():
    selection = cmds.ls(selection=True)

    if not selection:
        print("No object selected.")
        return

    obj = selection[0]

    """ Use default preset (Expand later!)"""
    tool.safe_cleanup(obj)


if __name__ == "__main__":
    run_cleanup()