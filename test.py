from os import environ as env
from pymongo import MongoClient
from dotenv import find_dotenv, load_dotenv

ENV_FILE = find_dotenv()

if ENV_FILE:
    load_dotenv(ENV_FILE)

cluster = env.get("MONGODB_CLUSTER")
client = MongoClient(cluster)
db = client['PanixDB']
songsDB = db['Songs']

songsDB.insert_one({'userName': 'Sri', 'song': {'songName': 'why dis kolevari'}, 'sessionName' : 'kkk', 'orderNo': 1})
# songsDB.update_many({'songName': 'checking123'},  {"$set": {'works': 'no'}})
print(songsDB.find_one({'songName': 'checking123'}))