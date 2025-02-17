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
            

    def commandParser(self):
        #Initialize optparser to parse command line prompt
        parser = optparse.OptionParser(usage="usage: %prog\n\tInstaller to set up my studio pipeline", version="0.0.1")
    
        # Defining command line arguments using add_option method of optparse
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

        return parser.parse_args()
    
   
    def executeCode(self):

        # cat.py is only for config and commands. All other execution should happen on utils.py
            # Create class in utils.py     

        # Parse command line arguments
        options, args = self.commandParser()
        print("Print options:\n", options)

        # Initialize utils_command
        utils_command = utils.UtilsCommand()

        # Executing code after command line arguments are parsed
        if options.open:        
            """
            Examples - done
            # cat --opens maya2025 --project proj1 (done)
            # cat --opens maya2025 --project "proj1" --artist "Artist_name" (done)
            """
            utils_command.runOpenCommand(options)      
            
        if options.create_artist:
            """
            Exapmples
            # cat --create-artist "Artist Name" (done)
            """
            utils_command.runCreateArtistCommand(options)

        if options.create_project:
            """
            Exapmples
            # cat --create-project "Project Name" (done)
            """          
            utils_command.runcreateProjectCommand(options)
                    

        if options.create_domain:
            """
            Exapmples
            # cat --create-domain "bat" --domain-cat <"asset"> --project_id <project id>
            # cat --create-domain "shot1" --domain-cat <"shot"> --project_id <project id>
            """
            utils_command.runCreateDomainCommand(options)

    
    
if __name__ == "__main__":
    cat_command = CatCommand()
    cat_command.executeCode()


    # Notes:
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

    # Think about revising code regularly. Code is not final, always. Feel free to refactor constantly. 
        # Refactor: enhance your code.
