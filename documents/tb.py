# tele bot

import telebot
import requests
from kafka import KafkaProducer
import json
from datetime import datetime
from kafka import KafkaConsumer

print('starting telegram bot')

# Get Token from bot Father
# token = '1470090878:AAGXlwguUthBx84SD1OFghppYcu62qrsrdo'
token = '1600767982:AAGJZ6SG_umpMoDT6cj8L-kz98u8yu1w2Ww'
apiUrl='http://xaviercat.com:8089/address?key=2021&address='
apiKey = '2021'
bot = telebot.TeleBot(token)
#consumer = KafkaConsumer('fromBot', bootstrap_servers=['xaviercat.com:9092'])
topicTo = 'toBot'
topicFrom = 'fromBot'
brokers = ['xaviercat.com:9092']

producer = KafkaProducer(
    bootstrap_servers = brokers,
    client_id = 'producer',
    acks = 1,
    compression_type = None,
    retries = 3,
    reconnect_backoff_ms = 50,
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    reconnect_backoff_max_ms= 1000)

@bot.message_handler(commands=['address'])
def address(message):
    fileName='/tmp/bot_log_file.txt'
    command=message.text[8:].strip()
    if len(command) < 1:
        with open(fileName, 'a') as fd:
            fd.write(f"{datetime.now()} [ERR]:{message.id}: bad/ empty request\n")
        bot.reply_to(message,'example:  /address [street address]')
    else:
        # print(command)
        url = f'{apiUrl}{command}'
        # print(url)
        response = requests.get(url)
        x = response.json()
        print(f'{datetime.now()} : [INFO] got "{command}" {x}' )
        with open(fileName, 'a') as fd:
            fd.write(f"{datetime.now()} [INFO]:{message.chat.id}: got request <{command}> \n")
        # bot.reply_to(message,str(x))
        # producer.send(topic=topicFrom, value=(x)) #.encode('utf-8'))
        producer.send(topicFrom, x)
        producer.flush()
        consumer = KafkaConsumer(topicTo, bootstrap_servers=['xaviercat.com:9092'])
        while message in consumer:
            print(f'from topic: {message.value}')
            bot.reply_to(message, message.value)


bot.polling()
