from flask import Flask
from flask.ext import restful
from flask import render_template
import urllib
import requests
import Model
import couchdb
import json

app = Flask(__name__)
api = restful.Api(app)

db = Model.setup_couchdb('')

class Documents(restful.Resource):
    def get(self):
        num_of_scenario = 3
        map_fun = '''function(doc) {
            if(doc.id)
            emit(doc.id, doc);
            }'''
        rows = Model.get_temp_view(db,map_fun).rows
        return json.dumps(rows)


class DateDocuments(restful.Resource):
    def get(self):
        map_fun = '''function(doc) {
            var dt = new Date(Date.parse(doc.created_at))
            emit([dt.getDate(),dt.getHours()], 1);
            }'''
        reduce_fun = '''
            function(key,values,rereduce) {
            if(rereduce)
            {
            return sum(values)
            }
            else
            {
            return values.length
            }
            }
        '''
        rows = Model.get_temp_view(db,map_fun,reduce_fun).rows
        return json.dumps(rows)


api.add_resource(Documents, '/Api/Get_All_Document')
api.add_resource(DateDocuments, '/Api/Get_Date_Document')


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response
if __name__ == '__main__':
    app.run()
