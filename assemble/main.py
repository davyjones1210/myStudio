import logging
import importlib
from assemble import utils
importlib.reload(utils)


logging.basicConfig(level=logging.INFO)

PUBLISH_DCC = None


def search(PUBLISH_DCC, category, name, department, typed, version=None, approved=True):
    """
    Use this fucntion to search for versions in the specific context passed as argument. Just search for it
    """
    # 1. find versions database
    # 2. Search for latest version of typed file and arguments passed
    # 3. Return info
    
    return utils.getVersion(PUBLISH_DCC, category, name, department, typed, version, approved)


def sourceFile(category, name, department, typed, version=None, approved=True):
    """
        latest approved or latest or specific version can be able to load in downstrem deparatment  to begin their work

        result = main.sourceFile("asset", "monkey", "modeling")
        or
        result = main.sourceFile("asset", "monkey", "modeling", version=v5)
        or 
        result = main.sourceFile("asset", "monkey", "modeling", version="latest", approved=True)
        or
        result = main.sourceFile("asset", "monkey", "modeling", version="latest", approved=False)   

        Find the proper version and generate the path.  

    """

    if not PUBLISH_DCC:
        raise Exception("Error could not set currennt publish software")

    logging.info("0. Begins source file search")

    # Search Source File
    if PUBLISH_DCC == "blender":
        import bpy
        searched_version = search(PUBLISH_DCC, category, name, department, typed, version, approved) 
        print("Filtered version: ", searched_version)
        logging.info("\1. successfully found specified version")        
        # If that version exists get the file path where the source file is saved
        if searched_version:
            version_path = utils.getFilepath(searched_version)
            print("Version path: ", version_path)
            logging.info("\2. successfully located specified version path")

            # Load the .blend file in Blender using bpy
            bpy.ops.wm.open_mainfile(filepath=version_path)
            logging.info("\3. successfully opened {} version in dcc".format(searched_version["version"]))

    if PUBLISH_DCC == "maya":
        import maya.cmds as cmds
        searched_version = search(PUBLISH_DCC, category, name, department, typed, version, approved)
        logging.info("\1. successfully found specified version")
        
        # If that version exists get the file path where the source file is saved
        if searched_version:
            version_path = utils.getFilepath(searched_version)
            print("Version path: ", version_path)
            logging.info("\2. successfully located specified version path")

            # Load the .ma file in Maya using cmds
            cmds.file(version_path, open=True, force=True)
            logging.info("\3. successfully opened {} version in dcc".format(searched_version["version"]))

    
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
    result = main.sourceFile("asset", "dobby", "rigging", "sourcefile")
    """

    # 1. Search for all versions in the specified context.
    # 2. Retrieve file path of searched version
    # 3. Open/load file on dcc from that file path
    # Figure out steps as exercise.
    # Final outcome: Have that input file to be imported and opened in blender where artists can start the work on the file.
