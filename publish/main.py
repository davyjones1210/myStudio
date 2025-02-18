import logging
import importlib

from publish import utils
from publish import blender_publish

importlib.reload(utils)
importlib.reload(blender_publish)

logging.basicConfig(level=logging.INFO)


def sourceFile(category, name, department):
    """
    import importlib
    from publish import main
    importlib.reload(main)
    result = main.sourceFile("asset", "monkey", "modeling")
    """

    print("\n\n")

    logging.info("Begins source file publish")

    # Get Source File
    source_filpath = blender_publish.source()

    logging.info("1: Successfully extarct current source file, {}".format(source_filpath))

    # registertation
    # adds entry in the database of this particular publish. A way to track the file.

    # Example: 
    # import importlib

    # from publish import main
    # importlib.reload(main)

    # result = main.sourceFile("asset", "monkey", "modeling")

    # print(result)
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
 



def moviePublish(category, name, department):
    """
    from publish import main. Right now not doing anything.

    """

    result, output = main.movie(category, name, department)

    print("\n", result, output)

    if result:
        main.register_version(category, name, department)

    else:
        logging.error("Your publish failed: %s" % output)


