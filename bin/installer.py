# This is to setup the studio environment

# import optparse
# print(help(optparse))

# import OptionParser class 
# from optparse module.
from optparse import OptionParser

# create a OptionParser
# class object
parser = OptionParser()

# add options
parser.add_option("-e", "--environment",
				dest = "environment",
				help = "to set environment to our studio", 
				metavar = "FILE")

(options, args) = parser.parse_args()

print(options, args)


