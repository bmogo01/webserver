#/!/usr/bin/python3

from flask import (Flask, render_template, redirect, url_for, request, jsonify)
import requests
#import serial
app = Flask(__name__)
#s = serial.Serial("COM3")


@app.route("/")
def main():
#    s.write('A'.encode("ascii"))
#    msg = s.readline().decode("ascii")
#    msg = msg.split(',')
#    hum = msg[0]
#    temp = msg[1]
    hum = 25.00
    temp = 50.00
    on_class = "btn btn-secondary"
    off_class = "btn btn-secondary"
    if ledState == 1:
        on_class+=" active"
    else:
        off_class += " active"

    resp = requests.get('https://api.openweathermap.org/data/2.5/weather?q=Annapolis&appid=12f00a07d488c607af9dd0810ee37290')
    values = resp.json()
   # import pdb
   # pdb.set_trace()
    weather = values['weather'][0]['description']
    tempK = values['main']['temp']
    tempF = (float(tempK)-273.15)*(9/5)+32
    tempFstr = "%.2f"%tempF
    wind = values["wind"]
    city = values["name"]
    #sunrise = values[""]

    return render_template("index.html",hum=hum, temp=temp, led_off_class=off_class, led_on_class = on_class,
                           descript=weather, tempF=tempFstr, wind=wind, city=city)

@app.route("/turn_on")
def ledOn():
    global  ledState
#    s.write('B'.encode("ascii"))
#    s.readline()
    ledState = 1
    return redirect(url_for('main'))

@app.route("/turn_off")
def ledOff():
    global ledState
   # s.write('C'.encode("ascii"))
   # s.readline()
    ledState = 0
    return redirect(url_for('main'))

@app.route("/buzz_on")
def buzzOn():
    global ledState
   # s.write('D'.encode("ascii"))
   # s.readline()
    return redirect(url_for('main'))

@app.route("/buzz_off")
def buzzOff():
    global ledState
   # s.write('E'.encode("ascii"))
   # s.readline()
    return redirect(url_for('main'))

@app.route("/message", methods = ["POST"])
def message():
    message = request.form['message']
    print('The user sent [%s]' % message)
    return "OK"

@app.route("/data.json", methods=["GET"])
def json_data():
    data = {'temp': 72.1,
            'humidity': 0.36}
    return jsonify(data)


ledState=0
print("I ran this line")


app.run(host="0.0.0.0", port=8080, debug=True, use_reloader=False)

