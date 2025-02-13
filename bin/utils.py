import os
import json

DOMAIN_CAT = ["asset", "shot"]

ASSET_CAT = [["asset", ["modeling", "rigging"]], ["shot", ["layout", "animation"]]]


def triggerOpen(name):
    filepath = os.path.expandvars("%CONFIG_PATH%/dcc.json")
    data = readJoson(filepath)
    # print("Data variable: ", data)
    print("Options.open value passed: ", name)
    collectDCC(name, data)



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
