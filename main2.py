#!usr/bin/python

from flask import (Flask, render_template, redirect, url_for, request, jsonify)
import requests
import serial
app = Flask(__name__)
s = serial.Serial("COM3")


@app.route("/")
def main():
    hum, temp, weather, tempFstr, city = get_data()
    return render_template("index2.html", hum=hum, temp=temp, weather=weather, tempF=tempFstr, city=city)


@app.route("/message", methods = ["POST"])
def message():
    message = request.form['message']
    conc_msg = 'B'+message+'\n'
    s.write(conc_msg.encode("ascii"))
    return redirect(url_for('main'))

def get_data():
    s.write('A'.encode("ascii"))
    msg = s.readline().decode("ascii")
    print("got msg: ", msg)
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
    city = values["name"]
    return hum, temp, weather, tempFstr, city

@app.route("/data.json", methods=["GET"])
def json_data():
    hum, temp, weather, tempFstr, city = get_data()
    data = {'Local Humidity': hum,
            'Local Temperature': temp,
            'City': city,
            'City Weather': weather,
            'City TemperatureF': tempFstr}
    return jsonify(data)

def get_remote_data():
    resp = requests.get('http://localhost:5001/data.json')
    values = resp.json()
    hum = values['Local Humidity']
    temp = values['Local Temperature']
    weather = values['City Weather']
    tempFstr = values['City TemperatureF']
    city = values["City"]
    return hum, temp, weather, tempFstr, city

app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)