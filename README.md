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