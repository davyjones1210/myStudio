import os
import optparse
import sys
import json

import utils

import importlib
importlib.reload(utils)

# Define the JSON file for artist db
json_file = os.path.expandvars("%DATABASE_PATH%/artists.json")
print("JSON FILE FOR DB: ", json_file)

def executeCode():
        
    parser = optparse.OptionParser(
    usage="usage: %prog\n\tInstaller to set up my studio pipeline",
    version="0.0.1",
    )


    parser.add_option("-o", "--opens", dest="open", action = "store", help="Sets which dcc to open", default=None)
    parser.add_option("-a", "--artist", dest="artist", action = "store", help="Sets name of artist", default="John Doe")
    parser.add_option("-p", "--project", dest="project", action = "store", help="Sets name of project", default="Project X")
    parser.add_option("-s", "--show", dest="show", action = "store", help="Sets name of show", default="Show ABC")
    
    options, args = parser.parse_args()

    print("Print options: ", options)
    print("Printing option.open here: ", options.open)
    print("Raw sys.argv:", sys.argv)

    

    if options.open:
        print("Triggering opening function now\n")
        utils.triggerOpen(options.open)
        
        # print("Opening DCCs")
        # dcc_path = "%SOFTWARE_PATH%" + "/" + options.open + ".bat"      
        # print("Printing DCC PATH: ", dcc_path)
        # os.system(dcc_path)       

    
    # json_file = os.path.expandvars("%DATABASE_PATH%/artists.json")    # "E:/pipelineDevelopment/database/artists.json"

    # Initialize the JSON database if it doesn't exist
    if not os.path.exists(json_file):
        with open(json_file, "w") as file:
            json.dump([], file, indent=4)  # Empty list to store artist data
    
    # Example Usage
    add_artist("John D Doe", 101, "johndoe@example.com")
    add_artist("Jane S Smith", 102, "janesmith@example.com")

    # Example Usage
    artist = get_artist(101)
    if artist:
        print("Artist Found:", artist)
    else:
        print("Artist not found!")


def add_artist(name, user_id, email):
    # json_file = os.path.expandvars("%DATABASE_PATH%/artists.json")
    # Load existing data
    with open(json_file, "r") as file:
        data = json.load(file)

    # Check if user ID already exists
    for artist in data:
        if artist["user_id"] == user_id:
            print(f"Artist with user ID {user_id} already exists!")
            return
    
    # Add new artist
    new_artist = {
        "name": name,
        "user_id": user_id,
        "email": email
    }
    data.append(new_artist)

    # Save updated data
    with open(json_file, "w") as file:
        json.dump(data, file, indent=4)

    print(f"Artist {name} added successfully!")


def get_artist(user_id):
    # json_file = os.path.expandvars("%DATABASE_PATH%/artists.json")
    with open(json_file, "r") as file:
        data = json.load(file)
    
    for artist in data:
        if artist["user_id"] == user_id:
            return artist
    
    return None





if __name__ == "__main__":
    executeCode()


# Debug options.open - done
# Create artist, create project, open show