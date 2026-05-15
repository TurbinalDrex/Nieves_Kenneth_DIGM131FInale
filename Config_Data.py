import maya.cmds as cmds

"""
Static configuration settings for Safe Cleanup Tool (Found/Refrences in Maya Docs)
"""
 
SAFE_CLEANUP_DEFAULTS = {
    "freeze_transforms": True,
    "delete_history": True,
    "preserve_deformers": True
}

def freeze_transforms(obj_name):
    cmds.makeIdentity(obj_name, apply=True, translate=True,
                      rotate=True, scale=True, normal=False)

def delete_non_deformer_history(obj_name):
    cmds.bakePartialHistory(obj_name, prePostDeformers=False)

def delete_all_history(obj_name):
    cmds.delete(obj_name, constructionHistory=True)

def safe_cleanup(obj_name, config=None):
    cmds.makeIdentity(obj_name, apply=True)
    cmds.delete(obj_name, constructionHistory=True)