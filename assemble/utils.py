import os
import json
import tempfile
import logging
import importlib
from publish import utils  as publish_utils
from publish import database
from pprint import pprint  # Import pprint module

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
    
    db = database.myDatabase()
    conditions = (
        f"category_id = (SELECT id FROM category WHERE LOWER(name) = LOWER('{category}')) AND "
        f"name = '{name}' AND "
        f"department_id = (SELECT department_id FROM departments WHERE LOWER(name) = LOWER('{department}')) AND "
        f"project_id = (SELECT id FROM projects WHERE LOWER(name) = LOWER('{getProjectName()}')) AND "
        f"type = '{typed}'"
    )
    if v is not None:
        conditions += f" AND version = '{v}'"
    if approved:
        conditions += " AND (status = 'Approved' OR status IS NULL)"
    if PUBLISH_DCC:
        conditions += f" AND (software IS NULL OR software = '{PUBLISH_DCC}')"

    
    versions = db.query("versions", "*", conditions)

    # print("Printing all available verions:\n")
    # pprint(versions)
    
    if versions:
        return versions[-1]  # Return the latest version for the filtered combination
    return None

def getCategoryNameById(category_id):
    db = database.myDatabase()
    conditions = f"id = {category_id}"
    result = db.query("category", "name", conditions)
    return result[0]['name'] if result else None

def getDepartmentNameById(department_id):
    db = database.myDatabase()
    conditions = f"department_id = {department_id}"
    result = db.query("departments", "name", conditions)
    return result[0]['name'] if result else None

def getProjectNameById(project_id):
    db = database.myDatabase()
    conditions = f"id = {project_id}"
    result = db.query("projects", "name", conditions)
    return result[0]['name'] if result else None


def getFilepath(version):
    # Parsing the various arguments from the version argument passed
    category_id = version["category_id"]
    name = version["name"]
    department_id = version["department_id"]
    typed = version["type"]
    v = version["version"]
    project_id = version["project_id"]

    
    category = getCategoryNameById(category_id)
    department = getDepartmentNameById(department_id)
    project = getProjectNameById(project_id)

    if "software" not in version or version["software"] == 'blender':
        extension = ".blend"
    elif version["software"] == 'maya':
        # Check for .ma extension first
        extension = ".ma"
        filepath = publish_utils.getVersionFilepath(category, name, department, project, typed, v, extension)
        
        # If the .ma file does not exist, check for .mb extension
        if not os.path.exists(filepath):
            extension = ".mb"
            filepath = publish_utils.getVersionFilepath(category, name, department, project, typed, v, extension)
        
    # Assuming publish_utils.getVersionFilepath can handle IDs instead of names
    return filepath