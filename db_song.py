from os import environ as env
from pymongo import MongoClient
from dotenv import find_dotenv, load_dotenv
import json
import random
import copy
from decimal import Decimal

ENV_FILE = find_dotenv()

if ENV_FILE:
    load_dotenv(ENV_FILE)


cluster = env.get("MONGODB_CLUSTER")
client = MongoClient(cluster)
db = client['PanixDB']
usersDB = db['Users']
songsDB = db['Songs']
sessionsDB = db['Sessions'] 

# returns session name
def create_session(session_name='', audio_type='ogg'):
    if session_name != None and sessionsDB.find_one({'sessionName': str(session_name)}) is None:
        sessionsDB.insert_one({'sessionName': session_name, 'songNo': 0.0, 'audio_type': str(audio_type)})
    else:
        session_name = random.randrange(10000, 99999)
        while sessionsDB.find_one({'session_name': str(session_name)}) != None:
            session_name+= 1
        sessionsDB.insert_one({'sessionName': session_name, 'songNo': 0.0})
    return session_name

# returns username and true or false if it connected
def connect_to_session(session_name, username=''):
    if sessionsDB.find_one({'sessionName': str(session_name)}) != None:
        if username == None or usersDB.find_one({'username': str(username), 'sessionName': str(session_name)}) != None:
            username = random.randrange(10000, 99999)
            while usersDB.find_one({'username': str(username)}) != None:
                username+= 1
        usersDB.insert_one({'sessionName': session_name, 'username': username})
        return {'username': username, 'connected': True}
    else:
        print('Error incorrect entered username: ', username, ' entered sessionName: ', session_name)
        return {'username': username, 'connected': False}

def delete_user(username):
    song_info = songsDB.delete_many({'username': username})
    user_info = usersDB.delete_many({'username': username})
    print(song_info.deleted_count, ' songs deleted')
    print(user_info.deleted_count, ' documents deleted')


def delete_session(session_name):
    song_info = songsDB.delete_many({'sessionName': session_name})
    user_info = usersDB.delete_many({'sessionName': session_name})
    session_info = sessionsDB.delete_many({'sessionName' : session_name})
    print(song_info.deleted_count, ' songs deleted')
    print(user_info.deleted_count, ' user deleted')
    print(session_info.deleted_count, ' session info deleted')

def get_audio_type(session_name):
    query_result = sessionsDB.find_one({'sessionName': str(session_name)}, {"_id": 0 ,"audio_type": 1}).get("audio_type") 
    return query_result



def db_append_songs(username, session_name, songs):
    song_no = sessionsDB.find_one({'sessionName': str(session_name)})['songNo']
    songs = copy.deepcopy(songs)
    for song in songs:
        song_no = song_no + 1
        song['songNo'] = song_no
        song['username'] = username
        song['sessionName'] = session_name
    songsDB.insert_many(songs)
    query = {'sessionName': str(session_name)}
    update = {'$set' : {'songNo': song_no}}
    sessionsDB.update_one(query, update)

def get_db_songs(session_name):
    songs = songsDB.find({'sessionName': session_name}).sort('orderNo', 1)
    return songs
    

    

