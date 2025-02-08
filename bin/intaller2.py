#!/bin/bash

import optparse

parser = optparse.OptionParser(
   usage="usage: %prog\n\tIntaller to set up my studio pipeline",
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
else:
    print("by passed, tried with -e or --environment")

 #!/bin/bash

import optparse

# python3 '/home/batman/Desktop/test/code_01.py'
# python3 '/home/batman/Desktop/test/code_01.py' -e

parser = optparse.OptionParser(
   usage="usage: %prog\n\tIntaller to set up my studio pipeline",
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
else:
    print("by passed, tried with -e or --environment")

   