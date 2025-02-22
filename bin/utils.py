import os
import json
import logging


# Setup logging
logging.basicConfig(level=logging.INFO)

DOMAIN_CAT = ["asset", "shot"]

ASSET_CAT = [["asset", ["modeling", "rigging"]], ["shot", ["layout", "animation"]]]
# Define the JSON file for DCC data
dcc_data_filepath = os.path.expandvars("%CONFIG_PATH%/dcc.json")
# Define the JSON file for artist db
artists_json_file = os.path.expandvars("%DATABASE_PATH%/artists.json")
# Define the JSON file for project db
projects_json_file = os.path.expandvars("%DATABASE_PATH%/projects.json")
# Define the JSON file for domain db
domains_json_file = os.path.expandvars("%DATABASE_PATH%/domains.json")
    
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
                print("\nProject '{}' already exists with ID {}".format(
        project["name"], project['id']
    )
)
                # Setup an environment variable for project
                os.environ["PROJECT_NAME"] = project["name"]
                print("\nProject env set to: ", os.environ["PROJECT_NAME"])
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
                    

def name_to_database(full_name, domain="example.com", start_id=101):

    artists = readJson(artists_json_file)

    # Remove quotes and split the name into parts
    name_parts = full_name.replace('"', '').split()

    # Ensure at least first and last name are present
    if len(name_parts) < 2:
        raise ValueError("Invalid name format. Must have at least a first and last name.")

    # Extract first name, middle initial (if present), and last name
    first_name = name_parts[0].lower()
    middle_initial = name_parts[1].lower() if len(name_parts) == 3 else ""
    last_name = name_parts[-1].lower()

    # Generate the email address
    email = f"{first_name}{middle_initial}{last_name}@{domain}" if middle_initial else f"{first_name}{last_name}@{domain}"

    # Check if email already exists in database
    for artist in artists:
        if artist["email"] == email:
            print(f"Email {email} already exists with ID {artist['id']}")
            return artist  # Return existing artist entry

    # Assign new ID (increment from highest existing ID)
    if artists:
        max_id = max(artist["id"] for artist in artists)
    else:
        max_id = start_id - 1  # Start from 101 if empty

    new_id = max_id + 1

    # Create new artist record
    new_artist = {
        "id": new_id,
        "name": full_name,
        "email": email
    }
    artists.append(new_artist)

    writeJson(artists_json_file, artists)
    print(f"Added new artist: {new_artist}\n")
    return new_artist


def save_project(project_name, start_id=201):
    
    projects = readJson(projects_json_file)        

    # Check if the project already exists
    for project in projects:
        if project["name"].lower() == project_name.lower():  # Case-insensitive match
            print(f"\nProject '{project_name}' already exists with ID {project['id']}")
            return project  # Return existing project entry

    # Assign new ID (increment from highest existing ID)
    if projects:
        max_id = max(project["id"] for project in projects)
    else:
        max_id = start_id - 1  # Start from 201 if empty

    new_id = max_id + 1

    # Create new project record
    new_project = {
        "id": new_id,
        "name": project_name
    }
    projects.append(new_project)
    writeJson(projects_json_file, projects)        

    print(f"\nAdded new project: {new_project}")
    return new_project

def createDomain(domain_name, domain_cat, start_id=301):
    # This function creates a new domain in the database       

    # Read existing domain database
    domains = readJson(domains_json_file)        

    # Check if the domain already exists
    for domain in domains:
        if domain["name"].lower() == domain_name.lower():  # Case-insensitive match
            print(f"\nDomain '{domain_name}' already exists with category {domain['category']}")
            return domain  # Return existing project entry            
    
    # Assign new domain ID (increment from highest existing ID)
    if domains:
        max_id = max(domain["id"] for domain in domains)
    else:
        max_id = start_id - 1  # Start from 201 if empty

    new_id = max_id + 1
    logging.info(f"\nChecked domain ID: {new_id}")

    # Create new domain record
    new_domain = {
        "id": new_id,
        "name": domain_name,
        "category": domain_cat
    }
    logging.info(f"\nNew domain info: {new_domain}")
    domains.append(new_domain)

    writeJson(domains_json_file, domains)    

    print(f"\nAdded new domain: {new_domain}")
    return new_domain

# From this data variable, figure out the specific block from the list, if blender collect blender data, if maya, collect maya
# From the config find out what DCC was typed in cat --opens "here"

def runOpenCommand(options):
    #Checking if artists' name exists in database
    artist_validated = checkIfArtistExists(options.artist)
    #Checking if project name exists in database
    project_validated = checkIfProjectExists(options.project)
                
    if artist_validated and project_validated:      # Trigger open only if artist name & project name match in db          
        print("Triggering opening function now\n")                
        triggerOpen(options.open)  

def runCreateArtistCommand(options):
    returned_artist_info = name_to_database(options.create_artist)   
    logging.info("\nArtist info in database\nName: {}, ID: {}, Artist ID: {}".format(
        returned_artist_info["name"], str(returned_artist_info["id"]), str(returned_artist_info["id"])
            )
        )
def runcreateProjectCommand(options):
    returned_project_info = save_project(options.create_project) 
    logging.info("\nProject info in database\nName:: {}, Project ID: {}".format(
        returned_project_info["name"], str(returned_project_info["id"])
    )
)
def runCreateDomainCommand(options):
    returned_domain_info = createDomain(options.create_domain, options.domain_cat)
    logging.info("\nDomain info in database\nName:: {}, Domain ID: {}".format(
        returned_domain_info["name"], str(returned_domain_info["id"])
    )
)
    # cata --create-domain "ball" --domain_cata "asset"

if __name__ == "__main__":    

    initialize_json_file(artists_json_file)
    initialize_json_file(projects_json_file)
    initialize_json_file(domains_json_file)
            
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


