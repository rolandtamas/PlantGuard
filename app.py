import time

from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from gpiozero import DigitalInputDevice
import datetime
import sqlite3
import sys
import Adafruit_DHT
from picamera import PiCamera
from time import sleep

d0_input = DigitalInputDevice(17)
d1_input = DigitalInputDevice(27)
contor = 0

app = Flask(__name__)
global temperature, humidity

@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')


@app.route('/waterplant', methods=['POST','GET'])
def waterPlant():
    if request.method == "POST":
        database = sqlite3.connect('smartgarden.db')
        if not d0_input.value or not d1_input.value:
            print('Info from sensor:Moisture threshhold reached!')
            current_time = ""
        else:
            print('Need to water the plant')
            #cod pompa de apa
            waterpin = 5
            time.sleep(2)
            #1 logic pe pin 5
            time.sleep(2)
            #0 logic pe pin 5

            current_time = datetime.date.today().strftime('%d/%m/%Y')
        try:
            database.execute("INSERT INTO GREENHOUSE (date) VALUES (?)", current_time)
        except:
            database.execute(
                '''CREATE TABLE GREENHOUSE(ID INTEGER PRIMARY KEY AUTOINCREMENT,temperatura FLOAT, umiditate FLOAT, date TEXT)''')
            database.execute("INSERT INTO GREENHOUSE (date) VALUES (?)", current_time)
        database.commit()
        cursor = database.execute("SELECT ID,temperatura, umiditate from GREENHOUSE")
        for row in cursor:
            print(row[0])
            print(row[1])
            print(row[2])
        database.close()
    return "Ok"



@app.route('/airhumidity')
def getAirHumidity():
    humidity= Adafruit_DHT.read_retry(11, 4)

    #cod pentru senzor umiditate
    database = sqlite3.connect('smartgarden.db')
    print("Humidity: {1:0.1f} %".format(humidity))
    try:
        database.execute("INSERT INTO GREENHOUSE (umiditate) VALUES (?)",
                          humidity)
    except:
        database.execute(
            '''CREATE TABLE GREENHOUSE(ID INTEGER PRIMARY KEY AUTOINCREMENT,temperatura FLOAT, umiditate FLOAT, date TEXT)''')
        database.execute("INSERT INTO GREENHOUSE (umiditate) VALUES (?)",
                         humidity)
    database.commit()
    return "You have accessed air humidity"


@app.route('/airtemperature')
def getAirTemp():
    #cod senzor temperatura aer
    return "You have accessed air temperature"


@app.route('/viewcamera')
def viewCameraFeed():
    camera = PiCamera()
    camera.rotation = 180
    camera.start_preview()
    camera.start_recording('video.h264')
    camera.stop_recording()
    camera.stop_preview()
    return render_template("camera.html")


if __name__ == "__main__":
    app.run(debug=True)
