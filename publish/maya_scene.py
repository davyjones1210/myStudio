<<<<<<< HEAD
import maya.cmds as cmds
from publish import utils



def maya_source():
=======
from publish import utils
from publish import broadcast

from maya import cmds

def source():
>>>>>>> b61cdeca6964b9e85b5ab0ec66322390d0c9e504
    """
    Execute the publish process
    """
    source_filpath = cmds.file(query=True, sceneName=True)

    if not source_filpath:
        raise Exception("Error: Maya scene has not been saved. Please save the scene before publishing.")

<<<<<<< HEAD
    return source_filpath

def maya_usd_export(selected=False, animation=False, uvmaps=False, materials=False, filepath=None):
    """
    Export the current Maya scene to USD format.
    """
    filepath = filepath or utils.getTempFilepath(".usda")

    print(f"Generated file path: {filepath}")

    # Ensure the USD plugin is loaded
    if not cmds.pluginInfo('mayaUsdPlugin', query=True, loaded=True):
        cmds.loadPlugin('mayaUsdPlugin')

    # Set export options
    # Set export options
    export_options = [
        "exportUVs={}".format(int(uvmaps)),
        "exportSkels=none",
        "exportSkin=none",
        "exportBlendShapes=0",
        "exportDisplayColor=0",
        "exportColorSets=1",
        "exportComponentTags=1",
        "defaultMeshScheme=catmullClark",
        "animation={}".format(int(animation)),
        "eulerFilter=0",
        "staticSingleSample=0",
        "startTime=1",
        "endTime=1",
        "frameStride=1",
        "frameSample=0.0",
        "defaultUSDFormat=usdc",
        "rootPrim=",
        "rootPrimType=scope",
        "defaultPrim=nurbsCube1",
        "exportMaterials={}".format(int(materials)),
        "shadingMode=useRegistry",
        "convertMaterialsTo=[UsdPreviewSurface]",
        "exportAssignedMaterials=1",
        "exportRelativeTextures=automatic",
        "exportInstances=1",
        "exportVisibility=1",
        "mergeTransformAndShape=1",
        "includeEmptyTransforms=1",
        "stripNamespaces=0",
        "worldspace=0",
        "exportStagesAsRefs=1",
        "excludeExportTypes=[]",
        "legacyMaterialScope=0"
    ]

    if selected:
        selected_objects = cmds.ls(selection=True)
        if not selected_objects:
            raise RuntimeError("No objects selected for export.")
        export_options.append("exportSelected=1")
    else:
        export_options.append("exportSelected=0")

    # Construct the export command
    export_command = '-file "{}" -options "{}"'.format(filepath.replace("\\", "/"), ";".join(export_options))
    print(f"Export command: {export_command}")
    # Execute the export command
    try:
        cmds.evalDeferred(lambda: cmds.mayaUsdExport(file=filepath, options=";".join(export_options)))
    except Exception as e:
        print(f"USD export failed: {e}")
        return None

    return filepath

def maya_alembic_export(selected=False, animation=False, start_frame=1, end_frame=1, filepath=None):
    """
    Export the current Maya scene to Alembic format.
    """
    filepath = filepath or utils.getTempFilepath(".abc")

    # Ensure the AbcExport plugin is loaded
    if not cmds.pluginInfo('AbcExport', query=True, loaded=True):
        cmds.loadPlugin('AbcExport')

    # Set export options
    export_options = [
        "-frameRange", str(start_frame), str(end_frame),
        "-uvWrite",
        "-worldSpace",
        "-writeVisibility",
        "-dataFormat", "ogawa"
    ]

    if selected:
        selected_objects = cmds.ls(selection=True)
        if not selected_objects:
            raise RuntimeError("No objects selected for export.")
        for obj in selected_objects:
            export_options.append("-root")
            export_options.append(obj)

    # Construct the export command
    export_command = ' '.join(export_options) + ' -file "{}"'.format(filepath.replace("\\", "/"))

    print(f"Export command: {export_command}")
    # Execute the export command
    try:
        cmds.AbcExport(j=export_command)
    except Exception as e:
        print(f"Alembic export failed: {e}")
        return None

    return filepath


def maya_motion_export(file_format, video_format, frame_start, frame_end, fps, filepath=None):
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

    return filepath


=======

    return source_filpath

>>>>>>> b61cdeca6964b9e85b5ab0ec66322390d0c9e504

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