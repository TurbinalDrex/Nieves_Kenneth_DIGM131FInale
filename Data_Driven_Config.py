"""
Data-driven cleanup configuration
for the Safe Cleanup Tool.
"""
import maya.cmds as cmds

CLEANUP_CONFIG = [

    {
        "type": "freeze",
        "object": "pCube1"
    },

    {
        "type": "safe_delete",
        "object": "pCube1"
    },

    {
        "type": "freeze",
        "object": "pSphere1"
    },

    {
        "type": "safe_delete",
        "object": "pSphere1"
    },

    {
        "type": "full_delete",
        "object": "pCylinder1"
    },

    {
        "type": "freeze",
        "object": "pCylinder1"
    },

    {
        "type": "safe_cleanup",
        "object": "pTorus1"
    },

    {
        "type": "freeze",
        "object": "pTorus1"
    }
]
