import os
import json
import tempfile
import logging
import importlib
from publish import utils  as publish_utils
importlib.reload(publish_utils)

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

def getVersion(PUBLISH_DCC, category, name, department, typed, v=None, approved=True):
    """
    Get the latest version of a file for a specific combination of category, name, department, and typed.
    If no current version exists, return None.
    """
    version_file = os.path.expandvars("%DATABASE_PATH%/versions.json")
    if os.path.exists(version_file):
        versions = readJsonFile(version_file)
        # Filter versions based on category, name, department, project and typed
        filtered_version = [
            version for version in versions
            if version["category"] == category and
               version["name"] == name and
               version["department"] == department and
               version["project"] == getProjectName() and
               version["type"] == typed and
               ("software" not in version or version["software"] == PUBLISH_DCC) and
               (v is None or version["version"] == v) and
               (not approved or version.get("status") == "Approved" or "status" not in version)
        ]
        
        if filtered_version:
            return filtered_version[-1]  # Return the latest version for the filtered combination
    return None

def getFilepath(version):
    # Parsing the various arguments from the version argument passed

    category = version["category"]
    name = version["name"]
    department = version["department"]
    typed = version["type"]
    v = version["version"]
    
    if ("software" not in version or version["software"] == 'blender'):
        extension = ".blend"
    elif version["software"] == 'maya':
        extension = ".ma"
    return publish_utils.getVersionFilepath(category, name, department, typed, v, extension)