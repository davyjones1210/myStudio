import os
import json

def readJsonFile(sourcefile):
    with open(sourcefile, "r") as file:
        data = json.load(file)
    return data


def writeJson(data):

    filepath = os.path.join(os.path.expandvars("%DATABASE_PATH%/version.json"))
    finalData = [data]

    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            finalData = json.load(file)  
            finalData.append(data)

    with open(filepath, "w") as file:
        file.write(json.dumps(finalData, indent=4)) 

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


def fileExtension(filepath):
    dirname, extension = os.path.splitext(filepath)
    return extension
     

def getVersionFilepath(category, name, department, typed, version, extension):
 
    department_path = departmentPath(category, name, department)

    filepath = os.path.join(
        department_path,
        typed,
        version,
        "{}{}".format(name, extension),
    )    
    
    return filepath


def getCurrentVersion(category, name, department):
    """
    Exercise: Find how to get current version of a file and next version. If no current version exists, start with v1.
    """
    return None


def nextVersion(currentVersion):
    if currentVersion:
        result = currentVersion + 1
    else:
        result = "v1"
    
    return result
