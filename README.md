# Patient Tracker System Backend
UMass CS520 Fall 2023 Project

## Usage
```
pip3 install -r requirements.txt
cd src
pip3 app.py
```
You will see a message similar to "Running on http://127.0.0.1:5000".
Open the link on your browser and you can start experimenting with the app.

## Existing Profiles to experiment with
For doctors, the profiles already exist in the database. You can log in with the following username/password pairs to experiment.
hconboy/doctor11
dmanus/doctor22

For patients, you can either create new profiles, or use the following username/password pairs that already exist in the database.
jsmith/1234
smith/1234

## Flask app
The flask app takes care of the routing and rendering of html pages. It also makes sure the logic works between patient login, doctor login, and scheduling.

#### app route "/":
- Returns the welcome page using the render template function

#### app route "patient_login":
- Returns the patient login page using the render template function

#### app route "patient_login_error":
- returns an error message if the username or password is wrong

#### app route "patient_login_submit":
- Once the patient presses submit in the login page, the user name and password is verified
- If it is valid, the patient portal is open, creates a session for the patient
- Receives the user details using the patient_login from the mongo.py 
- Else the patient login error app route is triggered

#### app route "patient_register":
- returns the patient register page using the render template function

#### app route "Patient_register_userexist":
- returns an error message if the username already exists when the patient registers

#### app route "Patient_reg_submit":
- receives all the information from the "patient_register" page
- Checks if username already exists or not using the patient_exists
- If not Stores all the information to the database using the add_patient function
- Else returns the "Patient_register_userexist"

#### app route "patient_logout":
- removes the sessions id
- redirect to the home page

#### app route "doctor_login":
- returns the doctor login page using the render template function

#### app route "doctor_login_error":
- returns an error message if the username or password is wrong

#### app route "doctor_login_submit":
- Once the doctor presses submit in the login page, the user name and password is verified
- If it is valid, the Doctor portal is open, Creates a session for the doctor
- Else the doctor login error app route is triggered

#### app route "doctor_logout":
- removes the sessions id
- redirect to the home page

#### app route "PatientPortal":
- receives the user details from the patient_login_submit and returns the patient portal page along with the user_details

#### app route "/patient-doctor-dashboard/<doctor_id>"
- receives the doctor_id from the Doctor_list page
- Calls the get_doctor_schedule using the doctor_id
- Renders the patient-doctor-dashboard.html and sends the schedule to the html file

#### app route "DoctorList":
- triggered when patient clicks request an appointment
- renders the Doctor list page using the render_template function

#### app route "Doctor_portal":
- gets the schedule of the doctor using the get_doctor_schedule
- renders the doctor-dashboard page along sending the schedule of the doctor

#### app route "/patient_appt/<appt>":
- Receives the day and time of the appointment using the appt variable
- Receives the patient details using the patient id from the sessions and calls the book appointment function
- redirect backs to the PatientPortal

#### app route "doctor_appt_view/<appt>":
- receives the day and time using the appt variable
- receives the schedule using the doctor id
- receives the patient who booked the appointment using the get_patient
- extracts the user_details and renders the doctor appointment view page using the user_details 

#### app route "/appt_submit/<day_time>":
- receives all the patient vitals from the doctor appointment view page
- stores it in the database using the update appointment function
- redicrects to the doctor_portal page

#### app route "/medical_history_record/<appt_pat_id>":
- receives the patient id, day and time using the appt_pat_id variable
- gets all the appointments using the get_all_appointments using the patient id
- renders the medical history record which takes in the day, time and appointments list

## Mongo Client
#### Patient Login/Register:
- patient_exists to check if the user with the given username exists
- add_patient to register user
- patient_login to authenticate user
- applied fernet class from cryptography module for authentication security
- tests for CRUD operations located under the function in commented try-except

#### Doctor Login/Register:
- doctor_exists to check if the doctor with the given username exists
- NO REGISTER: Since it is assumed that the doctor is already in the hospital network
- doctor_login to authenticate doctor
- applied fernet class from cryptography module for authentication security
- tests for CRUD operations located under the function in commented try-except

#### Schedule CRUD: 
- Create schedule
- get_doctor_schedule by DoctorID
- update_schedule
- tests for CRUD operations located under the function in commented try-except

#### Appointments CRUD:
- book_appointment with doctor_id, patient_id, day, hour, reason
    - Add appointment to doctor schedule
    - create_appointment
        - add appointment to the appointments table, partial information
- get_appointment with doctor_id, day, hour
- update_appointment
    - During the visit, doctor can update the appointments table with:
        - Blood pressure
        - Beats per minute
        - Oxygen Saturation
        - Doctor Notes
- get_all_appointments with patient_id
    - Patient's history of appointments with all information in the form of a list of objects for all the visits regardless of the doctor, iterable and unwrappable with a for loop
- tests for CRUD operations located under the function in the commented try-except

### DataBase Structure:
- MainDB:
    - doctors collection
        - Document
            - DoctorID
            - username
            - name
            - password
            - key
            - email
            - Specialty
    - patients collection
        - Document
            - PatientID
            - username
            - name
            - password
            - key
            - history
            - allergies
    - schedule collection
        - Document
            - DoctorID
            - Monday
                - "8-9": "PatientID"
                - "9-10": "PatientID"
                - ...
            - Tuesday
                - ...
            - Wednesday
                - ...
            - Thursday
                - ...
            - Friday
                - ...
    - appointments collection
        - Document
            - DoctorID
            - PatientID
            - Day
            - Time
            - Reason
            - BP
            - BPM
            - OxySat
            - DocNotes


- Purely a testing update