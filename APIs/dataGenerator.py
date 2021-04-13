# data Generator 

# imports
import random
import datetime
from datetime import datetime, timedelta
import time
from pymongo import MongoClient
import requests
import json

# mongoDB connection string
uri = "mongodb://***:***@xaviercat.com/?authSource=bigData&authMechanism=SCRAM-SHA-256"

# variables
date_string=datetime.now()
titles='timeStamp, towerName, telephoneNumber, cos, conQuality, distFromTowr, numDiald, duration\n'
remotePath='/tmp/staging/phoneData/'
localPath='/tmp/'
cellphoneOS=['ios', 'android']
companyOut = ['050', '052', '053', '054', '055']
companyIn = ['050', '052', '053', '054', '04', '03', '08', '06', '077', '073', '055']


# mail loop
while True:
    # generating random information
    tower=random.choice(open('list_sites_tlv.txt').read().splitlines())
    tel=f'{random.choice(companyOut)}-{str(random.randint(1000000, 9999999))}'.strip()
    timeStamp=int(time.time())
    cos = random.choice(cellphoneOS)      # cellphone os
    distanceFromTower = str(random.randint(30, 1000)).strip()
    connectioQuality = f'{str(random.randint(1, 100)).strip()}%'
    numberDialed = f'{random.choice(companyIn)}-{str(random.randint(1000000, 9999999))}'.strip()
    callDuration = str(random.randint(1, 3000)).strip()
    # construct of dictionary
    dbDict={
        'timeStamp' : str(int(time.time())) ,
        'siteName' : tower, 
        'teNumber' : tel, 
        'cellPhoneOS' : cos, 
        'conQuality' : connectioQuality, 
        'distFromToer' : distanceFromTower,
        'callTo' : numberDialed,
        'callDuration' :  callDuration 
    }
    # connecting to mongoDB
    c = MongoClient(uri)
    mydb = c["bigData"]
    mycol = mydb["cellData"]
    # print(dbDict)
    # writing to mongoDB
    mycol.insert_one(dbDict)
    # waiting for rnd time
    time.sleep(random.randint(3, 6))

