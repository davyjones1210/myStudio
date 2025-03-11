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
    Assemble a scene in Maya for layout dept. with the specified assets as references.
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

def replace_filename(filepath, new_filename, typed):
    """
    Replace the last part of the file path with a new file name.
    """
    directory = os.path.dirname(filepath)
    if typed == "alembicFile":
        new_filename = "{}.abc".format(new_filename)
    elif typed == "metadata":
        new_filename = "{}.json".format(new_filename)
    else:
        Exception("Error: Unsupported typed file in typed")

    new_filepath = os.path.join(directory, new_filename)
    return new_filepath

def get_asset_in_shot_version_path(name, asset, department, typed):
    """
    Get the file path for the specified asset in shot version.
    """
    searched_version = search(PUBLISH_DCC, "shot", name, department, typed)
        
    logging.info("1. Successfully found specified version of shot: %s", name)

    # This searched version, locate the required typed file path and replace with asset name
    if searched_version:
        version_path = utils.getFilepath(searched_version)
        #Replace the shot name with asset name
        new_filepath = replace_filename(version_path, asset, typed)
        logging.info("2. Successfully located specified version path for asset: %s", new_filepath)
        return new_filepath
    
    return None


def assembleLighting(start_frame, end_frame, category, name, department, typed, *assets):
    """
    Assemble a scene in Maya for lighting dept with the specified assets as references.
    """
    if PUBLISH_DCC != "maya":
        raise Exception("Error: PUBLISH_DCC is not set to 'maya'")

    logging.info("0. Begins assembling scene")

    for asset in assets:
        # Step 1: Create reference by import the Alembic file of the asset through the reference editor
        alembic_path = get_asset_in_shot_version_path(name, asset, "animation", "alembicFile")
        print("alembic_path: ", alembic_path)
        if alembic_path:
            import_alembic_cache(alembic_path)
        else:
            logging.info("1. Could not find Alembic cache for asset: %s", asset)
            continue

        # Step 2: Import lookdev shader file export of the asset
        shaderfile_path = get_asset_version_path(asset, "lookdev", "shaderfile")
        print("shaderfile_path: ", shaderfile_path)
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
        print("shader_metadata: ", shader_metadata)
        print("shader_metadata type: ", type(shader_metadata))
        
        # connect_shader_to_geometry(asset, shader_metadata)

    logging.info("4. End for loop for assembling the scene with all assets")
    
    # Set frame ranges
    # set_frame_ranges(start_frame, end_frame)
    return None
    layout_scene_path = save_layout_scene(name)
    logging.info("5. Successfully saved the layout scene to %s", layout_scene_path)

    return layout_scene_path

def import_alembic_cache(alembic_path):
    """
    Reference the Alembic cache into the Maya scene using the Reference Editor.
    """
    # Determine the namespace from the Alembic file name
    namespace = os.path.splitext(os.path.basename(alembic_path))[0]
    print("namespace: ", namespace)

    # Reference the Alembic file
    nodes_referenced = cmds.file(alembic_path, reference=True, type="Alembic", namespace=namespace, returnNewNodes=True)

    # file -r -type "Alembic"  -ignoreVersion -gl -mergeNamespacesOnClash false -namespace "dobby" "C:/works/projects/NewTestProj2/shot/shot-101/animation/alembicFile/v17/dobby.abc";

    print("nodes_referenced: ", nodes_referenced)
    char_group = cmds.group(empty=True, name=f"{namespace}_cache")
    cmds.parent(nodes_referenced, char_group)
    logging.info("Successfully referenced Alembic cache from %s", alembic_path)

def read_shader_metadata(metadata_path):
    """
    Read the shader metadata from the JSON file.
    """
    
    shader_metadata = utils.readJsonFile(metadata_path)
    logging.info("Successfully read shader metadata from %s", metadata_path)
    return shader_metadata

def validate_shader_metadata(shader_metadata):
    """
    Validate the shader metadata to ensure it is in the expected format.
    """
    if not isinstance(shader_metadata, list):
        raise ValueError("Shader metadata should be a list of dictionaries")
    
    for item in shader_metadata:
        if not isinstance(item, dict):
            raise ValueError("Each item in shader metadata should be a dictionary")
        if 'shader' not in item or 'mesh' not in item:
            raise ValueError("Each item in shader metadata should contain 'shader' and 'mesh' keys")
    
    return True


def connect_shader_to_geometry(asset, shader_metadata):
    """
    Connect the shader to the geometry using the metadata.
    """

    # Validate shader metadata
    validate_shader_metadata(shader_metadata)

    # Connect shaders to geometry
    for item in shader_metadata:
        shader_name = item['shader']
        shading_engine = item.get('shadingEngine')
        meshes = item['mesh']
        
        if meshes:
            if not isinstance(meshes, list):
                meshes = [meshes]
            
            for mesh in meshes:
                geo_full_name = "{}:{}".format(asset, mesh)
                shader_full_name = "{}:{}".format(asset, shader_name)
                shading_engine_full_name = "{}:{}".format(asset, shading_engine) if shading_engine else None
                print("geo_full_name, shader_full_name, shading_engine_full_name: ", geo_full_name, shader_full_name, shading_engine_full_name)
                
                # Check if the shader exists in the scene
                if cmds.objExists(shader_full_name):
                    cmds.select(geo_full_name, replace=True)
                    cmds.hyperShade(assign=shader_full_name)
                    logging.info("Successfully assigned shader %s to geometry %s", shader_full_name, geo_full_name)
                else:
                    # Attempt to find the shader without the asset namespace
                    if cmds.objExists(shader_name):
                        cmds.select(geo_full_name, replace=True)
                        cmds.hyperShade(assign=shader_name)
                        logging.info("Successfully assigned shader %s to geometry %s", shader_name, geo_full_name)
                    else:
                        logging.warning("Shader %s does not exist in the scene", shader_full_name)
                
                # Connect shading engine if it exists
                if shading_engine_full_name and cmds.objExists(shading_engine_full_name):
                    cmds.sets(geo_full_name, edit=True, forceElement=shading_engine_full_name)
                    logging.info("Successfully connected shading engine %s to geometry %s", shading_engine_full_name, geo_full_name)
                elif shading_engine and cmds.objExists(shading_engine):
                    cmds.sets(geo_full_name, edit=True, forceElement=shading_engine)
                    logging.info("Successfully connected shading engine %s to geometry %s", shading_engine, geo_full_name)
                else:
                    logging.warning("Shading engine %s does not exist in the scene", shading_engine_full_name or shading_engine)



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
        if typed == "metadata":
            version_path = replace_filename(version_path, asset, typed)
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

    
    from assemble import main
    import importlib
    importlib.reload(main)
    main.PUBLISH_DCC = "maya"
    result = main.assembleLighting(1001, 1020, "shot", "shot-101", "lighting", "sourcefile", "main_cam", "alien", "pyramid", "dobby")
    """

    # 1. Search for all versions in the specified context.
    # 2. Retrieve file path of searched version
    # 3. Open/load file on dcc from that file path
    # Figure out steps as exercise.
    # Final outcome: Have that input file to be imported and opened in blender where artists can start the work on the file.
