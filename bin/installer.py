# This is to setup the studio environment

#!/bin/bash

import logging
import optparse

logging.basicConfig(level=logging.INFO)

def execute():

    # python3 '/home/batman/Desktop/test/code_01.py'
    # python3 '/home/batman/Desktop/test/code_01.py' -e
    # python3 '/home/batman/Desktop/test/code_01.py' --open "belnder4.3.1"

    parser = optparse.OptionParser(
       usage="usage: %prog\n\tIntaller to set up my studio pipeline",
       version="0.0.1",
    )

    parser.add_option(
        "-e", "--environment",
        action = "store_true", 
        dest = "environment",
        default = False,
        help = "Set up the pipeline command and primary environments"
    )
    
    parser.add_option(     
        "-o", "--open",
        dest="open",
        action="store",
        help="To lauch(Open) DCC (Digital Command Control).",     
    )
     
    options, args = parser.parse_args()
 
    print(options, args)
    print("\n")
    
    if options.environment:
        print("\tenvironment", options.environment)
        logging.info("\tStart to setp my studio envs")
    
    if options.open:
        print("\tCurrent software", options.open)


if __name__ == "__main__":    
   execute()

