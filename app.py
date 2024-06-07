import logging
from flask import Flask, redirect, render_template, session, url_for, request, send_from_directory, jsonify
from flask_socketio import SocketIO, join_room, leave_room
from pymongo import MongoClient
from flask_session import Session
from flask_pymongo import PyMongo
import base64
from requests import post, get
from song import *
from os import environ as env
from dotenv import find_dotenv, load_dotenv
import json
from urllib.parse import urlencode
from urllib.parse import quote
from download_song import *
from spotify_songs import *
from db_song import *
from change_streams import *
import threading
import queue


ENV_FILE = find_dotenv()

if ENV_FILE:
    load_dotenv(ENV_FILE)

app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
socketio = SocketIO(app, async_mode='threading', logger=True, engineio_logger=True)

logging.basicConfig(level=logging.DEBUG)

redirect_url = 'http://localhost:5000/account'
# song1 = Song('Leo Ordinary Person')
# download_song(song1)

@app.route("/")
def home():
    session.clear()
    print('from /:', session.get('session_name'))
    print('from /:', session.get('username'))
    return render_template("choose_host_or_user.html")

@app.route("/create-session", methods=['GET', 'POST'])
def generate_session():
    name = request.get_json()['session_name_input']
    session_name = create_session(name, request.get_json()['audio_type'])
    # print("Session Name is: ", session_name)
    session['session_name'] = session_name #flask session is storing panix session name
    return json.dumps(session_name)

@app.route("/home")
def send_html_files():
    return render_template("/home.html", session_name=session.get("session_name"))

@app.route("/greeting-user")
def send_user_songs_page():
    data = {'user': session['username'], 'session':session['session_name']}
    return render_template("/greeting-user.html", data=data)

@app.route("/html/<page>")
def send_static_pages(page):
    return render_template(("/", page))

@app.route("/connect-user-to-session", methods=['GET', 'POST'])
def connect_user_to_session():
    username = request.get_json()['username_input']
    session_name = request.get_json()['session_name_input']
    print('Data recieved from user connect form: username is: ', username, ' session name is: ', session_name)
    connection_info = connect_to_session(session_name, username)
    if connection_info['connected'] == False:
        return json.dumps('ERROR1234567891011')
    else:
        session['username'] = connection_info['username']
        session['session_name'] = session_name
        print('Saved cookie session connect user ' , session['username'] , ' to ' , session['session_name'])
        return json.dumps(connection_info['username'])

#TODO: make sure send becon works    
@app.route("/user-exits")
def user_exits():
    print("user called the user-exit")
    delete_user(session['username'])
    session.clear()

@app.route('/get-spotify-auth-url')
def get_spotify_auth_url():
    # makes sure to remove the access_token from before if the user had one
    print('spotify authenticate user ' , session['username'] , ' to ' , session['session_name'])
    if 'access_token' in session:
        session['access_token'] = None
    print('/get-spotify-auth-url session name: ', session['session_name'], ' username: ', session['username'])
    data = "https://accounts.spotify.com/authorize?client_id=" + env.get("CLIENT_ID") + "&response_type=code&redirect_uri=" + quote(redirect_url, safe='') +  "&scope=user-read-playback-state+user-modify-playback-state"
    return json.dumps(data)

@app.route('/account')
def get_spotify_auth_code():
    if 'username' in session:
        print('account username ' , session['username'])
    else:
        print('account username none')

    if 'session_name' in session:
        print('account session name ' , session['session_name'])
        args = request.args
        if 'code' in args and args['code'] != None:
            print(args['code'])
            #request token
            print('session name from /account ', session['session_name'])
            session['spotify_auth_code'] = args['code']
            print('auth code: ', args['code'])
            data= {'session_name': session.get('session_name'), 'username':session.get('username')}
            print(session['session_name'])
            return render_template('/account.html', data=data)
        else: 
            print("There was no code in args")
    else:
        print('account session name none')
    

    # elif 'access_token' in args and args['access_token'] != None:
    #     print('workinge')
    # else:
    #     print('Error no code or acess token- due to refresh')
        return render_template('/account.html', data='Error occured')

#TODO: refreshing tokens
@app.route('/add-spotify-songs-to-Queue', methods=['GET', 'POST'])
def add_spotify_songs_to_queue():
    num_of_songs = int(request.get_json())
    print('number of songs: ', num_of_songs)
    if 'access_token' not in session or session['access_token'] is None:
        print('spotify auth code: ' , session.get('spotify_auth_code'))
        session['access_token'] = get_spotify_token(session.get('spotify_auth_code'), redirect_url)
    print("access token: " + session['access_token'])
    songs = get_spotify_queue(session['access_token'])
    if num_of_songs is None:
        num_of_songs = 1
    if songs != 'Error: no songs selected':
        db_append_songs(session.get('username'), session.get('session_name'), songs[0:num_of_songs])
        download_thread = threading.Thread(download_songs, args=(songs[0:num_of_songs]))
        download_thread.start()
        return jsonify(json.dumps(songs[0:num_of_songs]))
    else:
        return jsonify('Error: no songs selected') 

@app.route("/get-session-name")
def send_session_name():
    return jsonify(session.get("session_name"))

@app.route("/get-username")
def send_username():
    return jsonify(session.get("username"))

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = str(data['session_name'])
    join_room(room)
    socketio.emit('logs', username + ' has joined session', to=room)

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['session_name']
    leave_room(room)
    socketio.emit('logs', username + ' has left session', to=room)


# try namespaces    
# try redis/kafka
def update_realtime_playlist(sessionName, playlist):
    print('update_realtime_playlist executed: ', sessionName)
    # realtime_playlist = json.dumps(playlist)
    socketio.emit('update', json.dumps(playlist), to=sessionName)
    print('should emit update ', type(playlist))

def handle_queue(queue):
    prev = None
    while True:
        session_name, playlist = queue.get()
        if not prev:
            prev = tuple((session_name, playlist))
        elif tuple((session_name, playlist)) == prev:
            continue
        else:
            prev = tuple((session_name, playlist))
            
        if session_name and playlist:
            print(' going to execute update_realtime_playlist')
            update_realtime_playlist(session_name, playlist)


if __name__ == '__main__':

    change_streams_queue = queue.Queue()

    change_streams_thread = threading.Thread(target=start_change_streams, args=(change_streams_queue, ))
    change_streams_thread.start()

    queue_handler_thread = threading.Thread(target=handle_queue, args=(change_streams_queue, ))
    queue_handler_thread.start()


    socketio.run(app, debug=True)

    change_streams_thread.join()
    queue_handler_thread.join()
