from os import environ as env
from dotenv import find_dotenv, load_dotenv
from pymongo import MongoClient
import pymongo
from bson.json_util import dumps
import sys
import queue

ENV_FILE = find_dotenv()

if ENV_FILE:
    load_dotenv(ENV_FILE)

cluster = env.get("MONGODB_CLUSTER")
client = MongoClient(cluster)
db = client['PanixDB']
songsDB = db['Songs']

def start_change_streams(queue):
    resume_token = None
    pipeline = [{'$match': {'operationType': {'$in':['insert', 'update']}}}]
    while True:
        try:
            print('change stream loaded- waing for changes')
            with songsDB.watch(pipeline) as changeStream:
                for change in changeStream:
                    sessionName = change.get('fullDocument').get('sessionName')
                    songs = songsDB.find({'sessionName': sessionName}, {'_id': 0}).sort('orderNo', 1) # retrieves all the songs as Pymongo cursor and indicates not to return obj id
                    queue.put((sessionName, list(songs)))
                    resume_token = changeStream.resume_token
        except pymongo.errors.PyMongoError:
            if resume_token is None:
                sys.exit(1)
        finally:
            client.close()


