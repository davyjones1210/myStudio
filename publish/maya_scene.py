import os
import maya.cmds as cmds
from publish import utils
import json


def maya_source():
    """
    Execute the publish process
    """
    source_filpath = cmds.file(query=True, sceneName=True)
    print("source_filpath: ", source_filpath)

    if not source_filpath:
        raise Exception("Error: Maya scene has not been saved. Please save the scene before publishing.")

    return source_filpath

def maya_usd_export(frame_start, frame_end, selected=False, animation=False, uvmaps=False, materials=False, filepath=None):
    """
    Export the current Maya scene to USD format.
    """
    filepath = filepath or utils.getTempFilepath(".usda")

    # Ensure the USD plugin is loaded
    if not cmds.pluginInfo('mayaUsdPlugin', query=True, loaded=True):
        cmds.loadPlugin('mayaUsdPlugin')

    # Set export options
    export_options = {
        "exportUVs": uvmaps,
        "exportSkels": "none",
        "exportSkin": "none",
        "exportBlendShapes": False,
        "exportDisplayColor": False,
        "exportColorSets": True,
        "exportComponentTags": True,
        "defaultMeshScheme": "catmullClark",
        "eulerFilter": False,
        "staticSingleSample": not animation,
        "frameStride": 1,
        "defaultUSDFormat": "usdc",
        "rootPrim": "",
        "rootPrimType": "scope",
        "defaultPrim": "nurbsCube1",
        "exportMaterials": materials,
        "shadingMode": "useRegistry",
        "convertMaterialsTo": "[UsdPreviewSurface]",
        "exportAssignedMaterials": True,
        "exportRelativeTextures": "automatic",
        "exportInstances": True,
        "exportVisibility": True,
        "mergeTransformAndShape": True,
        "includeEmptyTransforms": True,
        "stripNamespaces": False,
        "worldspace": False,
        "exportStagesAsRefs": True,
        "excludeExportTypes": "[]",
        "legacyMaterialScope": False
    }

    # Handle selected objects
    if selected:
        selected_objects = cmds.ls(selection=True)
        if not selected_objects:
            raise RuntimeError("No objects selected for export.")
        # Include the selection flag in the export options
        export_options["selection"] = True
    else:
        export_options["selection"] = False

    # Handle animation export
    if animation:
        export_options["frameRange"] = (frame_start, frame_end)

    # Execute the export command
    try:
        cmds.mayaUSDExport(file=filepath, **export_options)
    except Exception as e:
        print("USD export failed: {}".format(e))
        return None

    print("USD export succeeded")
    return filepath

def maya_alembic_export(frame_start, frame_end, selected=False, animation=True, filepath=None):
    """
    Export the current Maya scene to Alembic format.
    """
    filepath = filepath or utils.getTempFilepath(".abc")

    # Ensure the AbcExport plugin is loaded
    if not cmds.pluginInfo('AbcExport', query=True, loaded=True):
        cmds.loadPlugin('AbcExport')

    # Set export options
    export_options = [
        "-uvWrite",
        "-worldSpace",
        "-writeVisibility",
        "-dataFormat", "ogawa"
    ]

    if animation:
        export_options.extend(["-frameRange", str(frame_start), str(frame_end)])

    if selected:
        selected_objects = cmds.ls(selection=True)
        if not selected_objects:
            raise RuntimeError("No objects selected for export.")
        for obj in selected_objects:
            export_options.append("-root")
            export_options.append(obj)

    # Construct the export command
    export_command = ' '.join(export_options) + ' -file "{}"'.format(filepath.replace("\\", "/"))

    print("Export command: {}".format(export_command))
    # Execute the export command
    try:
        cmds.AbcExport(j=export_command)
    except Exception as e:
        print("Alembic export failed: {}".format(e))
        return None

    return filepath


def maya_alembic_export_per_asset(frame_start, frame_end, selected=False, animation=True, directory=None):
    """
    Export the Alembic file of each asset in the Maya scene.
    """
    if directory is None:
        directory = utils.getTempDirectory()

    # Ensure the directory exists
    if not os.path.exists(directory):
        os.makedirs(directory)

    alembic_filepaths = []

    # Ensure the AbcExport plugin is loaded
    if not cmds.pluginInfo('AbcExport', query=True, loaded=True):
        cmds.loadPlugin('AbcExport')

    # Identify the names of the assets in the scene, excluding default cameras
    assets = [asset for asset in cmds.ls(assemblies=True) if asset not in ["persp", "top", "front", "side"]]

    for asset in assets:
        # Remove namespaces from the asset name and use the first part before the ':'
        asset_name = asset.split(":")[0]
        cache_set_name = "{}:cache_set".format(asset_name)

        # Check if the cache set exists
        if not cmds.objExists(cache_set_name):
            print("Cache set {} does not exist for asset: {}".format(cache_set_name, asset))
            continue

        # Get the members of the cache set
        cache_set_members = cmds.sets(cache_set_name, query=True) or []

        if not cache_set_members:
            print("No members found in cache set for asset: {}".format(asset))
            continue

        # Set the file path for the Alembic export
        alembic_filepath = "{}/{}.abc".format(directory, asset_name)
        alembic_filepath = alembic_filepath.replace("\\", "/")

        # Set export options
        export_options = [
            "-frameRange", str(frame_start), str(frame_end),
            "-uvWrite",
            "-worldSpace",
            "-writeVisibility",
            "-dataFormat", "ogawa",
            "-writeUVSets"
        ]

        # Add the cache set itself as a root
        export_options.append("-root")
        export_options.append(cache_set_name)

        # Add each member of the cache set as a root
        for member in cache_set_members:
            full_path_member = cmds.ls(member, long=True)[0]  # Get the full path of the member
            export_options.append("-root")
            export_options.append(full_path_member)

        # Construct the export command
        export_command = ' '.join(export_options) + ' -file "{}"'.format(alembic_filepath)

        print("Export command for {}: {}".format(asset, export_command))

        # Execute the export command
        try:
            cmds.AbcExport(j=export_command)
            alembic_filepaths.append(alembic_filepath)
        except Exception as e:
            print("Alembic export failed for {}: {}".format(asset, e))

    return alembic_filepaths

def maya_motion_export(frame_start, frame_end, file_format, video_format, fps, filepath=None):
    """
    Export the current Maya scene to either QuickTime (.mov) format (with H.264 codec)
    or MP4 using a workaround (convert .mov to .mp4).
    """
    if video_format == "MPEG4":
        # Use QuickTime (MOV) as an intermediate format (then convert to MP4 externally)
        extension = ".mov"
    elif video_format == "QUICKTIME":
        extension = ".mov"
    else:
        raise Exception("Invalid video_format error")

    filepath = filepath or utils.getTempFilepath(extension)
    print(f"Generated file path: {filepath}")

    # Set playblast options for QuickTime export
    playblast_options = {
        'format': 'qt',  # QuickTime format (required for H.264)
        'compression': 'H.264',  # H.264 codec for video compression
        'filename': filepath,
        'forceOverwrite': True,
        'clearCache': True,
        'viewer': False,
        'showOrnaments': False,
        'percent': 100,
        'quality': 100,
        'widthHeight': (1920, 1080),  # You can change this based on your requirements
        'startTime': frame_start,
        'endTime': frame_end,
        'framePadding': 4        
    }
    print(f"Playblast options: {playblast_options}")

    # Set frame rate (time unit, not FPS directly)
    if fps == 30:
        cmds.currentUnit(time='ntsc')
    elif fps == 25:
        cmds.currentUnit(time='pal')
    else:
        cmds.currentUnit(time='film')

    # Execute the playblast command
    try:
        result = cmds.playblast(**playblast_options)
        print(f"Playblast result: {result}")
    except Exception as e:
        print(f"MP4 export failed: {e}")
        return None

    print("Executed the playblast command")

    # If the video format is MPEG4, convert the MOV file to MP4
    if video_format == "MPEG4":
        mp4_filepath = filepath.replace(".mov", ".mp4")
        convert_mov_to_mp4(filepath, mp4_filepath)
        return mp4_filepath

    return filepath

def convert_mov_to_mp4(mov_filepath, mp4_filepath):
    """
    Convert a MOV file to MP4 using FFMPEG.
    """
    import subprocess

    command = [
        "ffmpeg",
        "-i", mov_filepath,
        "-vcodec", "libx264",
        "-acodec", "aac",
        "-strict", "experimental",
        mp4_filepath
    ]

    print("Converting MOV to MP4: {}".format(command))
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("FFMPEG output: {}".format(result.stdout.decode()))
        print("FFMPEG error (if any): {}".format(result.stderr.decode()))
        print("Successfully converted MOV to MP4: {}".format(mp4_filepath))
    except subprocess.CalledProcessError as e:
        print("Failed to convert MOV to MP4: {}".format(e))
        raise

def gather_texture_nodes():
    """
    Gather all texture nodes in the current Maya scene.
    """
        # Gather all texture nodes
    texture_nodes = cmds.ls(type="file")
    if not texture_nodes:
        raise Exception("Error: No texture nodes found in the scene")

    # Get the original file paths of the texture nodes
    texture_filepaths = []
    for node in texture_nodes:
        file_path = cmds.getAttr(f"{node}.fileTextureName")
        texture_filepaths.append(file_path)

    print("Successfully gathered texture file paths")
        
    return texture_filepaths

def reconnect_source_with_images(sourceImages_filepaths):
    """
    Reconnect the existing source file with the latest version of source images.
    """

    # Ensure sourceImages_filepaths is a list
    if isinstance(sourceImages_filepaths, str):
        sourceImages_filepaths = [sourceImages_filepaths]

    # Iterate over the texture file paths and reconnect them
    for texture_filepath in sourceImages_filepaths:
        # Get the base file name without the extension
        baseFileName = utils.getBaseFileName(texture_filepath)

        # Find the corresponding file node in Maya
        file_nodes = cmds.ls(type="file")

        if not file_nodes:
            raise Exception("Error: No file nodes found in the scene")
        for node in file_nodes:
            file_texture_name = cmds.getAttr(f"{node}.fileTextureName")

            if baseFileName in file_texture_name:
                # Reconnect the file node with the new texture file path
                cmds.setAttr(f"{node}.fileTextureName", texture_filepath, type="string")
                # Save the changes to the scene
                cmds.file(save=True)
    
    
    print("Scene saved successfully with the reconnected texture file paths.")

def export_shader_networks(filepath=None):
    """
    Export all shader networks in the Hypershade window to the target file path.
    """
    # Setting up temp file path for exporting shader network
    filepath = filepath or utils.getTempFilepath(".mb")
    # Select all shading nodes
    shading_nodes = cmds.ls(materials=True)
    if not shading_nodes:
        raise Exception("Error: No shading nodes found in the scene")

    # Select all shading nodes
    cmds.select(shading_nodes, replace=True)

    # Export selected shading nodes to the target file path
    cmds.file(filepath, exportSelected=True, type="mayaBinary", force=True)
    return filepath

def export_shader_network_metadata(filepath=None):

    # Initialize the json file to store the shader network metadata
    
    # Setting up temp file path for exporting shader network metadata
    filepath = filepath or utils.getTempFilepath(".json")

    utils.initialize_json_file(filepath)

    # Gather all shading nodes in the scene   
    shadingEngines = cmds.ls(type="shadingEngine")

    result = []
    for shadingEngine in shadingEngines:
        shader = cmds.listConnections("{}.surfaceShader".format(shadingEngine), source=True, destination=False)
        #cmds.listConnections("blinn1SG.surfaceShader", source=True, destination=False)
        mesh = cmds.sets(shadingEngine, query=True)
        content = {"shadingEngine": shadingEngine, "shader": shader[0], "mesh": mesh}
        result.append(content)

    utils.writeJson(filepath, result)
    return filepath


# Correct approach: Traverse all the nodes and extract all the geometry from the nodes of the asset hierarchy