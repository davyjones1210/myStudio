import os
import optparse
import sys
import json
import utils
import logging

import importlib
importlib.reload(utils)

class CatCommand():
    
    def __init__(self):        
        # Setup logging
        logging.basicConfig(level=logging.INFO)

        # Define the JSON file for artist db
        self.artists_json_file = os.path.expandvars("%DATABASE_PATH%/artists.json")


        # Initialize the JSON database if it doesn't exist
        if not os.path.exists(self.artists_json_file):
            with open(self.artists_json_file, "w") as file:
                json.dump([], file, indent=4)  # Empty list to store artist data

        # Define the JSON file for project db
        self.projects_json_file = os.path.expandvars("%DATABASE_PATH%/projects.json")


        # Initialize the JSON database if it doesn't exist
        if not os.path.exists(self.projects_json_file):
            with open(self.projects_json_file, "w") as file:
                json.dump([], file, indent=4)  # Empty list to store artist data

        


    def executeCode(self):
        #Initialize optparser to parse command line prompt
        parser = optparse.OptionParser(
        usage="usage: %prog\n\tInstaller to set up my studio pipeline",
        version="0.0.1",
        )
        # Parsing command line arguments using add_option method of optparse
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

        # Initialize utils_command
        utils_command = utils.UtilsCommand(self.artists_json_file, self.projects_json_file)

        # Executing code after command line arguments are parsed
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
            with open(self.projects_json_file, "r") as file:
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
            with open(self.artists_json_file, "r") as file:
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
                utils_command.triggerOpen(options.open) #, project=options.project, artist=options.artist)
            
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
            #utils_command = utils.UtilsCommand(self.artists_json_file, self.projects_json_file)
            returned_artist_info = utils_command.name_to_database(options.create_artist)   

            logging.info(f"\nArtist info in database\nName: {returned_artist_info["name"]}, ID: {str(returned_artist_info["id"])}, email: {returned_artist_info["email"]}\n")



        if options.create_project:
            """
            Exapmples
            # cat --create-project "Project Name"
            """

            # Think about revising code regularly. Code is not final, always. Feel free to refactor constantly. 
            # Refactor: enhance your code.        
            
            returned_project_info = utils_command.save_project(options.create_project)   

            logging.info(f"\nProject info in database\nName:: {returned_project_info["name"]}, PROJECT ID: {str(returned_project_info["id"])}")
            
            

        if options.create_domain:
            """
            Exapmples
            # cat --create-domain "bat" --domain-cat <"asset"> --project_id <project id>
            # cat --create-domain "shot1" --domain-cat <"shot"> --project_id <project id>
            """

            utils_command.createDomain(options.create_domain, options.domain_cat)
            # cata --create-domain "ball" --domain_cata "asset"
    

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
    cat_command = CatCommand()
    # utils_command = utils.UtilsCommand(self.artists_json_file, self.projects_json_file)
    cat_command.executeCode()


# Debug options.open - done
# Create artist, create project, open show