import os
import optparse
import sys


def executeCode():
        
    parser = optparse.OptionParser(
    usage="usage: %prog\n\tInstaller to set up my studio pipeline",
    version="0.0.1",
    )


    parser.add_option("-o", "--opens", dest="dcc_open", action = "store", help="Sets which dcc to open", default="tester4.3")
    parser.add_option("-a", "--artist", dest="artist", action = "store", help="Sets name of artist", default="John Doe")
    parser.add_option("-p", "--project", dest="project", action = "store", help="Sets name of project", default="Project X")
    parser.add_option("-s", "--show", dest="show", action = "store", help="Sets name of show", default="Show ABC")
    
    options, args = parser.parse_args()

    print("Print options: ", options)
    print("Printing option.dcc_open here: ", options.dcc_open)
    print("Raw sys.argv:", sys.argv)

    

    if options.dcc_open:        
        print("Opening DCCs")
        dcc_path = "%SOFTWARE_PATH%" + "/" + options.dcc_open + ".bat"      
        print("Printing DCC PATH: ", dcc_path)
        os.system(dcc_path)
        
        
    else:
        print("by passed, tried with -e or --environment")
        


if __name__ == "__main__":
    executeCode()


# Debug options.open - done
# Create artist, create project, open show

