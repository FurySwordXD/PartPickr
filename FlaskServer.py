from flask import Flask, request, render_template, make_response
import json
import os
from scrapper import *
from pathlib import Path
import pymysql

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def index():
    return render_template("Home.html")

@app.route("/build")
def build():
    components = {
        "Processor": "Processor",
        "CPU Cooler": "CPUCooler",
        "Motherboard": "Motherboard",
        "Memory": "Memory",
        "Storage": "Storage",
        "GPU": "GPU",
        "Case": "Case",
        "PSU": "PSU",
        "OS": "OS",
        "Monitor": "Monitor",
    }
    return render_template("Build.html", parts=components)


# AJAX REQUESTS
@app.route("/register", methods=['POST'])
def register():
    conn = pymysql.connect(host='localhost', password='', user='root', db='partpickr')
    cursor = conn.cursor()

    username = request.form['Username']
    password = request.form['Password']
    name = request.form['Name']
    age = request.form['Age']

    sql = "INSERT INTO users VALUES(%s, %s, %s, %s)"
    data = (username, password, name, age)
    print(sql, data)
    rows = cursor.execute(sql, data)
    print(rows)

    conn.close()
    if rows == 1:
        return 'Logged in'
    else:
        return 'Retry'

@app.route("/login", methods=['POST'])
def login():
    conn = pymysql.connect(host='localhost', password='', user='root', db='partpickr')
    cursor = conn.cursor()

    username = request.form['Username']
    password = request.form['Password']

    sql = "SELECT * FROM users WHERE email = " + username + "AND password = " + password
    rows = cursor.execute(sql)
    result = cursor.fetchone()
    print(result)

    conn.close()
    if rows == 1:
        return 'Logged in'
    else:
        return 'Retry'


@app.route("/build/getparts", methods=['POST'])
def getparts():
    part = request.form["Type"]
    file_path = Path("./Parts/" + part + ".json")
    if not file_path.exists():
        scrape(part, 2)
    file = open("./Parts/"+part+".json", "r")
    data = file.read()
    available_parts = json.loads(data)
    file.close()
    modal_html = render_template("BuildModal.html", availableParts=available_parts, part=part)
    return modal_html


@app.route("/build/addpart/<part>", methods=['POST'])
def addpart(part):
    part_id = int(request.form["PartID"])
    file_path = Path("./Parts/" + part + ".json")
    if not file_path.exists():
        scrape(part, 2)
    file = open("./Parts/" + part + ".json", "r")
    data = file.read()
    available_parts = json.loads(data)
    file.close()

    return render_template("Part.html", part=part, src=available_parts[part_id]['Img_Src'], title=available_parts[part_id]['Title'], price=available_parts[part_id]['Price'])


if __name__ == "__main__":
    app.run()