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
#Welcome page route
@app.route("/")
def welcome_page():
    return render_template("welcome.html")

#Patient login route
@app.route("/patient_login")
def patient_login_page():
    return render_template("patient-login.html")

#Patient register route
@app.route("/patient_register")
def patient_register():
    return render_template("patient-register.html")

#Doctor login route
@app.route("/doctor_login")
def doctor_login_page():
    return render_template("doctor-login.html")

#Doctor login unauthenticated
@app.route("/doctor_login_error")
def doctor_login_error():
    return render_template("doctor-login-error.html")

#Doctor login submit
# Called when doctor enters login info if username and password are correct, triggers the doctor portal else triggers the error login
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
            print("session[doctor]: " + str(session["doctor"]))
            doctor_info = status["DoctorID"]
            print(f"Status:{doctor_info}")
            return redirect(url_for('doctor_portal',doctor_info=doctor_info))
            #return redirect(url_for('doctor_portal'))
        else:
            return redirect(url_for('doctor_login_error'))

#Patient login unauthenticated
@app.route("/patient_login_error")
def patient_login_error():
    return render_template("patient_login_error.html")

#Patient login submit
# Called when patient enters login info if username and password are correct, triggers the doctor portal else triggers the error login
@app.route("/patient_login_submit",methods=["GET","POST"])
def patient_login_submit():
    if request.method =="POST":
        username=request.form['username']
        pwd = request.form['password']
        status = patient_login(username,pwd)
        print(username,pwd)
        print(status)
        
        if(status):
            del status["_id"]
            del status["password"]
            del status["hash_key"]
            status["CurrentAppointment"] = "None"
            return redirect(url_for('patient_portal',user_details=status))
        else:
            return redirect(url_for('patient_login_error'))


#Patient portal display, creates sessions
@app.route("/PatientPortal",methods=["GET","POST"])
def patient_portal():
    user_details = request.args.get("user_details")
    user_details = eval(user_details)
    session["patient"] = user_details["username"]
    return render_template("PatientPortal.html",user_details=user_details)

# Checks if username exists while a new patient tries to login
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

#Returns the schedule of the doctor for the patient to book an appointment
@app.route("/patient-doctor-dashboard/<doctor_id>")
def patient_doctor_dashboard(doctor_id):
    session["d_id"] = int(doctor_id)
    schedule = get_doctor_schedule(int(doctor_id))
    return render_template("patient-doctor-dashboard.html",doctor_info=schedule)

# Returns a list of doctors present
@app.route("/DoctorList")
def doctor_list():
    return render_template("DoctorList.html")

#Display the active schedule of the doctor to  check the list of patients who have booked an appointment
@app.route("/doctor_portal",methods=["GET","POST"])
def doctor_portal():
    doctor_info = request.args.get('doctor_info')
    #doctor_info = session.get("doctor")
    # Convert the string representation of the dictionary back to a dictionary
    #doctor_info = eval(doctor_info)
    print("session[doctor] at doctor_portal: " + str(session["doctor"]))
    schedule = get_doctor_schedule(int(doctor_info))
    #print(doctor_info,schedule)
    return render_template("doctor-dashboard.html",doctor_info=schedule) 

# Books an appointment for the patient, receives the doctor,day and time
@app.route("/patient_appt/<appt>")
def patient_appt(appt):
    decoded_string = unquote(appt)
    Day,time = decoded_string.split(" ")
    user_details = get_patient(session.get("patient"))
    status = book_appointment(session.get("d_id"),user_details["username"],Day,time,"")
    if(status):
        if(int(session.get("d_id"))==1):
            d_name = "Dr.Heather Conboy"
        elif(int(session.get("d_id"))==2):
            d_name = "Dr.David McManus"
        elif(int(session.get("d_id"))==3):
            d_name = "Dr.Hui Guan"   
        user_details["CurrentAppointment"] = Day+" "+time+" with " + d_name
        del user_details["_id"]
        del user_details["password"]
        del user_details["hash_key"]

        return redirect(url_for('patient_portal',user_details = user_details))

    else:
        return """Error in code: Not able to book appointment"""

# Displays the form for the doctor to enter the details about the patient during the interview
@app.route("/doctor_appt_view/<appt>")
def doctor_appt_view(appt):
    #print("session[doctor] at doctor_appt_view: " + str(session["doctor"]))
    decoded_string = unquote(appt)
    Day,time = decoded_string.split(" ")
    #print(Day,time)
    #schedule = get_doctor_schedule(id)
    #print("session.get(<doctor>): " + str(session.get("doctor")))
    schedule = get_doctor_schedule(session.get("doctor"))
    user_details = get_patient(schedule["Schedule"][Day][time])

    del user_details["_id"]
    del user_details["password"]
    del user_details["hash_key"]
    #user_details["_id"] = str(user_details["_id"])
    user_details["day"] = Day
    user_details["time"] =time
    for key in user_details:
        print(f"{key}:{type(user_details[key])}")
    return render_template("doctor-appt-view.html",user_details = user_details)
 
# Doctor logout
@app.route("/doctor_logout",methods=["GET","POST"])
def doctor_logout():
    session.pop('doctor', None)
    return redirect(url_for('welcome_page')) 

# Once the doctor hits submit on an appointment all the information entered is received and stored in the database
@app.route("/appt_submit/<day_time>",methods=["GET","POST"])
def appt_submit(day_time):
    bpUpper = request.form['bloodPressureUpper']
    print("bpUpper: " + bpUpper)
    bpLower = request.form['bloodPressureLower']
    bp = bpUpper + "/" + bpLower
    bpm = request.form['heartRate']
    oxysat = request.form["oxySat"]
    reasons = request.form["reasons"]
    notes = request.form["notes"]
    decoded_string = unquote(day_time)
    Day,time = decoded_string.split(" ")
    d_id = session.get("doctor")
    print(d_id, Day, time)
    patient = get_appointment(session.get("doctor"), Day, time)
    print(reasons)
    
    status = update_appointment(session.get("doctor"), Day, time, bp=bp, bpm=bpm, oxysat=oxysat, reasons=reasons, docnotes=notes)
    if(status):
        return redirect(url_for('doctor_portal',doctor_info = session.get("doctor")))
    else:
        return """Error"""

#Creates a visualization to the doctor on the previous appointments of the patient
@app.route("/medical_history_record/<appt_pat_id>",methods=["GET","POST"])
def medical_history(appt_pat_id):
    decoded_string = unquote(appt_pat_id)
    patient_id, day, time = decoded_string.split(" ")
    appointments = get_all_appointments(patient_id)
    # print(appointments)
    appointments_list = []
    if(appointments):
    #     for doc in appointments:
    #         print(f"{doc}:{type(doc)}")
        # appointments = list(appointments)
        for x in appointments:
            del x["_id"]
            appointments_list.append(x)
        return render_template("medical_history_record_v2.html", day=day, time=time, appts=appointments_list)

#patient logout
@app.route("/patient_logout",methods=["GET","POST"])
def patient_logout():
    session.pop('patient', None)
    session.pop("d_id",None)
    return redirect(url_for('welcome_page')) 
     
# Running app
if __name__ == '__main__':
    app.run(debug=True)
