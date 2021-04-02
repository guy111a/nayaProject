'''
    this script imports data from mongodb using web API into mysql
    using KAFKA, SPARK WEB Service and Mysql
    this script imports the data periodically  ( 10 min interval )
'''

import os
import pyarrow as pa
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql.functions import StringType
from pyspark.sql.types import StringType, StructType, IntegerType, MapType, FloatType
import pandas as pd
import json
from kafka import KafkaConsumer
import mysql.connector as mc
from datetime import datetime

os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.1 pyspark-shell'

bootstrapServers = "localhost:9092"

# connector to mysql
mysql_username = 'naya'
mysql_password = 'naya'
host = 'localhost'
mysql_port = 3306
mysql_database_name = 'Cellular'

mysql_conn = mc.connect(
    user=mysql_username,
    password=mysql_password,
    host=host,
    port=mysql_port,
    autocommit=True,  # <--
    database=mysql_database_name)

# spark object
spark = SparkSession\
        .builder\
        .appName("FromKafkaToParquet")\
        .getOrCreate()

#kafka variables
topics = "RawData"
brokers = ['localhost:9092']

consumer = KafkaConsumer(
    topics,
    group_id='File_MySQL_HDFS',
    bootstrap_servers=brokers,
    auto_offset_reset='latest',
    enable_auto_commit=True,
    auto_commit_interval_ms=1000)

df_kafka = spark\
    .readStream\
    .format("kafka")\
    .option("kafka.bootstrap.servers", bootstrapServers)\
    .option("subscribe", topics)\
    .load()

schema = StructType() \
    .add("callDuration", IntegerType(), True) \
    .add("callTo", StringType(), True) \
    .add("cellPhoneOS", StringType(), True) \
    .add("conQuality", StringType(), True) \
    .add("distFromToer", StringType(), True) \
    .add("telephone", StringType(), True) \
    .add("timeStamp", StringType(), True) \
    .add("siteName", StringType(), True) \
    .add("CallDateTime",TimestampType(), True) \
    .add("CallDate", DateType(), True) \
    .add("CallTime", StringType(), True)

df_tower = df_kafka.select(col("value").cast("string"))\
           .select(from_json(col("value"), schema).alias("value"))\
           .select("value.*")

df_tower.printSchema()

''' 
    this script imports data from mongodb using web API into mysql
'''
def mysql_event_insert(mysql_conn, callDuration, callTo, cellPhoneOS, conQuality, distFromToer, telephone, timeStamp,
                       tower, CallDateTime, CallDate, CallTime):
    mysql_cursor = mysql_conn.cursor()
    sql = insert_statement.format(callDuration, callTo, cellPhoneOS, conQuality, distFromToer, telephone, timeStamp,
                                  tower, CallDateTime, CallDate, CallTime)
    mysql_cursor.execute(sql)
    mysql_cursor.close()


for message in consumer:
    events = json.loads(message.value)

    callDuration = events['callDuration']
    callTo = events['callTo']
    cellPhoneOS = events['cellPhoneOS']
    conQuality = events['conQuality']
    distFromToer = events['distFromToer']
    telephone = events['telephone']
    timeStamp = events['timeStamp']
    print(type(timeStamp))
    siteName = events['siteName']

    dt_object = datetime.fromtimestamp(int(timeStamp))
    CallDateTime = dt_object
    only_date, only_time = dt_object.date(), dt_object.time()
    CallDate = only_date
    CallTime = only_time

    print(str(callDuration), callTo, cellPhoneOS, conQuality, distFromToer, telephone, timeStamp, siteName,
          str(CallDateTime), str(CallDate), CallTime)

    insert_statement = """
                            INSERT INTO Cellular.CallsData(callDuration,callTo,cellPhoneOS,conQuality,distFromToer,telephone,timeStamp,siteName,CallDateTime,CallDate,CallTime) 
                            VALUES ('{}', '{}', '{}' , '{}', '{}', '{}' , '{}', '{}', '{}', '{}', '{}');"""

    mysql_event_insert(mysql_conn, callDuration, callTo, cellPhoneOS, conQuality, distFromToer, telephone, timeStamp,
                       siteName, CallDateTime, CallDate, CallTime)

