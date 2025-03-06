import maya.cmds as cmds
from publish import utils



def maya_source():
    """
    Execute the publish process
    """
    source_filpath = cmds.file(query=True, sceneName=True)

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

def movie(category, name, department):
    """
    Execute the publish process
    """
    path = utils.departmentPath(category, name, department)

    # path = %PROJECT_PATH%test1/asset/human/modeling
    # path = %PROJECT_PATH%test1/shot/shot1/modeling

    

    print(path)

    # To extact the move file

    return "/temp/human.mov", True


def register_version(category, name, department):

    # Find the latest version input args

    # To add new entry in the database with new version
    pass