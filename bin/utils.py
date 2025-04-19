import os
import json
import logging
# import commonLib.triggerOpen as triggerOpen

# Setup logging
logging.basicConfig(level=logging.INFO)

DOMAIN_CAT = ["asset", "shot"]

ASSET_CAT = [["asset", ["modeling", "rigging", "lookdev", "grooming"]], 
             ["shot", ["layout", "animation", "FX", "lighting/Rendering", "Comp"]]]
# Layout is primary stage of shot animation - setting up shot before camera; more of staging.
# Final animation is done by anim dept

# # Define the JSON file for DCC data
dcc_data_filepath = os.path.expandvars("%CONFIG_PATH%/dcc.json")
# Define the JSON file for artist db
artists_json_file = os.path.expandvars("%DATABASE_PATH%/artists.json")
# Define the JSON file for project db
projects_json_file = os.path.expandvars("%DATABASE_PATH%/projects.json")
# Define the JSON file for domain db
domains_json_file = os.path.expandvars("%DATABASE_PATH%/domains.json")
    

def readJson(filepath):
    # Reads the json filepath passed and returns the data
    with open(filepath, 'r') as openfile:
        return json.load(openfile)    


def collectDCC(name, dcc_data):
    found = False  # Flag to track if DCC name is found
    # Extract and print 'envs' values
    for software in dcc_data:        
        if name == software['name']: 
            found = True  # Set flag to True if a match is found           
            dcc_path = software['path']
            for env in software["envs"]:
                env_name = env["env"]
                env_paths = ";".join(env["path"])  # Join paths with ';'
                os.environ[env_name] = env_paths   # Set environment variable        
            break  # Exit loop after the first match
    else:
        raise Exception("sssssssssssssssssssssssssss")
    
    # later remove this line
    os.environ["PROJECT_ID"] = "201"
    os.environ["DOMAIN_ID"] = "304"
    os.environ["DOMAIN_CATEGORY"] = "Asset"

    os.system(dcc_path)

    if not found:  # If no match was found after looping
        print("DCC name not matching")

def triggerOpen(name):
    # This function opens the DCC software based on the name passed
    
    dcc_data = readJson(dcc_data_filepath)
    # print("Data variable: ", data)
    print("Options.open value passed: ", name)
    collectDCC(name, dcc_data)    

def checkIfProjectExists(project_name):
        # check if project name exists in projects database

        project_found = False # Flag to track if project name is found            
        # Load existing project database
        projects = readJson(projects_json_file)
        
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
        
def checkIfArtistExists(artist_name):
        # check if artist name exists in artists database

        artist_found = False # Flag to track if artist name is found

        artists = readJson(artists_json_file)

        # Check if the artist already exists
        for artist in artists:
            if artist["name"].lower() == artist_name.lower():  # Case-insensitive match
                artist_found = True    # Set flag to True if a match is found 
                print("\nArtist '{}' already exists with ID {}, Email: {}".format(
                artist["name"], artist['id'], artist['email']
                    )
                )
                # Setup an environment variable for artist
                # Create environment varibles which will store this user info
                os.environ["ARTIST_ID"] = str(artist["id"])
                os.environ["ARTIST_NAME"] = artist["name"]
                os.environ["ARTIST_EMAIL"] = artist["email"]
                logging.info("\nArtist env set to\nName: {}, ID: {}, email: {}\n".format(
                    os.environ["ARTIST_NAME"], os.environ["ARTIST_ID"], os.environ["ARTIST_EMAIL"]
                                )
                            )
                return True 
                
        if not artist_found:
            print(f"\nArtist does not exist in database. Please add artist in database using create-artist flag")
            return False
                    


# From this data variable, figure out the specific block from the list, if blender collect blender data, if maya, collect maya
# From the config find out what DCC was typed in cat --opens "here"

def runOpenCommand(options):
    #Checking if artists' name exists in database
    artist_validated = checkIfArtistExists(options.artist)
    #Checking if project name exists in database
    project_validated = checkIfProjectExists(options.project)

    os.environ["DOMAIN_NAME"] = "human"

    if not project_validated:
        logging.warning("Your are not under any projects")             
       
    if artist_validated:      # Trigger open only if artist name & project name match in db          
        print("Triggering opening function now\n")                
        triggerOpen(options.open)  

    # cata --create-domain "ball" --domain_cata "asset"


def set_environments(key, value):
    os.environ[key] = value
    logging.info(f"Environment variable set: {key} = {value}")
            
# Notes:
# os.environ["BLENDER_PLUG_IN_PATH"] = "E:/pipelineDevelopment/test1;E:/pipelineDevelopment/test2",        
# os.environ["BLENDER_SCRIPT_PATH"] = "E:/pipelineDevelopment/test3;E:/pipelineDevelopment/test4",  
# 
# and then launch blender using the path key in json file. And also create a new block for Nuke.
# 
# One more task: Go to cat.py, create a artist by creating a database folder and treat json like a database (table, rows & column). Store artist info like # name, id, email, etc. If an artist database file doesn't exist create it and then edit it going forward.
# In installer.py add another env variable called DATABASE_PATH

# Next, create an argument for creating artist then name, id, email id.

# 13-2-2025 agenda for tomorrow
# Part of publishing
# Tomorrow's class: Create version database - create .json file. When you start a publish project, need to create a version database.
# version name, version id, domain id, project id, artist id, date created, status, department
# Create a new folder in myStudio called 'publish' and there we will create multiple modules for publish database, one for handing maya, handling blender, handling different dccs

# Configure the database - xamm and use pip install such that 'python -m pip install mysql-connector-python'
# Migration of databases - migrate data from .json files to sql database using mySQL


