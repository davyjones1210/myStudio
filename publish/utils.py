import os
import json

def readJsonFile(sourcefile):
    with open(sourcefile, "r") as file:
        data = json.load(file)
    return data


def getProjectName():
    return os.environ["PROJECT_NAME"]


def getProjectPath():
    """
    Get project details from database by ID
    """
    
    projects = readJsonFile(os.path.expandvars("%DATABASE_PATH%/projects.json"))

    for project in projects:
        if project["name"] == getProjectName():
            return os.path.abspath(os.path.join(os.environ["PROJECT_PATH"], project["name"]))

    return None


def departmentPath(category, name, department):
    """
    category = "asset"
    name = "human"
    department = "modeling"
    utils.departmentPath(category, name, department)
    """

    return  os.path.abspath(os.path.join(getProjectPath(), category, name, department))
