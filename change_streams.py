from os import environ as env
from dotenv import find_dotenv, load_dotenv
from pymongo import MongoClient
import pymongo
from bson.json_util import dumps
import sys
from app import update_realtime_playlist

ENV_FILE = find_dotenv()

if ENV_FILE:
    load_dotenv(ENV_FILE)

cluster = env.get("MONGODB_CLUSTER")
client = MongoClient(cluster)
db = client['PanixDB']
songsDB = db['Songs']

try:
    resume_token = None
    pipeline = [{'$match': {'operationType': {'$in':['insert', 'update']}}}]
    with songsDB.watch(pipeline) as changeStream:
        for change in changeStream:
            # print(dumps(change))
            # print("document key is: " , change['documentKey'])
            # print("Session Name is ", songsDB.find_one(change['documentKey'])['sessionName'])
            sessionName = songsDB.find_one(change['documentKey'])['sessionName']
            songs = songsDB.find({'sessionName': sessionName}).sort('orderNo', 1)
            
            update_realtime_playlist(sessionName, songs)
            resume_token = changeStream.resume_token
except pymongo.errors.PyMongoError:
    if resume_token is None:
        sys.exit(1)
    else:
        with songsDB.watch(pipeline, resume_after=resume_token) as changeStream:
            for change in changeStream:
                print(dumps(change))
finally:
    client.close()
