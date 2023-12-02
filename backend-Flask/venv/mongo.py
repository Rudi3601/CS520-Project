from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

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

def add_user(username, password, email, DOB, history, allergies):
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client['test']
    collection = db['users']
    count = object_count(db, client)
    user = {"PatientID": (count+1),"username": username, "password": hash(password), "email": email, "DOB": DOB, "history": history, "allergies": allergies}
    collection.insert_one(user)
    
def object_count(db, client):
    return db.client.count()
# try:
#     add_user("test", "test", "test", "test", "test", "test")
#     print("Added user successfully")
# except Exception as e:
#     print(e)

def get_user(user, passw):
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client['test']
    collection = db['users']
    user = collection.find_one({username: user, password: hash(passw)})
    return ""+user['_id']

try:
    id = get_user("test", "test")
    print(id)
except Exception as e:
    print(e)

def get_user(username):
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client['test']
    collection = db['users']
    user = collection.find_one({"username": username})
    return user