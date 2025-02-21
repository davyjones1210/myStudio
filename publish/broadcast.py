import os
import shutil
import getpass
import datetime

from publish import utils

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

