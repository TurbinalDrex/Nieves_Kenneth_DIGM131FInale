import maya.cmds as cmds

# Suggestion: Your module docstrings should be at the very top of the file before your import

"""
Static configuration settings for Safe Cleanup Tool (Found/Refrences in Maya and Qt For Python Docs)
"""

# Suggestion: Typo in docstring, "Refrences" should be "References"

DEBUG = True

SAFE_CLEANUP_DEFAULTS = {
    "freeze_transforms": True,
    "delete_history": True,
    "preserve_deformers": True
}
"""
Builder Functions
"""

# Suggestion: ^You can just frame these like inline comments as opposed to treating it
# like a docstring.

def freeze_transforms(data,
                      translate=True,
                      rotate=True,
                      scale=True):

    """
    Freezes the Transforms on an object
    """

    #Suggestion: Fix docstring, explain your paramaters

    try:

        obj_name = data.get("object")
        if not cmds.objExists(obj_name):

            cmds.warning(
                f"Object Does not Exist: {obj_name}"
            )

            return

        cmds.makeIdentity(
             obj_name,
             apply=True,
             translate=translate,
             rotate=rotate,
             scale=scale,
             normal=False
            
        )

        if DEBUG:

            print(
                f"[DEBUG] Transforms frozen on {obj_name}"
            )
    except Exception as error:

           cmds.warning(
               f"Freeze transforms failed: {error}"
           )

def delete_non_deformer_history(data,
                                preserve_deformers=True):

    """
    Delete Non-deformer History Safely.
    """
# Suggestion: Fix Docstring

    try:

        obj_name = data.get("object")

        if not obj_name:
            cmds.warning(f"No object key in data")
            return

        if not cmds.objExists(obj_name):

            cmds.warning(
                f"Object does not exist: {obj_name}"
            )

            return

        cmds.bakePartialHistory(
            obj_name,
            prePostDeformers=not preserve_deformers
        )

        if DEBUG:

            print(
                f"[DEBUG] Safe history deleted on {obj_name}"
            )

    except Exception as error:

        cmds.warning(
            f"Safe delete failed: {error}"
        )

def delete_all_history(data):
    """
    Delete All Contruction History
    """
    # Suggestion: Typo, "Contruction" should be "Construction"
    # Suggestion: Missing a blank line between this function and the one above, PEP 8 formatting error
    try:

        obj_name = data.get("object")

        if not cmds.objExists(obj_name):

            cmds.warning(
                f"Object does not exist: {obj_name}"
            )

            return

        cmds.delete(
            obj_name,
            constructionHistory=True
        )

        if DEBUG:

            print(
                f"[DEBUG] Full history deleted on {obj_name}"
            )

    except Exception as error:

        cmds.warning(
            f"Delete history failed: {error}"
        )



def safe_cleanup(data,
                 freeze=True,
                 delete_history=True,
                 full_delete=False):
    """
    Perform combined safe cleanup.
    """

    try:

        if freeze:

            freeze_transforms(data)

        if full_delete:

            delete_all_history(data)

        elif delete_history:
            delete_non_deformer_history(data)

        if DEBUG:

            print(
                "[DEBUG] Safe cleanup completed"
            )

    except Exception as error:

        cmds.warning(
            f"Safe cleanup failed: {error}"
        )



"""
Builder Dispatcher Dictionary
"""

#Suggestion: Could just be another inline comment, not a docstring format

BUILDERS = {

    "freeze": freeze_transforms,

    "safe_delete": delete_non_deformer_history,

    "full_delete": delete_all_history,

    "safe_cleanup": safe_cleanup
}



"""
Dispatcher Function
"""

def create_element(data):
    """
    Dispatcher function for cleanup operations.
    """

    try:

        operation_type = data.get("type")

        builder = BUILDERS.get(operation_type)

        if builder:

            builder(data)

        else:

            cmds.warning(
                f"Unknown operation type: {operation_type}"
            )

    except Exception as error:

        cmds.warning(
            f"Dispatcher failed: {error}"
        )
