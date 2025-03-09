import os
import json
import tempfile
import logging

logging.basicConfig(level=logging.INFO)


def environmantValue(key):
    return os.environ[key]

def initialize_json_file(json_file):
    # Initialize the JSON database if it doesn't exist
    if not os.path.exists(json_file):
        with open(json_file, "w") as file:
            json.dump([], file, indent=4)  # Empty list to store artist data

def readJson(filepath):
    # Reads the json filepath passed and returns the data
    with open(filepath, 'r') as openfile:
        return json.load(openfile)    

def writeJson(filepath, data):
    # Save updated domain database
    with open(filepath, "w") as file:
        json.dump(data, file, indent=4)


# def readJsonFile(sourcefile):
#     with open(sourcefile, "r") as file:
#         data = json.load(file)
#     return data


# def writeJson(data):

#     filepath = os.path.join(os.path.expandvars("%DATABASE_PATH%/versions.json"))
#     finalData = [data]

#     if os.path.exists(filepath):
#         with open(filepath, "r") as file:
#             finalData = json.load(file)  
#             finalData.append(data)

#     with open(filepath, "w") as file:
#         file.write(json.dumps(finalData, indent=4)) 



def getProjectName():
    return os.environ["PROJECT_NAME"]


def getProjectPath(project):
    """
    Get project details from database by ID
    """
    
    return os.path.abspath(os.path.join(os.environ["PROJECT_PATH"], project))

    return None


def departmentPath(category, name, department, project):
    """
    category = "asset"
    name = "human"
    department = "modeling"
    utils.departmentPath(category, name, department)
    """

    return  os.path.abspath(os.path.join(getProjectPath(project), category, name, department))


def fileExtension(filepath):   
    dirname, extension = os.path.splitext(filepath)
    
    return extension

def getFilePath(filepath):
    """
    Get the directory path of a file without the file name and extension.
    """
    directory_path = os.path.dirname(filepath)
    return directory_path
     
     
def getTempDirectory():
    """
    Generate a temporary directory path.
    """
    temp_dir = tempfile.mkdtemp()
    return temp_dir


def getTempFilepath(extension):
    """
    Generate a temporary file path with the specified extension.
    """
    temp_dir = tempfile.gettempdir()

    # Ensure the temporary directory exists
    tempfile.tempdir = temp_dir
        
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=extension)
    temp_file.close()
    return temp_file.name

def getBaseFileName(filepath):
    """
    Get the file name from the file path.
    """
    base_name = os.path.basename(filepath)
    baseFileName, _ = os.path.splitext(base_name)
    return baseFileName


def getVersionFilepath(category, name, department, project, typed, version, extension, fileName=None):
 
    department_path = departmentPath(category, name, department, project)
    if typed != "sourceimages" and department != "animation":
        fileName = name

    filepath = os.path.join(
        department_path,
        typed,
        version,
        "{}{}".format(fileName, extension),
    )
    
    return filepath

# def getCurrentVersion(category, name, department, typed):
#     """
#     Get the current version of a file for a specific combination of category, name, department, and typed.
#     If no current version exists, return None.
#     """
#     version_file = os.path.expandvars("%DATABASE_PATH%/versions.json")
#     if os.path.exists(version_file):
#         versions = readJsonFile(version_file)
#         # Filter versions based on category, name, department, project and typed
#         filtered_versions = [
#             version for version in versions
#             if version["category"] == category and
#                version["name"] == name and
#                version["department"] == department and
#                version["project"] == getProjectName() and
#                version["type"] == typed
#         ]
        
#         if filtered_versions:
#             return filtered_versions[-1]["version"]  # Return the latest version for the filtered combination
#     return None



def nextVersion(currentVersion):
    """
    Get the next version of a file. If no current version exists, start with 'v1'.
    """
    if currentVersion:  # If current version exists, proceed
        version_number = int(currentVersion[1:])  # Extracts the number part from the version string
        next_version = "v{}".format(version_number + 1)  # Using .format() for compatibility
        next_version = "v{}".format(version_number + 1)  # Using .format() for compatibility
    else:
        next_version = "v1"
    
    return next_version