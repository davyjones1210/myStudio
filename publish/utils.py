import os
import json
import tempfile
import logging

logging.basicConfig(level=logging.INFO)

def readJsonFile(sourcefile):
    with open(sourcefile, "r") as file:
        data = json.load(file)
    return data


def writeJson(data):

    filepath = os.path.join(os.path.expandvars("%DATABASE_PATH%/versions.json"))
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
    print("Filepath passed to fileExtension: ", filepath)
    dirname, extension = os.path.splitext(filepath)
    return extension
     

def getTempFilepath(extension):
    return "{}{}".format(tempfile.mkdtemp(), extension)


def getVersionFilepath(category, name, department, typed, version, extension):
 
    department_path = departmentPath(category, name, department)

    filepath = os.path.join(
        department_path,
        typed,
        version,
        "{}{}".format(name, extension),
    )  
    
    return filepath

def getCurrentVersion(category, name, department, typed):
    """
    Get the current version of a file for a specific combination of category, name, department, and typed.
    If no current version exists, return None.
    """
    version_file = os.path.expandvars("%DATABASE_PATH%/versions.json")
    if os.path.exists(version_file):
        versions = readJsonFile(version_file)
        # Filter versions based on category, name, department, and typed
        filtered_versions = [
            version for version in versions
            if version["category"] == category and
               version["name"] == name and
               version["department"] == department and
               version["project"] == getProjectName() and
               version["type"] == typed
        ]
        print("Filtered versions = ", filtered_versions)
        if filtered_versions:
            return filtered_versions[-1]["version"]  # Return the latest version for the filtered combination
    return None

def nextVersion(currentVersion):
    """
    Get the next version of a file. If no current version exists, start with 'v1'.
    """
    if currentVersion:  # If current version exists, proceed
        version_number = int(currentVersion[1:])  # Extracts the number part from the version string
        next_version = f"v{version_number + 1}"
    else:
        next_version = "v1"
    
    return next_version