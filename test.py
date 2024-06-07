# from os import environ as env
# from pymongo import MongoClient
# from dotenv import find_dotenv, load_dotenv

# ENV_FILE = find_dotenv()

# if ENV_FILE:
#     load_dotenv(ENV_FILE)

# cluster = env.get("MONGODB_CLUSTER")
# client = MongoClient(cluster)
# db = client['PanixDB']
# songsDB = db['Songs']

# songsDB.insert_one({'userName': 'Sri', 'song': {'songName': 'why dis kolevari'}, 'sessionName' : 'kkk', 'orderNo': 1})
# # songsDB.update_many({'songName': 'checking123'},  {"$set": {'works': 'no'}})
# print(songsDB.find_one({'songName': 'checking123'}))

hashset = {'_id': {'_data': '8266568995000000082B042C0100296E5A100441357D193CAC4C8EAB0E6DE14893BECE463C6F7065726174696F6E54797065003C696E736572740046646F63756D656E744B65790046645F6964006466568994CD80B57FC597E1A4000004'}, 
           'operationType': 'insert', 'clusterTime': 'Timestamp(1716947349, 8)', 'wallTime': 'datetime.datetime(2024, 5, 29, 1, 49, 9, 227000)', 
           'fullDocument': {'_id': 'ObjectId(66568994cd80b57fc597e1a4)', 'artist_name': 'OFFICIAL HIGE DANDISM', 'song_name': 'Cry Baby', 
            'image_url': 'https://i.scdn.co/image/ab67616d0000b273bbf9d502f3ce4a15b3c43f7a', 'songNo': 7.0, 'username': 'jip', 'sessionName': 'jill'}, 
            'ns': {'db': 'PanixDB', 'coll': 'Songs'}, 
            'documentKey': {'_id': 'ObjectId(66568994cd80b57fc597e1a4)'}}

print(hashset['fullDocument']['sessionName'])