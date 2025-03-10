import logging
import importlib
import tempfile
import os
import maya.cmds as cmds
from assemble import utils
importlib.reload(utils)


logging.basicConfig(level=logging.INFO)

PUBLISH_DCC = None

def search(PUBLISH_DCC, category, name, department, typed, version=None, approved=True):
    """
    Use this function to search for versions in the specific context passed as argument. Just search for it
    """
    return utils.getVersion(PUBLISH_DCC, category, name, department, typed, version, approved)

def sourceFile(category, name, department, typed, version=None, approved=True):
    """
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

def assembleLighting(start_frame, end_frame, category, name, department, typed, *assets):
    """
    Assemble a lighting scene in Maya with the specified assets as references.
    """
    if PUBLISH_DCC != "maya":
        raise Exception("Error: PUBLISH_DCC is not set to 'maya'")

    logging.info("0. Begins assembling scene")

    for asset in assets:
        # Step 1: Import Alembic file of the asset
        alembic_path = get_asset_version_path(asset, "animation", "alembicFile")
        if alembic_path:
            import_alembic_cache(alembic_path)
        else:
            logging.info("1. Could not find Alembic cache for asset: %s", asset)
            continue

        # Step 2: Import lookdev shader file export of the asset
        shaderfile_path = get_asset_version_path(asset, "lookdev", "shaderfile")
        if shaderfile_path:
            reference_asset_in_scene(asset, shaderfile_path)
        else:
            logging.info("2. Could not find lookdev shader file for asset: %s", asset)
            continue

        # Step 3: Read the metadata of the shader
        metadata_path = get_asset_version_path(asset, "lookdev", "metadata")
        if metadata_path:
            shader_metadata = read_shader_metadata(metadata_path)
        else:
            logging.info("3. Could not find shader metadata for asset: %s", asset)
            continue

        # Step 4: Connect the shader to the geometry
        connect_shader_to_geometry(asset, shader_metadata)

    logging.info("4. End for loop for assembling the scene with all assets")

    # Set frame ranges
    set_frame_ranges(start_frame, end_frame)

    layout_scene_path = save_layout_scene(name)
    logging.info("5. Successfully saved the layout scene to %s", layout_scene_path)

    return layout_scene_path

def import_alembic_cache(alembic_path):
    """
    Import the Alembic cache into the Maya scene.
    """
    cmds.AbcImport(alembic_path, mode="import")
    logging.info("Successfully imported Alembic cache from %s", alembic_path)

def read_shader_metadata(metadata_path):
    """
    Read the shader metadata from the JSON file.
    """
    with open(metadata_path, 'r') as file:
        shader_metadata = json.load(file)
    logging.info("Successfully read shader metadata from %s", metadata_path)
    return shader_metadata

def connect_shader_to_geometry(asset, shader_metadata):
    """
    Connect the shader to the geometry using the metadata.
    """
    for geo_name, shader_name in shader_metadata.items():
        geo_full_name = "{}:{}".format(asset, geo_name)
        shader_full_name = "{}:{}".format(asset, shader_name)
        cmds.select(geo_full_name, replace=True)
        cmds.hyperShade(assign=shader_full_name)
    logging.info("Successfully connected shaders to geometry for asset: %s", asset)

def set_frame_ranges(start_frame, end_frame):
    """
    Set the start and end frames in the Maya scene.
    """
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
    file_type = "mayaAscii" if version_path.endswith(".ma") else "mayaBinary"
    reference_node = cmds.file(version_path, reference=True, type=file_type, ignoreVersion=True, gl=True, mergeNamespacesOnClash=False, namespace=asset, options="v=0;")
    logging.info("3. Successfully referenced %s in the scene", asset)

    cmds.file(reference_node, loadReference=True)
    logging.info("4. Successfully reloaded reference for %s", asset)

def save_layout_scene(name):
    """
    Save the layout scene in a temporary location.
    """
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
    result = main.sourceFile("shot", "shot-101", "layout", "sourcefile")

    from assemble import main
    import importlib
    importlib.reload(main)
    main.PUBLISH_DCC = "maya"
    result = main.assembleScene(1001, 1020, "shot", "shot-101", "rigging", "sourcefile", "main_cam", "alien", "pyramid", "dobby")
    """

    # 1. Search for all versions in the specified context.
    # 2. Retrieve file path of searched version
    # 3. Open/load file on dcc from that file path
    # Figure out steps as exercise.
    # Final outcome: Have that input file to be imported and opened in blender where artists can start the work on the file.
