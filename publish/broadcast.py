import os
import shutil
import getpass
import datetime
from pprint import pprint  # Import pprint module

from publish import utils
from publish import database

PROJECT_FIELDS = [
    "id",
    "name",
    "createdBy",
    "createdAt",
    "description",
    "remark",
]

ARTISTS_FIELDS = [
    "id",
    "email",
    "name",
    "password",
]




def getAllCategories():
    db = database.myDatabase()
    return db.query("category", "name")

def getAllDepartments():
    db = database.myDatabase()
    return db.query("departments", "name")

def getAllProjects():
    db = database.myDatabase()
    return db.query("projects", "name, id")

def getAllDomains():
    db = database.myDatabase()
    return db.query("domains", "name")

def getCategoryFromDomain(name, projectID=None):
    projectID = projectID or int(utils.environmantValue("PROJECT_ID"))
    
    #Query domain from domain table filter based name and project id
    category = "Asset"
    index = 0

    return category, index

def checkIfDomainExistsInDB(domain_name):
    # Check if domain name exists in domains database

    domain_found = False  # Flag to track if domain name is found
    db = database.myDatabase()
    domains = db.query("domains", "name, id")

    # Check if the domain already exists
    for domain in domains:
        if domain["name"].lower() == domain_name.lower():  # Case-insensitive match
            domain_found = True  # Set flag to True if a match is found
            print(
                "\nDomain '{}' already exists with ID {}".format(
                    domain["name"], domain['id']
                )
            )
            # Setup an environment variable for domain
            os.environ["DOMAIN_NAME"] = domain["name"]
            os.environ["DOMAIN_ID"] = str(domain["id"])

            print("\nDomain env set to: ", os.environ["DOMAIN_NAME"], os.environ["DOMAIN_ID"])
            return True
    if not domain_found:
        print(f"\nDomain does not exist in database. Please add domain in database using create-domain flag")
        return False

def checkIfProjectExistsInDB(project_name):
    # check if project name exists in projects database

    project_found = False # Flag to track if project name is found            
    db = database.myDatabase()
    projects = db.query("projects", "name, id")
    
    # Check if the project already exists
    for project in projects:
        if project["name"].lower() == project_name.lower():  # Case-insensitive match
            project_found = True    # Set flag to True if a match is found
            print(
                "\nProject '{}' already exists with ID {}".format(
                    project["name"], project['id']
                )
            )
            # Setup an environment variable for project
            os.environ["PROJECT_NAME"] = project["name"]
            os.environ["PROJECT_ID"] = str(project["id"])
           
            print("\nProject env set to: ", os.environ["PROJECT_NAME"], os.environ["PROJECT_ID"])
            return True             
    if not project_found:
        print(f"\nProject does not exist in database. Please add project in database using create-project flag")
        return False



def _register_(table, data):
    myda = database.myDatabase()
    myda.connect()
    print("Data passed to database: ", data)
    myda.insert(table, data)
    # Print regisering done

def get_category_id(category_name):
    db = database.myDatabase()
    conditions = f"LOWER(name) = LOWER('{category_name}')"
    result = db.query("category", "id", conditions)
    return result[0]['id'] if result else None

def get_department_id(department_name):
    db = database.myDatabase()
    conditions = f"LOWER(name) = LOWER('{department_name}')"
    result = db.query("departments", "department_id", conditions)
    return result[0]['department_id'] if result else None

def get_project_id(project_name):
    db = database.myDatabase()
    conditions = f"LOWER(name) = LOWER('{project_name}')"
    result = db.query("projects", "id", conditions)
    return result[0]['id'] if result else None


def getCurrentVersionFromDB(category, name, department, typed):
    """
    Get the current version of a file for a specific combination of category, name, department, and typed from the database.
    If no current version exists, return None.
    """
    db = database.myDatabase()
    versions = db.query("versions", "category_id, name, department_id, project_id, type, version")
    
    # Get the IDs for category, department, and project
    category_id = get_category_id(category)
    department_id = get_department_id(department)
    project_id = get_project_id(utils.getProjectName())

    # Filter versions based on category_id, name, department_id, project_id and typed
    filtered_versions = [
        version for version in versions
        if version["category_id"] == category_id and
           version["name"].lower() == name.lower() and
           version["department_id"] == department_id and
           version["project_id"] == project_id and
           version["type"].lower() == typed.lower()
    ]

    print("List of available versions:")
    pprint(filtered_versions)  # Use pprint to print the list neatly

    if filtered_versions:
        return filtered_versions[-1]["version"]  # Return the latest version for the filtered combination
    return None



def register(category, name, department, typed, software):
    current_version = getCurrentVersionFromDB(category, name, department, typed)
    next_version = utils.nextVersion(current_version)

    # Get the IDs for category, department, and project
    category_id = get_category_id(category)
    department_id = get_department_id(department)
    project_id = get_project_id(utils.getProjectName())

    # version context
    version_context = {
        "name": name,  # monkey
        "category_id": category_id,  # Asset or shot
        "department_id": department_id,  # modelling, rigging, etc
        "version": next_version,
        "comment": "test publish",
        "project_id": project_id,
        "type": typed,
        "status": "Approved",
        "createdAt": datetime.datetime.now().strftime("%Y/%m/%d - %I:%M"),
        "createdBy": getpass.getuser(),
        "software": software,
    }

    _register_("versions", version_context)
    # utils.writeJson(version_context)

    return version_context


def deployed(source_filpath, target_filepath):

    if not os.path.exists(os.path.dirname(target_filepath)):
        os.makedirs(
            os.path.dirname(target_filepath)
        )
    # This is the exact clone of the user saved file
    shutil.copy(source_filpath, target_filepath)

