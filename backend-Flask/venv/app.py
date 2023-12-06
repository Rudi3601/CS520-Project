from flask import Flask
from flask import Flask, render_template, request,jsonify,redirect, url_for,session
from pymongo import MongoClient
import datetime
from mongo import *
from urllib.parse import unquote
from flask_session import Session
 
x = datetime.datetime.now()

import secrets

def generate_random_key(length=24):
    # Generate a random key with the specified length
    random_key = secrets.token_hex(length // 2)
    return random_key

app = Flask(__name__, static_url_path='/static')
app.config["SESSION_PERMANENT"] = False
app.secret_key = secrets.token_hex(24)
#Session(app)
#DB connection
client = MongoClient("mongodb+srv://super:xCtC5CJfyAWJyvCK@atlascluster.j0uq5ga.mongodb.net/")
 
# Route for seeing a data
# @app.route('/data')
# def get_time():
 
#     # Returning an api for showing in  reactjs
#     return {
#         'Name':"geek", 
#         "Age":"22",
#         "Date":x, 
#         "programming":"python"
#         }

"""
Called after the user hits submit in the register page
Sends all the info to the add_user function in the mongo.py.
The add user checks whether a username already exists or not.

Return type true or false:
True: New user added successfully
False: Username already exists
"""

@app.route("/")
def welcome_page():
    return render_template("welcome.html")

@app.route("/patient_login")
def patient_login_page():
    return render_template("patient-login.html")

@app.route("/patient_register")
def patient_register():
    return render_template("patient-register.html")

@app.route("/doctor_login")
def doctor_login_page():
    return render_template("doctor-login.html")

@app.route("/doctor_login_submit",methods=["GET","POST"])
def doctor_login_submit():
    if request.method =="POST":
        username=request.form['username']
        pwd = request.form['password']
        status = doctor_login(username,pwd)
        #print(username,pwd)
        #print(status)      
        if(status):
            session["doctor"] = status["DoctorID"]
            doctor_info = status["DoctorID"]
            print(f"Status:{doctor_info}")
            return redirect(url_for('doctor_portal',doctor_info=doctor_info))
            #return redirect(url_for('doctor_portal'))
        else:
            return """<html>Wrong username or password</html>"""

@app.route("/patient_login_submit",methods=["GET","POST"])
def patient_login_submit():
    if request.method =="POST":
        username=request.form['username']
        pwd = request.form['password']
        status = patient_login(username,pwd)
        print(username,pwd)
        print(status)
        if(status):
            return """<html>Welcome Patient</html>"""
        else:
            return """<html>Wrong username or password</html>"""

@app.route("/patient_register_userexist")
def patient_register_userexist():
    return render_template("patient-register-userexist.html")

"""
Called after the user hits submit in the register page
Sends all the info to the add_user function in the mongo.py.
The add user checks whether a username already exists or not.

Return type true or false:
True: New user added successfully
False: Username already exists
"""
@app.route("/Patient_reg_submit", methods=["GET","POST"])
def new_patient_submit():
    if request.method == "POST":
        username=request.form['username']
        Name = request.form['name']
        DOB = request.form['dob']
        medication = request.form['conditions']
        allergies = request.form['allergies']
        pwd = request.form['password']
        c_pwd = request.form['confirm_password']
        email = request.form['email']
        status = patient_exists(username)
        #status = add_patient(username,pwd,Name,email,DOB,medication,allergies)
        if(not status):
            added_flag = add_patient(username,pwd,Name,email,DOB,medication,allergies)
            if(added_flag):
                return redirect(url_for('patient_login_page'))
            else:
                return """<html>Cant add</html>"""
        else:
            return redirect(url_for('patient_register_userexist'))


@app.route("/doctor_portal",methods=["GET","POST"])
def doctor_portal():
    doctor_info = request.args.get('doctor_info')
    #doctor_info = session.get("doctor")
    # Convert the string representation of the dictionary back to a dictionary
    #doctor_info = eval(doctor_info)
    schedule = get_doctor_schedule(int(doctor_info))
    #print(doctor_info,schedule)
    return render_template("doctor-dashboard.html",doctor_info=schedule) 

@app.route("/doctor_appt_view/<appt>")
def doctor_appt_view(appt):
    decoded_string = unquote(appt)
    Day,time = decoded_string.split(" ")
    #print(Day,time)
    #schedule = get_doctor_schedule(id)
    print(session.get("doctor"))
    schedule = get_doctor_schedule(session.get("doctor"))
    user_details = get_patient(schedule["Schedule"][Day][time])
    del user_details["_id"]
    del user_details["password"]
    del user_details["hash_key"]
    #user_details["_id"] = str(user_details["_id"])
    for key in user_details:
        print(f"{key}:{type(user_details[key])}")
    return render_template("doctor-appt-view.html",user_details = user_details)

@app.route("/doctor_logout",methods=["GET","POST"])
def doctor_logout():
    session.pop('doctor', None)
    return redirect(url_for('welcome_page')) 
     
# Running app
if __name__ == '__main__':
    app.run(debug=True)