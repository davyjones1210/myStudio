from publish import database

def project(inputs):
    print("\nssssssssssssssssssssssss")
    from pprint import pprint
    pprint(inputs)
    print("\n------------------------------")
    print(inputs)

    db = database.myDatabase()
    db.connect()
    result = db.insert("project", values)    