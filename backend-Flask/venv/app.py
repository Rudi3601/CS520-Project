from flask import Flask
from flask import Flask, render_template, request,jsonify,redirect, url_for
from pymongo import MongoClient
import datetime
from mongo import *
 
x = datetime.datetime.now()
 
# Initializing flask app
app = Flask(__name__, static_url_path='/static')
 
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
def patient_login():
    return render_template("patient-login.html")

@app.route("/patient_register")
def patient_register():
    return render_template("patient-register.html")

@app.route("/doctor_login")
def doctor_login():
    return render_template("doctor_login.html")

@app.route("/patient_login_submit",methods=["GET","POST"])
def patient_login_submit():
    if request.method =="POST":
        username=request.form['username']
        pwd = request.form['pwd']
        status = get_user(user,passw)
        if(status):
            return render_template()

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
        # status = user_exists()
        status = add_user(username,pwd,Name,email,DOB,medication,allergies)
        status = False
        if(status):
            return redirect(url_for('patient_login'))
        else:
            return redirect(url_for('patient_register_userexist'))


 
     
# Running app
if __name__ == '__main__':
    app.run(debug=True)