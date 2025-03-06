'''
Mock Studio Pipeline Development with Subin Gopi - v0.1
Date: Feb 14, 2025
Author: Kunal Dekhane
kunal.dekhane@gmail.com
No Copyright 2025 Kunal Dekhane - No Rights Reserved, feel free to copy and distribute

# WARNING! All changes made in this file will be lost!
'''

# importing os module to interact with operating system to set environment variables
import os

# from optparse module, importing OptionParser class
from optparse import OptionParser

import utils

PIPELINE_DIRECTORY = "C:/works/pipeline"
PROJECTS_DIRECTORY = "C:/works/projects"    

def setup_studio_env(studio_name, environments):
    # Creating a separate function to set and print environment variables
    os.environ["STUDIO_NAME"] = studio_name
    os.environ["ENV_FLAG"] = str(environments)

    
    print("Studio Environment Variables Set:")
    print(f"STUDIO_NAME: {os.environ['STUDIO_NAME']}")


def execute():
    # First creating an object of class OptionParser which we imported above

    parser = OptionParser()

    # Using add_option to define various command line flags 
    parser.add_option("-s", "--studio", dest="studio_name", help="Set the studio name", default="KD_Studio")
    parser.add_option("-e", "--environment", action = "store_true", dest = "environments", default = False, help = "Set up the pipeline command and primary environments")

    # Reads command-line arguments and Splits them into recognized options and positional arguments.
    (options, args) = parser.parse_args()

    # Calls the above defined function and passes the various recognized options as arguments

    # Call the setup_studio_env method
    # setup_studio_env(options.studio_name, options.environments)
    utils.set_environments("STUDIO_NAME", options.studio_name)
    utils.set_environments("ENV_FLAG", str(options.environments))

    print("Studio Environment Variables Set:")
    print(f"STUDIO_NAME: {os.environ['STUDIO_NAME']}")
    print(f"ENV_FLAG: {os.environ['ENV_FLAG']}")

    if options.environments:
        # set PATH env    
        path_name = os.path.join(PIPELINE_DIRECTORY, "sourcecodes/myStudio/bin")
        os.environ["PATH"] = "%s;%s" % (os.environ["PATH"], path_name)
        os.environ["MY_BIN"] = path_name
        # print(os.environ["PATH"])

        # Add FFMPEG path to the PATH environment variable
        ffmpeg_path = "C:\\ffmpeg\\ffmpeg-7.1-essentials_build\\bin"
        os.environ["PATH"] = "%s;%s" % (os.environ["PATH"], ffmpeg_path)

        # Print the updated PATH for verification
        print("Updated PATH: {}".format(os.environ["PATH"]))

        mystudio_path = os.path.join(PIPELINE_DIRECTORY, "sourcecodes/myStudio")
        os.environ["SOURCE_CODE_PATH"] = mystudio_path

        # set software PATH env
        sw_path_name = os.path.join(PIPELINE_DIRECTORY, "software")
        os.environ["SOFTWARE_PATH"] = sw_path_name
        # print(os.environ["SOFTWARE_PATH"])

        # set pylib PATH env
        pylib_path_name = os.path.join(PIPELINE_DIRECTORY, "pylib")
        os.environ["PYTHONPATH"] = pylib_path_name + ";" + mystudio_path + ";" 
        # print(os.environ["PYTHONPATH"])

        # set config path
        config_path_name = os.path.join(PIPELINE_DIRECTORY, "config")      
        os.environ["CONFIG_PATH"] = config_path_name
        # print(os.environ["CONFIG_PATH"])

        # set database path
        db_path_name =  os.path.join(PIPELINE_DIRECTORY, "database")
        print("\ndb_path_name", db_path_name) 
        os.environ["DATABASE_PATH"] = db_path_name
        print("Database path: ", os.environ["DATABASE_PATH"])

        # set project path
        project_path_name = PROJECTS_DIRECTORY    
        os.environ["PROJECT_PATH"] = project_path_name
        print("Project path: ", os.environ["PROJECT_PATH"])
                
        os.system("cmd")
    else:
        print("by passed, try with -e or --environment")


    # Command line prompt for demonstration
    # python3 optparse_Exercise.py --studio Framestore --nuke 13.2v4 --maya 2022 --artist 'Kunal Dekhane'    

# Entry-point to the program. Code execution starts from here
if __name__ == "__main__":
    execute()