import os
import json

class UtilsCommand():

    def __init__(self, artists_json_file, projects_json_file):

        self.DOMAIN_CAT = ["asset", "shot"]

        self.ASSET_CAT = [["asset", ["modeling", "rigging"]], ["shot", ["layout", "animation"]]]

        self.artists_json_file = artists_json_file

        self.projects_json_file = projects_json_file

        # Define the JSON file for domain db
        self.domains_json_file = os.path.expandvars("%DATABASE_PATH%/domain.json")


        # Initialize the JSON database if it doesn't exist
        if not os.path.exists(self.domains_json_file):
            with open(self.domains_json_file, "w") as file:
                json.dump([], file, indent=4)  # Empty list to store artist data


    def triggerOpen(self, name):
        filepath = os.path.expandvars("%CONFIG_PATH%/dcc.json")
        data = self.readJoson(filepath)
        # print("Data variable: ", data)
        print("Options.open value passed: ", name)
        self.collectDCC(name, data)

    def createDomain(self, domain_name, domain_cat, start_id=301):
        
        # Load existing domain database
        with open(self.domains_json_file, "r") as file:
            domains = json.load(file)

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

        # Create new domain record
        new_domain = {
            "id": new_id,
            "name": domain_name,
            "category": domain_cat
        }
        domains.append(new_domain)

        # Save updated domain database
        with open(self.domains_json_file, "w") as file:
            json.dump(domains, file, indent=4)

        print(f"\nAdded new domain: {new_domain}")
        return new_domain

    # From this data variable, figure out the specific block from the list, if blender collect blender data, if maya, collect maya
    # From the config find out what DCC was typed in cat --opens "here"



    def readJoson(self, filepath):
        with open(filepath, 'r') as openfile:
            return json.load(openfile)
        

    def collectDCC(self, name, data):
        found = False  # Flag to track if DCC name is found
        # Extract and print 'envs' values
        for software in data:        
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


    def name_to_database(self, full_name, domain="example.com", start_id=101):
        # Load existing artist database
        with open(self.artists_json_file, "r") as file:
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
        with open(self.artists_json_file, "w") as file:
            json.dump(data, file, indent=4)

        print(f"Added new artist: {new_artist}\n")
        return new_artist
    

    def save_project(self, project_name, start_id=201):
        # Load existing project database
        with open(self.projects_json_file, "r") as file:
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
        with open(self.projects_json_file, "w") as file:
            json.dump(projects, file, indent=4)

        print(f"\nAdded new project: {new_project}")
        return new_project

                
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


