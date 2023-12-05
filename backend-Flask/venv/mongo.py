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
def patient_exists(username):
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client['test']
    collection = db['users']
    
    if collection.find_one({"username": username}) is not None:
        return True
    return False

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
# returns -> {ObjectID, username, password, email, DOB, history, allergies}
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
    
### Doctor CRUD
# doctor_exits -> check if doctor exists
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
# returns -> {DoctorID, username, name, password, email, specialization}
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