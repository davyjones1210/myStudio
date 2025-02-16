from publish import utils

from maya import cmds

def source(category, name, department):
    """
    Execute the publish process
    """
    path = utils.departmentPath(category, name, department)

    # path = %PROJECT_PATH%test1/asset/human/modeling
    # path = %PROJECT_PATH%test1/shot/shot1/modeling

    print(path)

    # To extact the source file

    return "/temp/human.ma"


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