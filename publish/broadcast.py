import os
import shutil
import getpass
import datetime

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


def getAllDomains():
    # query category from data base table
    return ["Asset", "Shot"]


def getCategoryFromDomain(name, projectID=None):
    projectID = projectID or int(utils.environmantValue("PROJECT_ID"))
    
    #Query domain from domain table filter based name and project id
    category = "Asset"
    index = 0

    return category, index


def _register_(table, data):
    myda = database.myDatabase()
    myda.connect()
    print("Data passed to database: ", data)
    myda.insert(table, data)
    # Print regisering done


def register(category, name, department, typed, software):

    current_version = utils.getCurrentVersion(category, name, department, typed)
    next_version = utils.nextVersion(current_version)

    # version context
    version_context = {
        "name": name, # monkey
        "category": category, #Asset or shot
        "department": department, # modelling, rigging, etc
        "version": next_version,
        "comment": "test publish",
        "project": utils.getProjectName(),
        "type": typed,
        "status": "Approved",
        "createAt": datetime.datetime.now().strftime("%Y/%m/%d - %I:%M"),
        "createBy": getpass.getuser(),
        "software": software,
    }

    utils.writeJson(version_context)

    return version_context


def deployed(source_filpath, target_filepath):

    if not os.path.exists(os.path.dirname(target_filepath)):
        os.makedirs(
            os.path.dirname(target_filepath)
        )
    # This is the exact clone of the user saved file
    shutil.copy(source_filpath, target_filepath)

