import os
import optparse
import sys

import utils

import importlib
importlib.reload(utils)

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
        utils.triggerOpen(options.open)
        
        # print("Opening DCCs")
        # dcc_path = "%SOFTWARE_PATH%" + "/" + options.open + ".bat"      
        # print("Printing DCC PATH: ", dcc_path)
        # os.system(dcc_path)       


if __name__ == "__main__":
    executeCode()


# Debug options.open - done
# Create artist, create project, open show