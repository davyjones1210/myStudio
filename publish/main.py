import logging

from publish import main

def moviePublish(category, name, department):

    result, output = main.movie(category, name, department)

    print("\n", result, output)

    if result:
        main.register_version(category, name, department)

    else:
        logging.error("Your publish failed: %s" % output)


