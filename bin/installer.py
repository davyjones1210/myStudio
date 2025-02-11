# importing os module to interact with operating system to set environment variables
import os

# from optparse module, importing OptionParser class
from optparse import OptionParser


def setup_studio_env(studio_name, environments):
    # Creating a separate function to set and print environment variables
    os.environ["STUDIO_NAME"] = studio_name
    os.environ["ENV_FLAG"] = str(environments)

    
    print("Studio Environment Variables Set:")
    print(f"STUDIO_NAME: {os.environ['STUDIO_NAME']}")
    print(f"ENV_FLAG: {os.environ['ENV_FLAG']}")




# Entry-point to the program. Code execution starts from here
if __name__ == "__main__":
    # First creating an object of class OptionParser which we imported above
    parser = OptionParser()

    # Using add_option to define various command line flags 
    parser.add_option("-s", "--studio", dest="studio_name", help="Set the studio name", default="KD_Studio")
    parser.add_option("-e", "--environment", action = "store_true", dest = "environments", default = False, help = "Set up the pipeline command and primary environments")



    # Reads command-line arguments and Splits them into recognized options and positional arguments.
    (options, args) = parser.parse_args()

    # Calls the above defined function and passes the various recognized options as arguments
    setup_studio_env(options.studio_name, options.environments)

    if options.environments:
        # set PATH env   
        print("Printing OS ENVIRON PATH")
        path_name = "E:/pipelineDevelopment/sourcecodes/myStudio/bin"
        os.environ["PATH"] = os.environ["PATH"] + ";" + path_name
        os.environ["MY_BIN"] = path_name
        # print(os.environ["PATH"])

        # set software PATH env
        sw_path_name = "E:/pipelineDevelopment/software"
        os.environ["SOFTWARE_PATH"] = sw_path_name
        # print(os.environ["SOFTWARE_PATH"])

        # set pylib PATH env
        pylib_path_name = "E:/pipelineDevelopment/pylib"
        mystudio_path = "E:/pipelineDevelopment/sourcecodes/myStudio"
        os.environ["PYTHONPATH"] = pylib_path_name + ";" + mystudio_path
        # print(os.environ["PYTHONPATH"])

        # set config path
        config_path_name = "E:/pipelineDevelopment/config"        
        os.environ["CONFIG_PATH"] = config_path_name
        print(os.environ["CONFIG_PATH"])
                
        os.system("cmd")
    else:
        print("by passed, try with -e or --environment")
    

# Command line prompt for demonstration
# python3 optparse_Exercise.py --studio Framestore --nuke 13.2v4 --maya 2022 --artist 'Kunal Dekhane'