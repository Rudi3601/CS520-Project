from flask import Flask
from pymongo import MongoClient
import datetime
 
x = datetime.datetime.now()
 
# Initializing flask app
app = Flask(__name__)
 
#DB connection
client = MongoClient("mongodb+srv://super:xCtC5CJfyAWJyvCK@atlascluster.j0uq5ga.mongodb.net/")
 
# Route for seeing a data
@app.route('/data')
def get_time():
 
    # Returning an api for showing in  reactjs
    return {
        'Name':"geek", 
        "Age":"22",
        "Date":x, 
        "programming":"python"
        }
 
     
# Running app
if __name__ == '__main__':
    app.run(debug=True)