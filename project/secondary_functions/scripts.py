# project/secondary_functions/scripts.py
def query_students(query) -> list:
    lst = []
    dct = {}
    for i in query:
        dct["id"] = i.id
        dct["first_name"] = i.first_name
        dct["last_name"] = i.last_name
        dct['group_id'] = i.group_id
        lst.append(dct)
        dct = {}
    return lst


def query_groups(query) -> list:
    lst = []
    dct = {}
    for i in query:
        dct["id"] = i.id
        dct["name"] = i.name
        lst.append(dct)
        dct = {}
    return lst


def query_courses(query) -> list:
    lst = []
    dct = {}
    for i in query:
        dct["id"] = i.id
        dct["name"] = i.name
        dct["description"] = i.description
        lst.append(dct)
        dct = {}
    return lst
