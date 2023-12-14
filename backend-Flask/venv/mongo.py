from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
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
        print(passw,fernet.decrypt(user['password']).decode())
        if passw != fernet.decrypt(user['password']).decode():
            return False
        return user
    except Exception as e:
        print(e)
        return False

# try:
#     id = patient_login("padhiyaman", "12345")
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
    
# try:
#     id = get_patient("darshuser")
#     print(id)
# except Exception as e:
#     print(e)
    
# update_patient_password -> update patient password
# type signature -> update_patient_password(username: str, old_password: str, new_password: str) -> bool
# test in app
def update_patient_password(username, old_password, new_password):
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client['test']
    collection = db['users']
    
    try:
        user = collection.find_one({"username": username})
        key = user['hash_key']
        fernet = Fernet(key)
        if old_password != fernet.decrypt(user['password']).decode():
            return False
        key = fernet.generate_key()
        fernet = Fernet(key)
        user['hash_key'] = key
        user['password'] = fernet.encrypt(new_password.encode())
        collection.update_one({"username": username}, {"$set": user})
        return True
    except Exception as e:
        print(e)
        return False

# try:
#     id = update_patient_password("darshuser", "Darshpass", "Darshpass")
#     print(id)
# except Exception as e:
#     print(e)

# update_patient_info -> update patient info
# type signature -> update_patient_info(username: str, name: str, email: str, DOB: str, history: str, allergies: str) -> bool
# test in app
def update_patient_info(username, name, email, DOB, history, allergies):
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client['test']
    collection = db['users']
    
    try:
        if not patient_exists(username):
            return False
        user = collection.find_one({"username": username})
        user['name'] = name if name != "" else user['name']
        user['email'] = email if email != "" else user['email']
        user['DOB'] = DOB if DOB != "" else user['DOB']
        user['history'] = history if history != "" else user['history']
        user['allergies'] = allergies if allergies != "" else user['allergies']
        collection.update_one({"username": username}, {"$set": user})
        return True
    except Exception as e:
        print(e)
        return False

# try: 
#     id = update_patient_info("darshuser", "Darsh G", "dgondalia@umass.edu", "01-02-2001", "", "")
#     print(id)
# except Exception as e:
#     print(e)
    
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
    
# try:
#     print(get_doctor_schedule(1))
# except Exception as e:
#     print(e)

# update_schedule -> update schedule for a doctor
# type signature -> update_schedule(dict(str(DoctorID): int, schedule: dict(str(days): dict(str(time_slots): str))) -> bool
def update_schedule(schedule):
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client['test']
    collection = db['schedule']
    print(schedule, "input schedule")
    # schedule = {"DoctorID": ..., "Schedule": {"Monday": {"8-9": ..., "9-10": ..., ...}, "Tuesday": {...}, ...}}
    try: 
        current_schedule = collection.find_one({"DoctorID": schedule['DoctorID']})
        print(current_schedule, "current schedule")
        for day in schedule['Schedule']:
            for hour in schedule['Schedule'][day]:
                current_schedule[day][hour] = schedule['Schedule'][day][hour]
        print(current_schedule, "updated schedule")
        collection.update_one({"DoctorID": schedule['DoctorID']}, {"$set": current_schedule})
        return True
    except Exception as e:
        print(e)
        return False
    
# try:
#     testschedule = {
#         "DoctorID": 1, 
#         "Schedule": {
#             "Monday": {
#                 "8-9": "darshuser",
#                 "9-10": "padhiyaman", 
#                 "10-11": "dgondalia", 
#                 "11-12": "darshuser", 
#                 "12-13": "padhiyaman", 
#                 "13-14": "dgondalia", 
#                 "14-15": "darshuser", 
#                 "15-16": "padhiyaman", 
#                 "16-17": "dgondalia", 
#                 "17-18": "darshuser"}, 
#             "Tuesday": {
#                 "8-9": "padhiyaman", 
#                 "9-10": "dgondalia",
#                 "10-11": "darshuser",
#                 "11-12": "padhiyaman",
#                 "12-13": "dgondalia",
#                 "13-14": "darshuser",
#                 "14-15": "padhiyaman",
#                 "15-16": "dgondalia",
#                 "16-17": "darshuser",
#                 "17-18": "padhiyaman"}, 
#             "Wednesday": {
#                 "8-9": "dgondalia",
#                 "9-10": "darshuser",
#                 "10-11": "padhiyaman",
#                 "11-12": "dgondalia",
#                 "12-13": "darshuser",
#                 "13-14": "padhiyaman",
#                 "14-15": "dgondalia",
#                 "15-16": "darshuser",
#                 "16-17": "padhiyaman",
#                 "17-18": "dgondalia"},
#             "Thursday": {
#                 "8-9": "darshuser",
#                 "9-10": "padhiyaman",
#                 "10-11": "dgondalia", 
#                 "11-12": "darshuser",
#                 "12-13": "padhiyaman",
#                 "13-14": "dgondalia",
#                 "14-15": "darshuser",
#                 "15-16": "padhiyaman", 
#                 "16-17": "dgondalia", 
#                 "17-18": "darshuser"},
#             "Friday": {
#                 "8-9": "padhiyaman",
#                 "9-10": "dgondalia",
#                 "10-11": "darshuser",
#                 "11-12": "padhiyaman", 
#                 "12-13": "dgondalia",
#                 "13-14": "darshuser",
#                 "14-15": "padhiyaman", 
#                 "15-16": "dgondalia",
#                 "16-17": "darshuser",
#                 "17-18": "padhiyaman"
#                 }
#             }
#         }
#     print(update_schedule(testschedule), "testing update_schedule")
#     print(get_doctor_schedule(1), "\n ,get_doctor_schedule(1)")
# except Exception as e:
#     print(e)


# APPOINTMENTS CRUD

# patient books an appointment
# type signature -> book_appointment(doctor_id: int, patient_id: str, day: str, hour: str, reason: str) -> bool
def book_appointment(doctor_id, patient_id, day, hour, reason):
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client['test']
    collection = db['schedule']
    
    try:
        schedule = collection.find_one({"DoctorID": doctor_id})
        print(schedule)
        if schedule[day][hour] != "":
            return False
        
        if not create_appointment(doctor_id, patient_id, day, hour, reason):
            return False
        
        schedule[day][hour] = patient_id
        collection.update_one({"DoctorID": doctor_id}, {"$set": schedule})
        return True
    except Exception as e:
        print(e)
        return False

# only used by book_appointment: STAY AWAY
# type signature -> create_appointment(doctor_id: int, patient_id: str, day: str, hour: str, reason: str) -> bool
def create_appointment(doctor_id, patient_id, day, hour, reason):
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client['test']
    collection = db['appointments']

    try:
        appointment = {
            "PatientID": patient_id, 
            "DoctorID": doctor_id, 
            "Day": day, 
            "Time": hour,
            "Reason": reason,
            "BP": "",
            "BPM": "",
            "OxySat": "",
            "DocNotes": ""
        }
        
        collection.insert_one(appointment)
        return True
    except Exception as e:
        print(e)
        return False


# Test for book_appointment and create_appointment
# try:
#     print(book_appointment(2, "darshuser", "Tuesday", "9-10", "Regular check up"))
# except Exception as e:
#     print(e)

# get all appointments for a doctor
# type signature -> get_appointments(doctor_id: int) -> list(dict(PatientID: int, DoctorID: int, Day: str, Time: str, Reason: str))
def get_appointment(doctor_id, day, hour):
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client['test']
    collection = db['schedule']
    
    try:
        doctor_schedule = collection.find_one({"DoctorID": doctor_id})
        # print(doctor_schedule)
        patient = doctor_schedule[day][hour]
        
        return patient
    except Exception as e:
        print(e)
        return None
        
# update_appointment -> update appointment info from the DOCTOR side
# Doctor clicks on appointment -> form to fill out BP, BPM, OxySat, DocNotes -> update_appointment
# type signature -> update_appointment(doctor_id: int, day: str, hour: str, bp: str, bpm: str, oxysat: str, docnotes: str) -> bool
def update_appointment(doctor_id, day, hour, bp="", bpm="", oxysat="", reasons="", docnotes=""):
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client['test']
    collection = db['appointments']
    
    try:
        patient = get_appointment(doctor_id, day, hour)
        print("update_appointment, got patient username: " + patient)
        appointment = collection.find_one({"DoctorID": doctor_id, "PatientID": patient, "Day": day, "Time": hour})
        print("Retriving the current appointment at update_appointment: ")
        print(appointment)
        appointment['BP'] = bp if appointment['BP'] == "" and bp != "" else ""
        appointment['BPM'] = bpm if appointment['BPM'] == "" and bpm != "" else ""
        appointment['OxySat'] = oxysat if appointment['OxySat'] == "" and oxysat != "" else ""
        appointment['DocNotes'] = docnotes if appointment['DocNotes'] == "" and docnotes != "" else ""
        appointment['Reason'] = reasons if appointment['Reason'] == "" and reasons != "" else ""
        print("Updated the current appointment at update_appointment: ")
        print(appointment)
        collection.update_one({"DoctorID": doctor_id, "PatientID": patient, "Day": day, "Time": hour}, {"$set": appointment})
        print("Updated successful!")
        return True
    except Exception as e:
        print(e)
        return False
    
# try:
#     print(update_appointment(2, "Tuesday", "9-10", "120/110", "55", "100"))
# except Exception as e:
#     print(e)

def get_all_appointments(patient_id):
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client['test']
    collection = db['appointments']
    
    try:
        appointments = collection.find({"PatientID": patient_id})
        return appointments
    except Exception as e:
        print(e)
        return None
    
# try: 
#     print(get_all_appointments("darshuser"))
# except Exception as e:
#     print(e)