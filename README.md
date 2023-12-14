# Patient Tracker System Backend
UMass CS520 Fall 2023 Project

## Flask app

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