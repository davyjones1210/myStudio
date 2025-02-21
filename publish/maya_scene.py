from publish import utils
from publish import broadcast

from maya import cmds

def source():
    """
    Execute the publish process
    """
    source_filpath = cmds.file(query=True, sceneName=True)

    if not source_filpath:
        raise Exception("Error: Maya scene has not been saved. Please save the scene before publishing.")


    return source_filpath


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