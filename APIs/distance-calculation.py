# distance calculation

# imports
import math
import flask
from flask import Flask
import requests
from flask import request, jsonify
# from geopy.geocoders import GoogleV3

# declarations
apiUrl='http://xaviercat.com:8089/coords?key=***&coords='
apiKey = '***'

# distance calculation function
def calc(fromcord, tocord): 
    x1=float(fromcord.split(',')[0].replace('.', ''))
    y1=float(fromcord.split(',')[1].replace('.', ''))
    x2=float(tocord.split(',')[0].replace('.', ''))
    y2=float(tocord.split(',')[1].replace('.', ''))
    print(f' f {x1}  {y1}') 
    print(f' t {x2}  {y2}') 
    dist=int(math.sqrt((x2-x1)**2 + (y2-y1)**2 ))
    return dist 

# print('%.2f' % calc(2,2,4,5))

# app name
app = flask.Flask(__name__)
app.config["DEBUG"] = True


# default reply
@app.route('/', methods=['GET'])
def home():
    return "<h1>OnLin Distance Calculator</h1><p>Distance Calculator API.</p>"


# main function
@app.route('/distance', methods=['GET'])
def calculate():
    if 'key' in request.args:
        if str(request.args['key']) == apiKey:
            if 'from' in request.args:
                if 'to' in request.args:
                    if  request.args['from'] != '' :
                        if request.args['to'] != '' :
                            fromCoord=str(request.args['from'])
                            print(f' from {fromCoord}')
                            toCoord=str(request.args['to'])
                            print(f' from {fromCoord}')
                            res = calc(fromCoord, toCoord)
                            return  jsonify({'distance' : res})   # res 
                        else:
                            return 'wrong "to" coords'
                    else:
                        return 'wrong "from" coords'
                else:
                    return 'missing "to"'
            else:
                return 'missing "from"'
        else:
            return 'wrong key'
    else:
        return 'error'
    


app.run(host='0.0.0.0', port='8093')
# app.run(host='0.0.0.0', port='8094')
