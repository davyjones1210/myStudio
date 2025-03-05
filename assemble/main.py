import logging
import importlib
import tempfile
import os
from assemble import utils
importlib.reload(utils)


logging.basicConfig(level=logging.INFO)

PUBLISH_DCC = None


def search(PUBLISH_DCC, category, name, department, typed, version=None, approved=True):
    """
    Use this fucntion to search for versions in the specific context passed as argument. Just search for it
    """
    # 1. find versions database
    # 2. Search for latest version of typed file and arguments passed
    # 3. Return info
    
    return utils.getVersion(PUBLISH_DCC, category, name, department, typed, version, approved)


def sourceFile(category, name, department, typed, comments="Test Publish", version=None, approved=True):
    """
        latest approved or latest or specific version can be able to load in downstrem deparatment  to begin their work

        result = main.sourceFile("asset", "monkey", "modeling")
        or
        result = main.sourceFile("asset", "monkey", "modeling", version=v5)
        or 
        result = main.sourceFile("asset", "monkey", "modeling", version="latest", approved=True)
        or
        result = main.sourceFile("asset", "monkey", "modeling", version="latest", approved=False)   

        Find the proper version and generate the path.  

    """

    if not PUBLISH_DCC:
        raise Exception("Error: PUBLISH_DCC is not set")

    logging.info("0. Begins source file search")

    if PUBLISH_DCC == "blender":
        load_blender_file(category, name, department, typed, version, approved)
    elif PUBLISH_DCC == "maya":
        load_maya_file(category, name, department, typed, version, approved)
    else:
        raise Exception("Error: Unsupported DCC software")

def load_blender_file(category, name, department, typed, version, approved):
    """
    Load the specified version of a Blender file.
    """
    import bpy
    searched_version = search(PUBLISH_DCC, category, name, department, typed, version, approved)
    logging.info("1. Successfully found specified version")

    if searched_version:
        version_path = utils.getFilepath(searched_version)
        logging.info("2. Successfully located specified version path: %s", version_path)

        bpy.ops.wm.open_mainfile(filepath=version_path)
        logging.info("3. Successfully opened %s version in Blender", searched_version["version"])

def load_maya_file(category, name, department, typed, version, approved):
    """
    Load the specified version of a Maya file.
    """
    import maya.cmds as cmds
    searched_version = search(PUBLISH_DCC, category, name, department, typed, version, approved)
    logging.info("1. Successfully found specified version")

    if searched_version:
        version_path = utils.getFilepath(searched_version)
        logging.info("2. Successfully located specified version path: %s", version_path)

        cmds.file(version_path, open=True, force=True)
        logging.info("3. Successfully opened %s version in Maya", searched_version["version"])


def assembleScene(start_frame, end_frame, category, name, department, typed, *assets):
    """
    Assemble a scene in Maya with the specified assets as references.
    """
    if PUBLISH_DCC != "maya":
        raise Exception("Error: PUBLISH_DCC is not set to 'maya'")

    import maya.cmds as cmds

    logging.info("0. Begins assembling scene")

    for asset in assets:
        version_path = get_asset_version_path(asset, department, typed)
        if version_path:
            reference_asset_in_scene(asset, version_path)
        else:
            logging.info("1. Could not find specified version for asset: %s", asset)

    logging.info("4. End for loop for assembling the scene with all assets")

    # Set frame ranges
    set_frame_ranges(start_frame, end_frame)

    layout_scene_path = save_layout_scene(name)
    logging.info("5. Successfully saved the layout scene to %s", layout_scene_path)

    return layout_scene_path

def set_frame_ranges(start_frame, end_frame):
    """
    Set the start and end frames in the Maya scene.
    """
    import maya.cmds as cmds
    cmds.playbackOptions(min=start_frame, max=end_frame)
    cmds.currentTime(start_frame)
    logging.info("Set frame range: start_frame=%d, end_frame=%d", start_frame, end_frame)

def get_asset_version_path(asset, department, typed):
    """
    Get the file path for the specified asset version.
    """
    searched_version = search(PUBLISH_DCC, "asset", asset, department, typed)
    logging.info("1. Successfully found specified version for asset: %s", asset)

    if searched_version:
        version_path = utils.getFilepath(searched_version)
        logging.info("2. Successfully located specified version path for asset: %s", version_path)
        return version_path
    return None

def reference_asset_in_scene(asset, version_path):
    """
    Reference the asset in the Maya scene.
    """
    import maya.cmds as cmds

    file_type = "mayaAscii" if version_path.endswith(".ma") else "mayaBinary"
    reference_node = cmds.file(version_path, reference=True, type=file_type, ignoreVersion=True, gl=True, mergeNamespacesOnClash=False, namespace=asset, options="v=0;")
    logging.info("3. Successfully referenced %s in the scene", asset)

    cmds.file(reference_node, loadReference=True)
    logging.info("4. Successfully reloaded reference for %s", asset)

def save_layout_scene(name):
    """
    Save the layout scene in a temporary location.
    """
    import maya.cmds as cmds

    temp_dir = tempfile.gettempdir()
    layout_scene_path = os.path.join(temp_dir, "{}.mb".format(name))
    cmds.file(rename=layout_scene_path)
    cmds.file(save=True, type="mayaBinary")
    return layout_scene_path


"""
    import importlib
    from assemble import main
    importlib.reload(main)
    main.PUBLISH_DCC = "blender"
    result = main.sourceFile("asset", "monkey", "modeling", "sourcefile")
    print(result)

    from assemble import main
    import importlib
    importlib.reload(main)
    main.PUBLISH_DCC = "maya"
    result = main.sourceFile("asset", "dobby", "rigging", "sourcefile")

    from assemble import main
    import importlib
    importlib.reload(main)
    main.PUBLISH_DCC = "maya"
    result = main.assembleScene("shot", "shot-101", "rigging", "sourcefile", "asset1", "asset2", "asset3", "asset4")
    """

    # 1. Search for all versions in the specified context.
    # 2. Retrieve file path of searched version
    # 3. Open/load file on dcc from that file path
    # Figure out steps as exercise.
    # Final outcome: Have that input file to be imported and opened in blender where artists can start the work on the file.
