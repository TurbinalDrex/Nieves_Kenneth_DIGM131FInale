"""
Safe Cleanup Tool

Main entry point and user interface.
By Kenneth Nieves
"""

import maya.cmds as cmds

import os
import sys

from PySide6 import QtWidgets

"""
Module Set-Up
"""

_THIS_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

if _THIS_DIR not in sys.path:

    sys.path.insert(0, _THIS_DIR)

import Config_Data as tool
import Data_Driven_Config as config
"""
Driver Looper
"""
def run_cleanup_pipeline():
    """
    Runs all cleanup operations defined
    in the data-driven configuration file.
    
    Returns:
        None
    """
    for cleanup_operation in config.CLEANUP_CONFIG:

        tool.create_element(
            cleanup_operation
        )
"""
Qt Window
"""
class CleanupWindow(QtWidgets.QWidget):
    """
    Main UI window for the Safe Cleanup Tool.

    Allows users to perform safe cleanup
    operations on selected Maya objects.
    """
    def __init__(self):

        super(CleanupWindow, self).__init__()

        self.setWindowTitle(
            "Safe Cleanup Tool"
        )

        self.setMinimumWidth(300)

        layout = QtWidgets.QVBoxLayout()

        self.safe_checkbox = QtWidgets.QCheckBox(
            "Safe Cleanup Mode"
        )

        run_button = QtWidgets.QPushButton(
            "Run Cleanup"
        )

        run_button.clicked.connect(
            self.run_cleanup
        )

        layout.addWidget(
            self.safe_checkbox
        )

        layout.addWidget(
            run_button
        )

        self.setLayout(layout)

    def run_cleanup(self):
        """
        Executes safe cleanup on all currently
        selected Maya objects.
    
        Returns:
            None
        """
        selection = cmds.ls(selection=True)

        if not selection:

            cmds.warning(
                "Nothing selected."
            )

            return

        for obj in selection:

            data = {
                "type": "safe_cleanup",
                "object": obj
            }

            tool.create_element(data)
"""
Launch UI
"""
window = None

def launch_ui():
    """
    Creates and displays the cleanup tool UI.

    If an existing window is open,
    it is closed first.

    Returns:
        None
    """
    global window

    try:

        window.close()
        window.deleteLater()

    except Exception as error:

        print(
            f"UI cleanup failed: {error}"
        )

    window = CleanupWindow()

    window.show()
"""
Self Test
"""

if __name__ == "__main__":

    launch_ui()
