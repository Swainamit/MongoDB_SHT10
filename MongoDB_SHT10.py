import pymongo
from time import sleep
import datetime
import json
from pymongo import MongoClient
import RPi.GPIO as GPIO
from pi_sht1x import SHT1x

now = datetime.datetime.now()
time1 = now.strftime("%d %B %Y at %H:%M:%S UTC")

try:
    conn  = MongoClient('Enter Host Name here')
    print("Connected to MongoDB successfully!!!")
    
except Exception as e:
    print(e)
    print("Could not connect to MongoDB. Trying again!")

db = conn['Enter name of DB']

collection = db.Collection_name #Enter your collection name

fixed_interval = 20
# Setup a loop to send Temperature values at fixed intervals in seconds

while True:
    try:
        with SHT1x(18, 23, gpio_mode=GPIO.BCM) as sensor:
            temp = sensor.read_temperature()
            hum = sensor.read_humidity(temp)
            dew1 = sensor.calculate_dew_point(temp, hum)
        #rec = {'temperature': str(temp),  'humidity': str(hum),  'dewpoint': dew1}
        rec = {'updatedAt': time1,'temperature': str(temp),  'humidity': str(hum),  'dewpoint': dew1}
        doc_id = pollution.insert_one(rec).inserted_id
        print(str(doc_id) + ", " + str(time1) + ", " + str(temp) + "°C, " + str(hum)+ "%, " + str(dew1) + "°C")
        
    except pymongo.errors.DuplicateKeyError:
        continue
    
    sleep(fixed_interval)