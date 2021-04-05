
# imports
import flask
from flask import request, jsonify
from werkzeug import datastructures
from pymongo import MongoClient
from flask import Flask
from flask_pymongo import PyMongo
import time

# declarations
api_key = '2021'
uri = "mongodb://user:2020P@xaviercat.com/?authSource=bigData&authMechanism=SCRAM-SHA-256"

app = flask.Flask(__name__)
app.config["DEBUG"] = True

app.config['MONGO_DBNAME'] = 'bigData'
app.config['MONGO_URI'] = 'mongodb://user:2020P@xaviercat.com/bigData?authSource=bigData&authMechanism=SCRAM-SHA-256'
mongo = PyMongo(app)

#  default api reply
@app.route('/', methods=['GET'])
def home():
    return "<h1>A.P.I</h1><p>CellPhone DATA access API.</p>"

# some instructions and error messages
@app.route('/api/data/all', methods=['GET'])
def api_all():
    if 'key' in request.args:
        if str(request.args['key']) == api_key:
            if 'limit' in request.args:
                limit = int(request.args['limit'])
            else:
                limit = 10
            output = []
            q = { }
            for s in mongo.db.cellData.find(q).limit(limit):
                output.append({'time Stamp' : s['timeStamp'],'siteName' : s['siteName'],'telephone' : s['teNumber'], 'cellPhoneOS' : s['cellPhoneOS'], 'conQuality' : s['conQuality'], 'distFromToer' : s['distFromToer'], 'callTo' : s['callTo'], 'callDuration' : s['callDuration']})
                # print(output)
            return jsonify({'result' : output})
        else:
            return "Error: KEY is wrong / missing ."

# main function and data handling
@app.route('/api/data', methods=['GET'])
def api_filter():
    if 'key' in request.args:
        if str(request.args['key']) == api_key:
            q = { }
            if 'comQup' in request.args:
                if 'comQdw' in request.args:
                    comQ = { 'conQuality' : { '$gt' : int(request.args['comQdw'])  , '$lt' : int(request.args['comQup']) }}
                q.update(comQ)
            if 'limit' in request.args:
                limit = int(request.args['limit'])
            else:
                limit = 10
            if 'cos' in  request.args:
                cos = {'cellPhoneOS': str(request.args['cos'])}
                q.update(cos)
            if 'tw' in  request.args:
                 tw = {'tower': str(request.args['tw'])}
                 q.update(tw)
            if 'startTS' in  request.args:
                if 'stopTS' in  request.args:
                    TS = {'timeStamp' :{ '$gt' : str(request.args['startTS']) ,  '$lt' : str(request.args['stopTS']) }}
                    q.update(TS)
                else:
                    return "missing end time"

            print(f'\nq')
            output = []
            for s in mongo.db.cellData.find(q).limit(limit):
                output.append({'time Stamp' : s['timeStamp'],'siteName' : s['siteName'],'telephone' : s['teNumber'], 'cellPhoneOS' : s['cellPhoneOS'], 'conQuality' : s['conQuality'], 'distFromToer' : s['distFromToer'], 'callTo' : s['callTo'], 'callDuration' : s['callDuration']})
                # print(output)
            return jsonify({'result' : output})
        else:
            return "Error: KEY is wrong / missing ."



app.run(host='0.0.0.0', port='7777')