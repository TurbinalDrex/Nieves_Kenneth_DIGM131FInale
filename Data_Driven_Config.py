import maya.cmds as cmds

"""
Config presets for Safe Cleanup Tool
"""

CLEANUP_PRESETS = {
    "safe_mode": {
        "freeze_transforms": True,
        "delete_history": True,
        "preserve_deformers": True
    },
    "rig_safe": {
        "freeze_transforms": True,
        "delete_history": False,
        "preserve_deformers": True
    }
}