from flask import Flask, request, render_template, make_response, session, jsonify, redirect
import json
import os
from scrapper import *
from pathlib import Path
import pymysql

app = Flask(__name__)
app.secret_key = os.urandom(24)

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

    if session.get('logged_in'):
        with open("UserData/"+session['email']+"_Cart.json", 'r') as file:
            jsonDetails = json.loads(file.read())
        return render_template("Build.html", parts=components, selectedParts=jsonDetails)
    else:
        return redirect("/")


# AJAX REQUESTS
@app.route("/register", methods=['POST'])
def register():
    conn = pymysql.connect(host='localhost', user='root', password='', db='partpickr')
    cursor = conn.cursor()

    email = request.form['Email']
    password = request.form['Password']
    name = request.form['Name']
    age = request.form['Age']

    sql = "INSERT INTO users VALUES(%s, %s, %s, %s)"
    data = (email, password, name, age)
    print(sql, data)
    result = cursor.execute(sql, data)
    conn.commit()
    print(result)

    conn.close()
    if result == 1:
        open("UserData/"+email+"_Cart.json", "w")
        return jsonify({"Flag": True, "Message": 'Registered'})
    else:
        return jsonify({"Flag": False, "Message": 'Retry'})


@app.route("/login", methods=['POST'])
def login():
    conn = pymysql.connect(host='localhost', password='', user='root', db='partpickr')
    cursor = conn.cursor()

    email = request.form['Email']
    password = request.form['Password']

    sql = "SELECT * FROM users WHERE email = %s AND password = %s"
    data = (email, password)
    rows = cursor.execute(sql, data)
    result = cursor.fetchone()
    print(result)

    conn.close()
    if rows == 1:
        session.permanent = True
        session['logged_in'] = True
        session['name'] = result[2]
        session['age'] = result[3]
        session['email'] = result[0]
        response = {"Flag": True, "Email": result[0], "Name": result[2], "Age": result[3]}
    else:
        response = {"Flag": False}

    return jsonify(response)


@app.route("/logout", methods=['GET', 'POST'])
def logout():
    session['logged_in'] = False
    session['name'] = ''
    session['age'] = ''
    session['email'] = ''
    return 'Logged out'

@app.route("/changeinfo", methods=['POST'])
def changeinfo():
    conn = pymysql.connect(host='localhost', password='', user='root', db='partpickr')
    cursor = conn.cursor()

    name = request.form['Name']
    age = request.form['Age']
    email = request.form['Email']
    password = request.form['Password']

    if password != "":
        sql = "UPDATE users SET name = %s, age = %s, password = %s WHERE email = %s"
        data = (name, age, password, email)
    else:
        sql = "UPDATE users SET name = %s, age = %s WHERE email = %s"
        data = (name, age, email)
    result = cursor.execute(sql, data)
    conn.commit()
    print(result)

    conn.close()
    if result == 1:
        session['name'] = name
        session['age'] = age
        session['email'] = email
        response = {"Flag": True, "Email": email, "Name": name, "Age": age}
    else:
        response = {"Flag": False}

    return jsonify(response)


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


@app.route("/build/addpart", methods=['POST'])
def add_part():
    part_id = int(request.form["PartID"])
    part = request.form["Part"]
    email = session['email']
    file_path = Path("./Parts/" + part + ".json")
    if not file_path.exists():
        scrape(part, 2)

    with open("./Parts/" + part + ".json", "r") as file:
        available_parts = json.loads(file.read())

    print(part, part_id, email)
    with open("UserData/"+email+"_Cart.json", 'r') as file:
        jsonDetails = json.loads(file.read())
        jsonDetails[part] = available_parts[part_id]
    with open("UserData/"+email+"_Cart.json",'w') as file:
        json.dump(jsonDetails, file)
    
    return render_template("Part.html", part=part, src=available_parts[part_id]['Img_Src'], title=available_parts[part_id]['Title'], price=available_parts[part_id]['Price'])

@app.route("/build/removepart", methods=['POST'])
def remove_part():
    part = request.form["Part"]
    email = session['email']
    print(part)
    with open("UserData/"+email+"_Cart.json", 'r') as file:
        jsonDetails = json.loads(file.read())
        jsonDetails.pop(part)

    with open("UserData/"+email+"_Cart.json",'w') as file:
        json.dump(jsonDetails, file)

    return 'Removed ' + part

if __name__ == "__main__":
    app.run(debug=True)
