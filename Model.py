__author__ = 'zhizheng'



def get_temp_view(db,map_fun, reduce_fun='', start_key=-1, end_key=-1):
    if(start_key == -1 and end_key == -1):
        view = db.query(map_fun,reduce_fun)
    elif(start_key != -1 and end_key == -1):
        view = db.query(map_fun,start_key=start_key)
    elif(start_key==-1 and end_key !=-1):
        view = db.query(map_fun,end_key=end_key)
    return view


def get_view(db,view_name, map_fun, reduce_fun='', start_key=-1,end_key=-1):
    if(start_key == -1 and end_key == -1):
        view = db.view(view_name)
    elif(start_key!=-1):
        view = db.view(view_name,start_key = start_key)
    else:
        view = db.view(view_name,end_key=end_key)
    return view


def setup_couchdb(Url):
    db_name = 'toronto'
    couch = couchdb.Server()
    # couch.resource.credentials = (db_user, db_pass)
    try:
        test = couch[db_name]
        return test
    except couchdb.ResourceNotFound:
        return couch.create(db_name)


import couchdb
from couchdb import Server, Session
