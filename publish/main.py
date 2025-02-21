import logging
import shutil

from publish import utils
from publish import broadcast

logging.basicConfig(level=logging.INFO)

PUBLISH_DCC = None


def sourceFile(category, name, department):
    """
    import importlib
    from publish import main
    importlib.reload(main)
    result = main.sourceFile("asset", "monkey", "modeling")
    print(result)
    """

    print("\n\n")

    if not PUBLISH_DCC:
        raise Exception("Error could not set currennt publish software")

    logging.info("Begins source file publish")

    # Get Source File
    if PUBLISH_DCC == "blender":
        from publish import blender_scene
        source_filpath = blender_scene.source()

    if PUBLISH_DCC == "maya":
        from publish import maya_scene
        source_filpath = maya_scene.source()
    
    logging.info("1: Successfully extarct current source file, {}".format(source_filpath))

    # registertation
    # adds entry in the database of this particular publish. A way to track the file.
    # Types of source files: sourcefile, usd, dailies, movs, etc. This helps identify what kind of publish it is.

    #     
    register_result = broadcast.register(
        category,
        name,
        department,
        "sourcefile",
        PUBLISH_DCC,
    )
    logging.info(
        "2: Successfully registered in our data base, {} {} {}".format(
            name, department, register_result["version"]
        )
    )

    # Deployed
    # Means ready for distribution of the file to be saved somewhere in the project directory for use downstream.
    extension = utils.fileExtension(source_filpath)

    target_filepath = utils.getVersionFilepath(
        category,
        name,
        department,
        "sourcefile",
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


def usdFile(category, name, department):
    # Get USD File
    """
    import importlib
    from publish import main
    importlib.reload(main)
    result = main.usdFile("asset", "monkey", "modeling")
    print(result)
    """
    print("\n\n")
    logging.info("Begins usd file publish")

    usd_filpath = blender_publish.usd_export(False, False, True, False, filepath=None)
    
    register_result = broadcast.register(category, name, department, "usdFile", PUBLISH_DCC)

    extension = utils.fileExtension(usd_filpath)

    target_filepath = utils.getVersionFilepath(
        category,
        name,
        department,
        "usdFile",
        register_result["version"],
        extension,
    )

    broadcast.deployed(
        usd_filpath,
        target_filepath,
    )

    logging.info("Successfully deployed version called {}, file path is {}".format(register_result["version"], target_filepath))


def alembicFile(category, name, department):
    # Get alembic File
    """
    import importlib
    from publish import main
    importlib.reload(main)
    result = main.alembicFile("asset", "monkey", "modeling")
    print(result)
    """

    print("\n\n")
    logging.info("Begins alembic file publish")
    alembic_filpath = blender_publish.alembic_export(False, True, True, True, filepath=None)

    register_result = broadcast.register(category, name, department, "alembicFile", PUBLISH_DCC)

    extension = utils.fileExtension(alembic_filpath)

    target_filepath = utils.getVersionFilepath(
        category,
        name,
        department,
        "alembicFile",
        register_result["version"],
        extension,
    )

    broadcast.deployed(
        alembic_filpath,
        target_filepath,
    )

    logging.info("Successfully deployed version called {}, file path is {}".format(register_result["version"], target_filepath))


def mp4File(category, name, department):
    # Get mp4 File
    """
    import importlib
    from publish import main
    importlib.reload(main)
    result = main.mp4File("asset", "monkey", "modeling")
    print(result)
    """
    print("\n\n")
    logging.info("Begins mp4 file publish")

    if not PUBLISH_DCC:
        raise Exception("Error could not set currennt publish software")

    # Get Source File
    if PUBLISH_DCC == "blender":
        from publish import blender_scene
        mp4_filepath = blender_scene.motion_export("FFMPEG", "MPEG4", 1, 5, 24, filepath=None)  

    if PUBLISH_DCC == "maya":
        from publish import maya_scene
        mp4_filepath = maya_scene.motion_export("FFMPEG", "MPEG4", 1, 5, 24, filepath=None) 

    register_result = broadcast.register(category, name, department, "mp4File", PUBLISH_DCC)

    extension = utils.fileExtension(mp4_filepath)

    target_filepath = utils.getVersionFilepath(
        category,
        name,
        department,
        "mp4File",
        register_result["version"],
        extension,
    )

    broadcast.deployed(
        mp4_filepath,
        target_filepath,
    )

    logging.info("Successfully deployed version called {}, file path is {}".format(register_result["version"], target_filepath))


def movFile(category, name, department):
    # Get mov File
    """
    import importlib
    from publish import main
    importlib.reload(main)
    result = main.movFile("asset", "monkey", "modeling")
    print(result)
    """
    print("\n\n")
    logging.info("Begins mov file publish")
    
    if not PUBLISH_DCC:
        raise Exception("Error could not set currennt publish software")

    # Get Source File
    if PUBLISH_DCC == "blender":
        from publish import blender_scene
        mov_filepath = blender_scene.motion_export("FFMPEG", "QUICKTIME", 1, 5, 24, filepath=None)  

    if PUBLISH_DCC == "maya":
        from publish import maya_scene
        mov_filepath = maya_scene.motion_export("FFMPEG", "QUICKTIME", 1, 5, 24, filepath=None) 


    register_result = broadcast.register(
        category, name, department, "movFile",
        PUBLISH_DCC,
    )

    extension = utils.fileExtension(mov_filepath)

    target_filepath = utils.getVersionFilepath(
        category,
        name,
        department,
        "movFile",
        register_result["version"],
        extension,
    )

    broadcast.deployed(
        mov_filepath,
        target_filepath,
    )

    logging.info("Successfully deployed version called {}, file path is {}".format(register_result["version"], target_filepath))


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