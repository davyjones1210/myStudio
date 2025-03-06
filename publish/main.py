import logging
import importlib
from publish import utils
from publish import broadcast

# Reload modules to ensure the latest changes are loaded
importlib.reload(broadcast)
importlib.reload(utils)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Global variable to store the current DCC software
PUBLISH_DCC = None


def dcc_context(frame_start, frame_end, category, name, department, PUBLISH_DCC, typed="sourcefile"):
    """
    Determine the context for the DCC software and execute the appropriate export function.
    """
    if not PUBLISH_DCC:
        raise Exception("Error: Could not set current publish software")

    logging.info("Begins source file publish")

    try:
        if PUBLISH_DCC == "blender":
            from publish import blender_scene
            importlib.reload(blender_scene)
            if typed == "sourcefile":
                return blender_scene.source()
            elif typed == "usdFile":
                return blender_scene.usd_export(False, False, True, False, filepath=None)
            elif typed == "alembicFile":
                return blender_scene.alembic_export(False, True, True, True, filepath=None)
            elif typed == "mp4File":
                return blender_scene.motion_export("FFMPEG", "MPEG4", 1, 5, 24, filepath=None)
            elif typed == "movFile":
                return blender_scene.motion_export("FFMPEG", "QUICKTIME", 1, 5, 24, filepath=None)

        if PUBLISH_DCC == "maya":
            from publish import maya_scene
            importlib.reload(maya_scene)
            if typed == "sourcefile":
                return maya_scene.maya_source()
            elif typed == "usdFile":
                return maya_scene.maya_usd_export(frame_start, frame_end, False, True, True, False, filepath=None)
            elif typed == "alembicFile":
                return maya_scene.maya_alembic_export(frame_start, frame_end, False, True, filepath=None)
            elif typed == "mp4File":
                return maya_scene.maya_motion_export(frame_start, frame_end, "FFMPEG", "MPEG4", 24, filepath=None)
            elif typed == "movFile":
                return maya_scene.maya_motion_export(frame_start, frame_end, "FFMPEG", "QUICKTIME", 24, filepath=None)
    except Exception as e:
        logging.error("Error during DCC context operation: %s", str(e))
        raise

    raise Exception("Error: Unsupported DCC software or invalid type")
        # Add optional argument for frame ranges. Eg: startframe=1001, endframe=1020
        # New task: Assemble scene, version management, publish
        # Layout scene assembly - publish assets (.mb file), reference assets, bring into layout scene

def check_source_filepath(source_filpath):
    """
    Check if the source file path is set properly.
    """
    if not source_filpath:
        raise Exception("Error: source file path could not be determined")
    logging.info("1: Successfully extracted current source file, {}".format(source_filpath))

def register_version(category, name, department, typed, PUBLISH_DCC, comments):
    """
    Register the publish in the database.
    """
    register_result = broadcast.register(
        category,
        name,
        department,
        typed,
        PUBLISH_DCC,
        comments,
    )
    logging.info("2: Successfully registered in our data base, {} {} {} {}".format(
        name, department, register_result["version"], typed
    ))

    return register_result

def deploy_target_filepath(source_filpath, category, name, department, typed, register_result):
    """
    Deploy the file for distribution.
    """
    extension = utils.fileExtension(source_filpath)
    project = utils.getProjectName()
    fileName = utils.getBaseFileName(source_filpath)
    
    print("register_result: {}".format(register_result))
    print("register_result type: {}".format(type(register_result)))

    target_filepath = utils.getVersionFilepath(
        category,
        name,
        department,
        project,
        typed,
        register_result["version"],
        extension,
        fileName,
    )

    broadcast.deployed(
        source_filpath,
        target_filepath,
    )

    logging.info(
        "3: Successfully deployed version called {}, file path is {}".format(
            register_result["version"], target_filepath
        )
    )

def sourceFile(frame_start, frame_end, category, name, department, typed, comments):
    """
    import importlib
    from publish import main
    importlib.reload(main)
    main.PUBLISH_DCC = "blender"
    result = main.sourceFile("asset", "monkey", "modeling", "sourcefile")
    print(result)

    from publish import main
    import importlib
    importlib.reload(main)
    main.PUBLISH_DCC = "maya"
    result = main.sourceFile(1001, 1020, "shot", "shot-101", "layout", "sourcefile", "test comment")

    Publish the source file for the given category, name, and department.
    """

    print("\n\n")

    source_filpath = dcc_context(frame_start, frame_end, category, name, department,PUBLISH_DCC, typed)

    # Check if source_filpath is set properly
    check_source_filepath(source_filpath)

    # Register the publish in the database
    register_result = register_version(category, name, department, typed, PUBLISH_DCC, comments)
    

    # Deploy the file for distribution
    deploy_target_filepath(source_filpath, category, name, department, typed, register_result)


def sourceImages(category, name, department, typed, comments):
    """
    from publish import main
    import importlib
    importlib.reload(main)
    main.PUBLISH_DCC = "maya"
    result = main.sourceImages("asset", "alien", "texture", "sourceimages", "test comment")
    print("Texture file paths: {}".format(result))

    Publish the source images for the given category, name, and department.
    """
    logging.info("Begins source images publish")


    # Ensure the current DCC software is set to Maya
    if PUBLISH_DCC != "maya":
        raise Exception("Error: Current publish software is not set to Maya")
    
    from publish import maya_scene
    importlib.reload(maya_scene)

    # Gather texture nodes and get their file paths
    texture_filepaths = maya_scene.gather_texture_nodes()

    # Register the publish in the database
    register_result = register_version(category, name, department, typed, PUBLISH_DCC, comments)

    # Deploy each texture file for distribution
    for texture_filepath in texture_filepaths:
        # Check if texture_filepath is set properly
        check_source_filepath(texture_filepath)

        # Deploy the file for distribution
        deploy_target_filepath(texture_filepath, category, name, department, typed, register_result)

    return texture_filepaths




# This is for source file publish. Create a new function for USD and Alembic publish
# Next exercise: Export alembic and movie. Find out how to export movie in Blender. .mov or .ava format
# After that, same process for rigging and surfacing.

# Notes
# Understand the code, don't try to understand code line by line
# Avoid legacy steps

# Exercise for 20-2-2025 - finish lookdev publish - source file & usd file.
# Now we have all types of publishing files available for all types of publishing
# In real life (studio requirements), for modeling, use usd or alembic with source file. For rigging, source file is enough
# For alembic publish, also publish a thumbnail image for presentation.
# Dependeancies - mdl > lookdev > rigging
# Q: Create another function called build or generate 