from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import bcrypt
import json
from cryptography.fernet import Fernet
# Replace the placeholder with your Atlas connection string
uri = "mongodb+srv://super:superuser@atlascluster.j0uq5ga.mongodb.net/?retryWrites=true&w=majority"
# Set the Stable API version when creating a new client
# client = MongoClient(uri, server_api=ServerApi('1'))
                          
# # Send a ping to confirm a successful connection
# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)

# Patient CRUD
# patient_exists -> check if patient exists
# type signature -> patient_exists(username: str) -> bool
def patient_exists(username):
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client['test']
    collection = db['users']
    
    if collection.find_one({"username": username}) is not None:
        return True
    return False


# try:
#     print(patient_exists("darshuser"))
# except Exception as e:
#     print(e)

# add_patient -> add patient to database
# type signature -> add_patient(username: str, password: str, name: str, email: str, DOB: str, history: str, allergies: str) -> bool
def add_patient(username, password, name, email, DOB, history, allergies):
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client['test']
    collection = db['users']
    
    key = Fernet.generate_key()
    fernet = Fernet(key)

    
    num_documents = collection.count_documents({})
    user = {"PatientID": (num_documents+1),"username": username, "name":name, "password": fernet.encrypt(password.encode()), "hash_key": key, "email": email, "DOB": DOB, "history": history, "allergies": allergies}
    try:
        collection.insert_one(user)
    except Exception as e:
        print(e)
        return False
    return True

# try:
#     add_patient("darshuser", "Darshpass", "Darsh Gondalia", "dmillis@umass.edu", "12122012", "David", "__ tendencies")
# except Exception as e:
#     print(e)


# get_patient -> user object from mongo
# type signature -> get_patient(username: str) -> returns {ObjectID, username, password, email, DOB, history, allergies}
def patient_login(user, passw):
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client['test']
    collection = db['users']

    try:
        if not patient_exists(user):
            return False
        user = collection.find_one({"username": user})
        
        key = user['hash_key']
        fernet = Fernet(key)
        print(key)
        print(fernet.encrypt(passw.encode()))
        print(fernet.decrypt(user['password']).decode())
        
        if passw != fernet.decrypt(user['password']).decode():
            return False
        return user
    except Exception as e:
        print(e)
        return False

# try:
#     id = patient_login("darshuser", "Darshpass")
#     print(id)
# except Exception as e:
#     print(e)

# get_patient -> user object from mongo
# type signature -> get_patient(username: str) -> returns {ObjectID, username, password, email, DOB, history, allergies}
def get_patient(username):
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client['test']
    collection = db['users']
    
    try:
        if not patient_exists(username):
            return None
        user = collection.find_one({"username": username})
        return user
    except Exception as e:
        print(e)
        return None
    
# def update_patient(username, password, name, email, DOB, history, allergies):
#     client = MongoClient(uri, server_api=ServerApi('1'))
#     db = client['test']
#     collection = db['users']
    
#     key = Fernet.generate_key()
#     fernet = Fernet(key)
    
#     try:
#         if not patient_exists(username):
#             return False
#         user = collection.find_one({"username": username})
#         user['name'] = name
#         user['password'] = fernet.encrypt(password.encode())
#         user['hash_key'] = key
#         user['email'] = email
#         user['DOB'] = DOB
#         user['history'] = history
#         user['allergies'] = allergies
#         collection.update_one({"username": username}, {"$set": user})
#         return True
#     except Exception as e:
#         print(e)
#         return False

    
### Doctor CRUD
# doctor_exits -> check if doctor exists
# type signature -> doctor_exists(username: str) -> bool
def doctor_exists(username):
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client['test']
    collection = db['doctors']
    
    if collection.find_one({"username": username}) is not None:
        return True
    return False

#for testing purposes, adding doctors at random:
def doctor_register():
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client['test']
    collection = db['doctors']
    num_documents = collection.count_documents({})
    
    # Generate a random hash seed
    key = Fernet.generate_key()
    fernet = Fernet(key)
    
    doctor = [{"DoctorID": (1),"username": "hconboy", "name":"Dr. Heather Conboy", "password": fernet.encrypt("doctor11".encode()), "hash_key": key, "email": "hconboy@umass.edu", "specialization": "Neurology"},
              {"DoctorID": (2),"username": "dmanus", "name":"Dr. David McManus", "password": fernet.encrypt("doctor22".encode()), "hash_key": key, "email": "padhiyaman@umass.edu", "specialization": "Cardiology"},
              {"DoctorID": (3),"username": "hguan", "name":"Dr. Hui Guan", "password": fernet.encrypt("doctor33".encode()), "hash_key": key, "email": "hguan", "specialization": "Pediatrics"}
            ]

    for i in doctor:
        try:
            collection.insert_one(i)
        except Exception as e:
            print(e)
            return False
    return True
# Add doctors to database: uncomment the below try block
# try:
#     doctor_register()
# except Exception as e:
#     print(e)
    

# doctor_login -> get doctor object from mongo
# type signature -> doctor_login(username: str) -> returns {ObjectID, username, password, email, specialization}
def doctor_login(user, passw):
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client['test']
    collection = db['doctors']
    
    try:
        # collection.insert_one({"username": user, "password": hash(passw)})
        user = collection.find_one({"username": user})
        if user is None:
            return False
        key = user['hash_key']
        fernet = Fernet(key)
        print(key)
        print(fernet.encrypt(passw.encode()))
        print(fernet.decrypt(user['password']).decode())
        
        if passw != fernet.decrypt(user['password']).decode():
            return False
        return user
    except Exception as e:
        print(e)
        return False

# try:
#     id = doctor_login("hconboy", "doctor11")
#     print(id)
# except Exception as e:
#     print(e)

# SCHEDULE CRUD
# create_empty_schedule -> create empty schedule for all doctors when the new week begins
# type signature -> create_empty_schedule() -> bool
def create_empty_schedule():
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client['test']
    doctor_collection = db['doctors']
    collection = db['schedule']
    num_documents = collection.count_documents({})
    
    all_doctors = doctor_collection.find()
    doctor_id_list = []
    for doctor in all_doctors:
        doctor_id_list.append(doctor['DoctorID'])
    
    print(doctor_id_list)
    
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    work_hours = ["8-9", "9-10", "10-11", "11-12", "12-13", "13-14", "14-15", "15-16", "16-17", "17-18"]
    
    schedule = dict()
    
    for d in doctor_id_list:
        doctor_id = dict()
        doctor_id['DoctorID'] = d
        for day in days:
            doctor_id[day] = dict()
            for hour in work_hours:
                doctor_id[day][hour] = ""
        try:
            collection.insert_one(doctor_id)
        except Exception as e:
            print(e)
    return True
    

# print(create_empty_schedule())

# get_schedule -> get schedule for a doctor
# type signature -> update_schedule(doctor_id: int, day: str, hour: str, patient_id: int) -> 
# return dict('DoctorID': int, 'Schedule': dict(days: dict(hours: str)))
def get_doctor_schedule(doctor_id):
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client['test']
    collection = db['schedule']
    
    try:
        schedule = collection.find_one({"DoctorID": doctor_id})
        ret_dict = dict()
        ret_dict['DoctorID'] = schedule['DoctorID']
        ret_dict['Schedule'] = dict()
        
        for day in schedule:
            if day != 'DoctorID' and day != '_id':
                ret_dict['Schedule'][day] = schedule[day]
                
        return ret_dict
    except Exception as e:
        print(e)
        return None
    
# print(get_doctor_schedule(1))
