

def  search(category, name, department, typed):
    """
    Use this fucntion to search for versions in the specific context passed as argument. Just search for it
    """
    pass
    

def sourceFile(category, name, department, typed, version=None, approved=True):
    """
        latest approved or latest or specific version can be able to load in downstrem deparatment  to begin their work

        result = main.sourceFile("asset", "monkey", "modeling")
        or
        result = main.sourceFile("asset", "monkey", "modeling", version=v5)
        or 
        result = main.sourceFile("asset", "monkey", "modeling", version="latest", approved=True)
        or
        result = main.sourceFile("asset", "monkey", "modeling", version="latest", approved=False)   

        Find the proper version and generate the path.  
    """
    pass

    # 1. Search for all versions in the specified context.
    # Figure out steps as exercise.
    # Final outcome: Have that input file to be imported and opened in blender where artists can start the work on the file.
