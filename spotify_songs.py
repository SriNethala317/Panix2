from dotenv import find_dotenv, load_dotenv
from os import environ as env
from requests import post, get
import base64
import json
from urllib.parse import quote
import requests

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

client_id = env.get('CLIENT_ID')
client_secret = env.get('CLIENT_SECRET')

def get_spotify_token(code, redirect_url):
    url = "https://accounts.spotify.com/api/token"
    auth_string = env.get("CLIENT_ID") + ':' + env.get("CLIENT_SECRET")
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')
    headers = {
    "Authorization": "Basic " + auth_base64,
    "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {'code':code, 'redirect_uri': redirect_url, 'grant_type': "authorization_code"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    print("json_results: ",  json_result)
    token = json_result["access_token"]
    return token


def get_auth_header(token):
    return {"Authorization" : "Bearer " + token}

def put_songs_in_list(json_result):
    songs = []
    #can get the user queue by having the original queue and then having another list where you add a song to the end of the queue in that list and you compare both lists
    current_song_info = json_result["currently_playing"] 
    songs.append({'artist_name': current_song_info['artists'][0]['name'], 'song_name': current_song_info['name'], 'image_url': current_song_info['album']['images'][0]['url']})
    for song_info in json_result["queue"]:
        song = {'artist_name': song_info['artists'][0]['name'], 'song_name': song_info['name'], 'image_url': song_info['album']['images'][0]['url']}
        # songs.append(song['song_name'])
        songs.append(song)
    
    return songs

    
#TODO: add error handling to the get, put, and post calls
def get_spotify_queue(token):
    url = "https://api.spotify.com/v1/me/player/queue"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    songs = []
    error_msg = 'Error: no songs selected'
    #if there isn't a "currently_playing" then there was an issue with geting the result
    if "currently_playing" not in json_result:
        print('Error: currently_playing is not in results')
        return error_msg
    #indicates that the user hasn't started playing their music in a long time so it appears to be null so we play and pause to recheck
    #TODO: Fix the issue of it showing up as None untill the spotify playlist is acted 
    elif json_result["currently_playing"] is None:
        print('currently_playing is null')
        print('json_results: ',  json_result)
        #play the queue
        header_with_context_type = get_auth_header(token)
        header_with_context_type['Content-Type'] = 'application/json'
        requests.put('https://api.spotify.com/v1/me/player/play', headers=header_with_context_type, data={"position_ms": '0'})
        #sets the volume to 0
        requests.put('https://api.spotify.com/v1/me/player/volume', headers=headers, data={'volume_percent':'0'})

        #pause the queue
        requests.put('https://api.spotify.com/v1/me/player/pause', headers=headers)
        
        # re do the request to get the queue
        result = get(url, headers=headers)
        json_result = json.loads(result.content)
        #if the queue is still none then inform the users
        if json_result["currently_playing"] is None:
            return error_msg;

    songs = put_songs_in_list(json_result)
    print('spotify songs: ' , songs, ' len is: ', len(songs))
    return songs

    
