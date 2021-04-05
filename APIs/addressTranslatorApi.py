
# imports
import flask
from flask import Flask
import requests
from flask import request, jsonify
from geopy.geocoders import GoogleV3

apiKey = '2021'

# declaring the APP name
app = flask.Flask(__name__)
app.config["DEBUG"] = True

#  default api reply
@app.route('/', methods=['GET'])
def home():
    return "<h1>A.P.I</h1><p>Address translator API.</p>"

# some instructions and error messages
@app.route('/coords', methods=['GET'])
def rTranslate():
    if 'key' in request.args:
        if str(request.args['key']) == apiKey:
            if 'coords' in request.args:
                if  request.args['coords'] != '' :
                    googleKey='AIzaSyB1KHBiMKs6s_DGMb6Prbb0MywWAwWxM_8'
                    coords = str(request.args['coords'])
                    print(f' coords {coords}')
                    lat=str(coords[0])
                    long=str(coords[1])
                    # print(f' .. {lat} {long}')
                    geolocator = GoogleV3(api_key=googleKey)
                    res = str(geolocator.reverse(coords))
                    return res
                else:
                    return 'illegal coords'
            else:
                return 'missing coords'
        else:
            return 'missing or wrong key'


# main function and data handling
@app.route('/address', methods=['GET'])
def translate():
    if 'key' in request.args:
        if str(request.args['key']) == apiKey:
            if 'address' in request.args:
                if  request.args['address'] != '' :
                    list=[]
                    address=str(request.args['address'])
                    list=address.split()
                    adrs='+'.join(list)
                    googleKey='AIzaSyB1KHBiMKs6s_DGMb6Prbb0MywWAwWxM_8'
                    url=f"https://maps.googleapis.com/maps/api/geocode/json?address={adrs}&key={googleKey}"
                    print(url)
                    x = requests.get(url).json()
                    l=x['results'][0]['geometry']
                    lat=l['location']['lat']
                    lng=l['location']['lng']
                    res = { 'lat' : lat , 'lng' : lng }
                    return res
                else:
                    return 'illegal address'
            else:
                return 'missing address'
        else:
            return 'missing or wrong key'


app.run(host='0.0.0.0', port='8089')