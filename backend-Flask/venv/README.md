# Patient Tracker System Backend
UMass CS520 Fall 2023 Project

## Flask app

## Mongo Client
Patient Login/Register:
- patient_exists to check if the user with the given username exists
- add_patient to register user
- patient_login to authenticate user
- applied fernet class from cryptography module for authentication security

Doctor Login/Register:
- doctor_exists to check if the doctor with the given username exists
- NO REGISTER: Since it is assumed that the doctor is already in the hospital network
- doctor_login to authenticate doctor
- applied fernet class from cryptography module for authentication security

Schedule CRUD: 
- Create schedule
- get_schedule by DoctorID
DataBase:
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