
import shutil
import os

import bpy

from publish import utils


def source():
    """
    get saved blender file path
    """
    source_filpath = bpy.data.filepath

    return source_filpath

# def usd():
    # export usd filer into temp 
    # return temp location


    
def register(category, name, department, typed):

    current_version = utils.getCurrentVersion(category, name, department)
    next_version = utils.nextVersion(current_version)

    # version context
    version_context = {
        "name": name, # monkey
        "category": category, #Asset or shot
        "department": department, # modelling, rigging, etc
        "version": next_version,
        "comment": "test publish",
        "type": typed,
    }

    utils.writeJson(version_context)

    return version_context


def deployed(source_filpath, target_filepath):

    if not os.path.exists(os.path.dirname(target_filepath)):
        os.makedirs(
            os.path.dirname(target_filepath)
        )
    # This is the exact clone of the user saved file
    shutil.copy(source_filpath, target_filepath)



