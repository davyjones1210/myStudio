import os
import json

DOMAIN_CAT = ["asset", "shot"]

ASSET_CAT = [["asset", ["modeling", "rigging"]], ["shot", ["layout", "animation"]]]

# Define the JSON file for domain db
domains_json_file = os.path.expandvars("%DATABASE_PATH%/domain.json")


# Initialize the JSON database if it doesn't exist
if not os.path.exists(domains_json_file):
    with open(domains_json_file, "w") as file:
        json.dump([], file, indent=4)  # Empty list to store artist data


def triggerOpen(name):
    filepath = os.path.expandvars("%CONFIG_PATH%/dcc.json")
    data = readJoson(filepath)
    # print("Data variable: ", data)
    print("Options.open value passed: ", name)
    collectDCC(name, data)

def createDomain(domain_name, domain_cat, start_id=301):
    
    # Load existing domain database
    with open(domains_json_file, "r") as file:
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
    with open(domains_json_file, "w") as file:
        json.dump(domains, file, indent=4)

    print(f"\nAdded new domain: {new_domain}")
    return new_domain

# From this data variable, figure out the specific block from the list, if blender collect blender data, if maya, collect maya
# From the config find out what DCC was typed in cat --opens "here"



def readJoson(filepath):
    with open(filepath, 'r') as openfile:
        return json.load(openfile)
    

def collectDCC(name, data):
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
            os.system(dcc_path)
            break  # Exit loop after the first match
    if not found:  # If no match was found after looping
        print("DCC name not matching")
            

# os.environ["BLENDER_PLUG_IN_PATH"] = "E:/pipelineDevelopment/test1;E:/pipelineDevelopment/test2",        
# os.environ["BLENDER_SCRIPT_PATH"] = "E:/pipelineDevelopment/test3;E:/pipelineDevelopment/test4",  
# 
# and then launch blender using the path key in json file. And also create a new block for Nuke.
# 
# One more task: Go to cat.py, create a artist by creating a database folder and treat json like a database (table, rows & column). Store artist info like # name, id, email, etc. If an artist database file doesn't exist create it and then edit it going forward.
# In installer.py add another env variable called DATABASE_PATH

# Next, create an argument for creating artist then name, id, email id.
