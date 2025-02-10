import os
import optparse


def executeCode():
        
    parser = optparse.OptionParser(
    usage="usage: %prog\n\tInstaller to set up my studio pipeline",
    version="0.0.1",
    )


    parser.add_option(
        "-e", "--environment",
        action = "store_true", 
        dest = "environments",
        default = False,
        help = "Set up the pipeline command and primary environments"
    )
    
    options, args = parser.parse_args()

    if options.environments:
        print("Start to setp my studio envs")
        # set PATH env
        path_name = "E:/pipelineDevelopment/myStudio/bin"
        os.environ["PATH"] = os.environ["PATH"] + ";" + path_name
        print(os.environ["PATH"])

        # set software PATH env
        sw_path_name = "E:/pipelineDevelopment/software"
        os.environ["SOFTWARE_PATH"] = sw_path_name
        print(os.environ["SOFTWARE_PATH"])

        # set pylib PATH env
        pylib_path_name = "E:/pipelineDevelopment/pylib"
        mystudio_path = "E:/pipelineDevelopment/myStudio"
        os.environ["PYTHONPATH"] = pylib_path_name + ";" + mystudio_path
        print(os.environ["PYTHONPATH"])

        os.system("cmd")
        
        
    else:
        print("by passed, tried with -e or --environment")


if __name__ == "__main__":
    executeCode()
