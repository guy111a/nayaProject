
# imports
import telebot
from kafka import KafkaProducer
from datetime import datetime
import json
from msg_Result import msg_Result

print('starting telegram bot')

# Get Token from bot Father
token = '1470090878:AAGXlwguUthBx84SD1OFghppYcu62qrsrdo'
bot = telebot.TeleBot(token)
brokers = ['localhost:9092']
topics = 'LocationFromBot'
topics_target = "LocationToBot"

# creating object of kafka producer
producer = KafkaProducer(bootstrap_servers=brokers,
                                                 value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# telelgram bot handling function
@bot.message_handler(commands=['address'])
def address(message):
    # managing accepted values
    print(message.text)
    fileName='/tmp/bot_log_file.txt'
    command=message.text[8:].strip()
    if len(command) < 1:
        with open(fileName, 'a') as fd:
            fd.write(f"{datetime.now()} [ERR] bad/ empty request\n")
    else:
        with open(fileName, 'a') as fd:
            fd.write(f"{datetime.now()} [INFO] {message.chat.id} got request <{command}> \n")
        Location_Source = message.text[8:].strip()

        # sending data to kafka stream
        producer.send(topics, {'Location_Source': Location_Source})

        mychatid = message.chat.id
        print(mychatid)

        # flushing to kafka
        producer.flush()

        # saving to file
        with open('/tmp/Location_Target.txt', 'r') as f:
            Location_Target = (f.read().split('=')[0])

        ## get address of user location from telegram BOT , return the address of the most close and vacant corona test location
        def get_Location(Location):
            return msg_Result.get_Location(Location)
        Location_Target = get_Location(Location_Source)

        # retuning the most close and vacant coronat test location to the user telegram client
        bot.reply_to(message, f'{Location_Target}\'s Location is 4u')

bot.polling()