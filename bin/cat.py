import os
import optparse
import sys
import json
import utils
import logging

import importlib
importlib.reload(utils)

# Setup logging
logging.basicConfig(level=logging.INFO)

# Define the JSON file for artist db
artists_json_file = os.path.expandvars("%DATABASE_PATH%/artists.json")


# Initialize the JSON database if it doesn't exist
if not os.path.exists(artists_json_file):
    with open(artists_json_file, "w") as file:
        json.dump([], file, indent=4)  # Empty list to store artist data

# Define the JSON file for project db
projects_json_file = os.path.expandvars("%DATABASE_PATH%/projects.json")


# Initialize the JSON database if it doesn't exist
if not os.path.exists(projects_json_file):
    with open(projects_json_file, "w") as file:
        json.dump([], file, indent=4)  # Empty list to store artist data

def executeCode():
        
    parser = optparse.OptionParser(
    usage="usage: %prog\n\tInstaller to set up my studio pipeline",
    version="0.0.1",
    )

    parser.add_option("-o", "--opens", dest="open", action = "store", help="Sets which dcc to open", default=None)
    parser.add_option("--create-artist", dest="create_artist", action = "store", help="Create name of artist", default=None)
    parser.add_option("--create-project", dest="create_project", action = "store", help="Create name of project", default=None)
    parser.add_option("--create-domain", dest="create_domain", action = "store", help="Create domain", default=None)  
    parser.add_option("--domain-cat", dest="domain_cat", action = "store", help="Create domain category", default=None) 
    # parser.add_option("--login", dest="login", action = "store", help="Sets login info of artist", default=None)  
       
    parser.add_option("--domain-cata", dest="domain_cata", action = "store", help="Sets name of artist", default=None)    

    parser.add_option("-a", "--artist", dest="artist", action = "store", help="Sets name of artist", default="John Doe")
    parser.add_option("-p", "--project", dest="project", action = "store", help="Sets name of project", default="Test_project")
    parser.add_option("-s", "--show", dest="show", action = "store", help="Sets name of show", default="Test_show")
    parser.add_option("-d", "--domain", dest="domain", action = "store", help="Sets domain name", default="Test_domain")


    
    options, args = parser.parse_args()
    print("Print options:\n", options)


    if options.open:        
        """
        Examples - done
        # cat --open maya2025 --project proj1
        # cat --open maya2025 --project proj1 --artist "Artist_name"
        # cat --open maya2025
        """      
           

        # check if project name exists in projects database
        project_found = False # Flag to track if project name is found

        # cat.py is only for config and commands. All other execution should happen on utils.py
        # Create class in utils.py

        # Load existing project database
        with open(projects_json_file, "r") as file:
            projects = json.load(file)

        # Check if the project already exists
        for project in projects:
            if project["name"].lower() == options.project.lower():  # Case-insensitive match
                project_found = True    # Set flag to True if a match is found 
                print(f"\nProject '{project["name"]}' already exists with ID {project['id']}")
                # Setup an environment variable for project
                os.environ["PROJECT_NAME"] = project["name"]
                print("\nProject env set to: ", os.environ["PROJECT_NAME"])
                break  # Exit loop after the first match                
        if not project_found:
            print(f"\nProject does not exist in database. Please add project in database using create-project flag")
            exit
        
        # check if artist name exists in artists database
        artist_found = False # Flag to track if artist name is found

        # Load existing artist database
        with open(artists_json_file, "r") as file:
            artists = json.load(file)

        # Check if the artist already exists
        for artist in artists:
            if artist["name"].lower() == options.artist.lower():  # Case-insensitive match
                artist_found = True    # Set flag to True if a match is found 
                print(f"\nArtist '{artist["name"]}' already exists with ID {artist['id']}, Email: {artist['email']}")
                # Setup an environment variable for artist
                # Create environment varibles which will store this user info
                os.environ["ARTIST_ID"] = str(artist["id"])
                os.environ["ARTIST_NAME"] = artist["name"]
                os.environ["ARTIST_EMAIL"] = artist["email"]
                logging.info(f"\nArtist env set to\nName: {os.environ["ARTIST_NAME"]}, ID: {os.environ["ARTIST_ID"]}, email: {os.environ["ARTIST_EMAIL"]}\n")
                break   # Exit loop after the first match 
                
        if not artist_found:
            print(f"\nArtist does not exist in database. Please add artist in database using create-artist flag")
            exit
        
        # Now the program triggers opening of project after project & artist env is set            

        if artist_found and project_found:      # Trigger open only if artist name & project name match in db          
            print("Triggering opening function now\n")
            utils.triggerOpen(options.open) #, project=options.project, artist=options.artist)
        
        # print("Opening DCCs")
        # dcc_path = "%SOFTWARE_PATH%" + "/" + options.open + ".bat"      
        # print("Printing DCC PATH: ", dcc_path)
        # os.system(dcc_path)  


        
    if options.create_artist:
        """
        Exapmples
        # cat --create-artist "Artist Name"
        """

        # os.environ["USER_EMAIL"] = "johndoe@example.com"
        # Update such that the user info is stored as environment variables.         

        returned_artist_info = name_to_database(options.create_artist)   


        logging.info(f"\nArtist info in database\nName: {returned_artist_info["name"]}, ID: {str(returned_artist_info["id"])}, email: {returned_artist_info["email"]}\n")



    if options.create_project:
        """
        Exapmples
        # cat --create-project "Project Name"
        """

        # Think about revising code regularly. Code is not final, always. Feel free to refactor constantly. 
        # Refactor: enhance your code.        

        returned_project_info = save_project(options.create_project)   

        logging.info(f"\nProject info in database\nName:: {returned_project_info["name"]}, PROJECT ID: {str(returned_project_info["id"])}")
        
        

    if options.create_domain:
        """
        Exapmples
        # cat --create-domain "bat" --domain-cat <"asset"> --project_id <project id>
        # cat --create-domain "shot1" --domain-cat <"shot"> --project_id <project id>
        """

        utils.createDomain(options.create_domain, options.domain_cat)
        # cata --create-domain ball --domain_cata asset
        pass
 

def save_project(project_name, start_id=201):
    # Load existing project database
    with open(projects_json_file, "r") as file:
        projects = json.load(file)

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

    # Save updated project database
    with open(projects_json_file, "w") as file:
        json.dump(projects, file, indent=4)

    print(f"\nAdded new project: {new_project}")
    return new_project



def name_to_database(full_name, domain="example.com", start_id=101):
    # Load existing artist database
    with open(artists_json_file, "r") as file:
        data = json.load(file)

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
    for artist in data:
        if artist["email"] == email:
            print(f"Email {email} already exists with ID {artist['id']}")
            return artist  # Return existing artist entry

    # Assign new ID (increment from highest existing ID)
    if data:
        max_id = max(artist["id"] for artist in data)
    else:
        max_id = start_id - 1  # Start from 101 if empty

    new_id = max_id + 1

    # Create new artist record
    new_artist = {
        "id": new_id,
        "name": full_name,
        "email": email
    }
    data.append(new_artist)

    # Save updated database
    with open(artists_json_file, "w") as file:
        json.dump(data, file, indent=4)

    print(f"Added new artist: {new_artist}\n")
    return new_artist

    # In cat command, if you write 'set project' it should set this project as the environment variable. - done
    # Example:  cat --opens maya2025 --project "PROJECT_ABC" --domains <name> which will have attributes like "type/category/status" which can be queried when asked.
    
    # This way, it will launch maya under PROJECT_ABC" - done
    # Before launching dcc, launch it with valid user, set the project and then launch Maya.
    # Setup project path as well by setting up PROJECT_PATH env variable in installer.py - done

    # New command to create domains
    # cat --domains <type/name/category/status>
    # Then, projects can be broken down into different domains/departments like FX, Assets, etc
    # Create one more DB for CREATE_DOMAIN which create domain type, domain category and domain name.
    # Example, ball, bat, etc is Asset type, and name is 'ball', 'bat' etc category is 'modeling', 'rigging' etc
    # Domains are necessary during publishing stage.

          

    
    # json_file = os.path.expandvars("%DATABASE_PATH%/artists.json")    # "E:/pipelineDevelopment/database/artists.json"

if __name__ == "__main__":
    executeCode()


# Debug options.open - done
# Create artist, create project, open show