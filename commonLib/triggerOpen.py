import os
import json
import logging


# Define the JSON file for DCC data
dcc_data_filepath = os.path.expandvars("%CONFIG_PATH%/dcc.json")

def readJson(filepath):
    # Reads the json filepath passed and returns the data
    with open(filepath, 'r') as openfile:
        return json.load(openfile) 

def triggerOpen(name):
    # This function opens the DCC software based on the name passed
    
    dcc_data = readJson(dcc_data_filepath)
    # print("Data variable: ", data)
    print("Options.open value passed: ", name)
    collectDCC(name, dcc_data)    


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

    os.system(dcc_path)

    if not found:  # If no match was found after looping
        print("DCC name not matching")