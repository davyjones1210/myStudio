import os
import optparse


def executeCode():
        
    parser = optparse.OptionParser(
    usage="usage: %prog\n\tInstaller to set up my studio pipeline",
    version="0.0.1",
    )


    parser.add_option("-o", "--opens", dest="open", action = "store", help="Sets which dcc to open", default="blender4.3")
    
    options, args = parser.parse_args()

    print("Print options: ", options)
    print("Printing option.open here: ", options.open)
    

    if options.open:        
        print("Opening DCCs")
        dcc_path = "%SOFTWARE_PATH%" + "/" + options.open + ".bat"      
        print("Printing DCC PATH: ", dcc_path)
        os.system(dcc_path)
        
        
    else:
        print("by passed, tried with -e or --environment")
        


if __name__ == "__main__":
    executeCode()


# Debug options.open
# Create artist, create project, open show

