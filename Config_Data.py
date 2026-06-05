"""
Core cleanup operations and
dispatcher functions for the
Safe Cleanup Tool.
"""
import maya.cmds as cmds
 
DEBUG = True

SAFE_CLEANUP_DEFAULTS = {
    "freeze_transforms": True,
    "delete_history": True,
    "preserve_deformers": True
}
"""
Builder Functions
"""
def freeze_transforms(data,
                      translate=True,
                      rotate=True,
                      scale=True):

    """
   Freezes transforms on a Maya object.
   
   Args:
       data (dict):
           Contains object information.
   
       translate (bool):
           Freeze translation values.
   
       rotate (bool):
           Freeze rotation values.
   
       scale (bool):
           Freeze scale values.
   
   Returns:
        None
    """

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

    try:

        obj_name = data.get("object")

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
                 delete_history=True):
    """
    Perform combined safe cleanup.
    """

    try:

        if freeze:

            freeze_transforms(data)

        if delete_history:

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


BUILDERS = {

    "freeze": freeze_transforms,

    "safe_delete": delete_non_deformer_history,

    "full_delete": delete_all_history,

    "safe_cleanup": safe_cleanup
}



"""
Dispatches cleanup operations using the
builder dictionary.

Args:
    data (dict):
        Cleanup operation information.

Returns:
    None
"""

def create_element(data):
    """
    Dispatcher function for cleanup operations.
    """

    try:
        if "object" not in data:

            cmds.warning(
                "Operation data missing 'object' key."
            )
        
            return

        if "type" not in data:
       
            cmds.warning(
                "Operation data missing 'type' key."
            )
        
            return
        
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
