import logging

from publish import utils
from publish import blender_publish

logging.basicConfig(level=logging.INFO)

def sourceFile(category, name, department):
    """
    import importlib
    from publish import main
    importlib.reload(main)
    result = main.sourceFile("asset", "monkey", "modeling")
    print(result)
    """

    print("\n\n")

    logging.info("Begins source file publish")

    # Get Source File
    source_filpath = blender_publish.source()

    logging.info("1: Successfully extarct current source file, {}".format(source_filpath))

    # registertation
    # adds entry in the database of this particular publish. A way to track the file.
    # Types of source files: sourcefile, usd, dailies, movs, etc. This helps identify what kind of publish it is.

    #     
    register_result = blender_publish.register(category, name, department, "sourcefile")
    logging.info("2: Successfully registered in our data base, {} {} {}".format(name, department, register_result["version"]))

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

    blender_publish.deployed(
        source_filpath,
        target_filepath,
    )

    logging.info("3: Successfully deployed version called {}, file path is {}".format(register_result["version"], target_filepath))


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
    
    register_result = blender_publish.register(category, name, department, "usdFile")

    extension = utils.fileExtension(usd_filpath)

    target_filepath = utils.getVersionFilepath(
        category,
        name,
        department,
        "usdFile",
        register_result["version"],
        extension,
    )

    blender_publish.deployed(
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

    register_result = blender_publish.register(category, name, department, "alembicFile")

    extension = utils.fileExtension(alembic_filpath)

    target_filepath = utils.getVersionFilepath(
        category,
        name,
        department,
        "alembicFile",
        register_result["version"],
        extension,
    )

    blender_publish.deployed(
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
    mp4_filepath = blender_publish.mp4_export("FFMPEG", "MPEG4", 1, 5, 24, filepath=None)    

    register_result = blender_publish.register(category, name, department, "mp4File")

    extension = utils.fileExtension(mp4_filepath)

    target_filepath = utils.getVersionFilepath(
        category,
        name,
        department,
        "mp4File",
        register_result["version"],
        extension,
    )

    blender_publish.deployed(
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
    
    mov_filepath = blender_publish.mov_export("FFMPEG", "QUICKTIME", 1, 5, 24, filepath=None)    

    register_result = blender_publish.register(category, name, department, "movFile")

    extension = utils.fileExtension(mov_filepath)

    target_filepath = utils.getVersionFilepath(
        category,
        name,
        department,
        "movFile",
        register_result["version"],
        extension,
    )

    blender_publish.deployed(
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