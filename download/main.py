#!usr/bin/python

from flask import (Flask, render_template, redirect, url_for)
import serial
app = Flask(__name__)
s = serial.Serial("/dev/ttyACM0")

@app.route("/")
def main():
    s.write('A'.encode("ascii"))
    msg = s.readline().decode("ascii")
    msg = msg.split(',')
    hum = msg[0]
    temp = msg[1]
    on_class = "btn btn-secondary"
    off_class = "btn btn-secondary"
    if ledState == 1:
        on_class+=" active"
    else:
        off_class += " active"
    print(ledState)
    print("on class: [%s]" % on_class)
    print("off class: [%s]" % off_class)
    return render_template("index.html",hum=hum,temp=temp,led_off_class=off_class,
     led_on_class = on_class)

@app.route("/turn_on")
def ledOn():
    global  ledState
    s.write('B'.encode("ascii"))
    s.readline()
    ledState = 1
    return redirect(url_for('main'))

@app.route("/turn_off")
def ledOff():
    global ledState
    s.write('C'.encode("ascii"))
    s.readline()
    ledState = 0
    return redirect(url_for('main'))

@app.route("/buzz_on")
def buzzOn():
    global ledState
    s.write('D'.encode("ascii"))
    s.readline()
    return redirect(url_for('main'))

@app.route("/buzz_off")
def buzzOff():
    global ledState
    s.write('E'.encode("ascii"))
    s.readline()
    return redirect(url_for('main'))


ledState=0
print("I ran this line")
