
'''
    this script imports data from mongodb using web API into mysql
    using KAFKA, SPARK WEB Service and Mysql
    this script imports the data periodically  ( 10 min interval )
'''

# imports
import time as tm
from kafka import KafkaProducer
import json
import requests

# kafka declarations
bootstrapServers = "localhost:9092"
topics = "RawData"

producer = KafkaProducer(bootstrap_servers='***:9092',
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# concatanating the URL string
limit = '&limit=100'
start_ts = str(int(tm.time()) - 6000)
fromDate = f'&startTS={start_ts}&stopTS={str(int(tm.time()))}'
api = ('http://xaviercat.com:8085/api/data/all?key=***')
url = api + fromDate + limit
data = requests.get(url)
print(url)

# revtreave data from API and saves them to mysql
w = []
w_json = []
data_json = json.loads(data.text)['result']
for x in data_json:
    w_json.append(x)
    print(f'{x}')

    callDuration = x['callDuration']
    callTo = x['callTo']
    cellPhoneOS = x['cellPhoneOS']
    conQuality = x['conQuality']
    distFromToer = x['distFromToer']
    telephone = x['telephone']
    timeStamp = x['time Stamp']
    siteName = x['siteName']

    print(callDuration, callTo, cellPhoneOS, conQuality, distFromToer, telephone, timeStamp, siteName)
    producer.send(topics, {'callDuration': callDuration,
                           'callTo': callTo,
                           'cellPhoneOS': cellPhoneOS,
                           'conQuality': conQuality,
                           'distFromToer': distFromToer,
                           'telephone': telephone,
                           'timeStamp': timeStamp,
                           'siteName': siteName})
    w.append([callDuration, callTo, cellPhoneOS, conQuality, distFromToer, telephone, timeStamp, siteName])
    tm.sleep(2)

print('row: ', len(w))
