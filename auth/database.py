from pymongo import MongoClient
from pymongo.server_api import ServerApi
import certifi

uri = "mongodb+srv://adminusername:adminpassword@cluster0.6l4r7.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'),tlsCAFile = certifi.where())

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
    db=client["Test"]
    collection=db["user"]
    otp_collection=db["otp"]
except Exception as e:
    print(e)