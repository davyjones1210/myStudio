import logging
import importlib
from publish import utils
from publish import broadcast

import importlib
importlib.reload(broadcast)
importlib.reload(utils)

logging.basicConfig(level=logging.INFO)

PUBLISH_DCC = None


def dcc_context(frame_start, frame_end, category, name, department, PUBLISH_DCC, typed="sourcefile"):
    if not PUBLISH_DCC:
        raise Exception("Error could not set current publish software")

    logging.info("Begins source file publish")

    # Get Source File
    try:

        if PUBLISH_DCC == "blender":
            from publish import blender_scene
            importlib.reload(blender_scene)
            if typed=="sourcefile":
                return blender_scene.source()
            elif typed=="usdFile":
                return blender_scene.usd_export(False, False, True, False, filepath=None)
            elif typed=="alembicFile":
                return blender_scene.alembic_export(False, True, True, True, filepath=None)
            elif typed=="mp4File":
                return blender_scene.motion_export("FFMPEG", "MPEG4", 1, 5, 24, filepath=None)
            elif typed=="movFile":
                return blender_scene.motion_export("FFMPEG", "QUICKTIME", 1, 5, 24, filepath=None) 

        if PUBLISH_DCC == "maya":
            from publish import maya_scene
            importlib.reload(maya_scene)
            if typed=="sourcefile":
                return maya_scene.maya_source()
            elif typed=="usdFile":
                return maya_scene.maya_usd_export(False, False, True, False, filepath=None)
            elif typed=="alembicFile":
                return maya_scene.maya_alembic_export(False, True, 1, 5, filepath=None)
            elif typed=="mp4File":
                return maya_scene.maya_motion_export(frame_start, frame_end, "FFMPEG", "MPEG4",24, filepath=None) 
            elif typed=="movFile":
                return maya_scene.maya_motion_export(frame_start, frame_end, "FFMPEG", "QUICKTIME", 24, filepath=None)
    except Exception as e:
        logging.error("Error during DCC context operation: %s", str(e))
        raise

    raise Exception("Error: Unsupported DCC software or invalid type")
        # Add optional argument for frame ranges. Eg: startframe=1001, endframe=1020
        # New task: Assemble scene, version management, publish
        # Layout scene assembly - publish assets (.mb file), reference assets, bring into layout scene


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
    result = main.sourceFile("asset", "dobby", "rigging", "sourcefile")
    """

    print("\n\n")

    source_filpath = dcc_context(frame_start, frame_end, category, name, department,PUBLISH_DCC, typed)

    # Check if source_filpath is set properly
    if not source_filpath:
        raise Exception("Error: source file path could not be determined")

    
    logging.info("1: Successfully extracted current source file, {}".format(source_filpath))

    # registertation
    # adds entry in the database of this particular publish. A way to track the file.
    # Types of source files: sourcefile, usd, dailies, movs, etc. This helps identify what kind of publish it is.

    #     
    
    register_result = broadcast.register(
            category,
            name,
            department,
            typed,
            PUBLISH_DCC,
            comments,
        )

    logging.info("2: Successfully registered in our data base, {} {} {}".format(
            name, department, register_result["version"], typed
        )
    )

    # Deployed
    # Means ready for distribution of the file to be saved somewhere in the project directory for use downstream.
    extension = utils.fileExtension(source_filpath)
    project = utils.getProjectName()

    target_filepath = utils.getVersionFilepath(
        category,
        name,
        department,
        project,
        typed,
        register_result["version"],
        extension,
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