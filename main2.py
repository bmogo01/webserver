#!usr/bin/python

from flask import (Flask, render_template, redirect, url_for, request, jsonify)
import requests
import serial
app = Flask(__name__)
s = serial.Serial("COM3")


@app.route("/")
def main():
    hum, temp, weather, tempFstr, wind, city = get_data()
    return render_template("index.html", hum=hum, temp=temp, descript=weather, tempF=tempFstr, wind=wind, city=city)


@app.route("/message", methods = ["POST"])
def message():
    message = request.form['message']
    conc_msg = 'B'+message+'\n'
    s.write(conc_msg.encode("ascii"))
    return redirect(url_for('main2'))

def get_data():
    s.write('A'.encode("ascii"))
    msg = s.readline().decode("ascii")
    msg = msg.split(',')
    hum = msg[0]
    temp = msg[1]

    resp = requests.get(
        'https://api.openweathermap.org/data/2.5/weather?q=Annapolis&appid=12f00a07d488c607af9dd0810ee37290')
    values = resp.json()
    # import pdb
    # pdb.set_trace()
    weather = values['weather'][0]['description']
    tempK = values['main']['temp']
    tempF = (float(tempK) - 273.15) * (9 / 5) + 32
    tempFstr = "%.2f" % tempF
    wind = values["wind"]
    city = values["name"]
    return hum, temp, weather, tempFstr, wind, city

app.run(host="0.0.0.0", port=8080, debug=True, use_reloader=False)