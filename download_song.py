from pytube import YouTube
import os
import re
import urllib.request
import urllib.parse
import shutil
from multiprocessing.pool import ThreadPool
from moviepy.editor import *


SONGSFOLDER = "song_downloads"

if os.path.exists(SONGSFOLDER):
    shutil.rmtree(SONGSFOLDER)
os.mkdir(SONGSFOLDER)

def get_url(song_name, artist):
    keyword = song_name.replace(" ", "+")
    if artist != None:
        keyword+= "+by+" + artist.replace(" ", "+")

    html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + keyword) #can look at meta data and see if it displays the length of the video and check that with information given by user
    vid_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    url = "https://www.youtube.com/watch?v=" + vid_ids[0]
    return url

def download_audio_from_yt(url, song, audio_type, filename):
    yt = YouTube(url)
    song['length'] = yt.length;
    video = yt.streams.filter(only_audio=True, file_extension='mp4').first()
    path = os.path.join(os.getcwd(), SONGSFOLDER, '')
    print(path)
    # download video from youtube
    audio_file = video.download(output_path= path , filename=filename + '.mp4')

    # Load the mp4 file
    video = AudioFileClip(os.path.join(path, filename + '.mp4'))

    # Convert from mp4 to mp3 or ogg 
    video.write_audiofile(os.path.join(path, filename + '.'+ audio_type), logger=None)

    # remove mp4 file
    os.remove(os.path.join(path, filename + '.mp4'))
    

def download_song(song, audio_type='ogg'):
    try:
        artist = song.get('artist_name')
        if artist:
            artist = '_by_' + artist
        else:
            artist = ''
        possible_file = song.get('song_name').replace(" ", "_") + artist.replace(" ", "_") +'.' + audio_type
        if os.path.exists(os.path.join(os.getcwd(), SONGSFOLDER, possible_file)): #if file already exists then return
            return
        url = get_url(song.get('song_name'), song.get('artist_name'))
        print('url: ', url)
        download_audio_from_yt(url, song, audio_type, possible_file[:-4])
        print('Song name is: ' + song.get('song_name'))
    except Exception as e:
        print(f"Failed to download {song.get('song_name')}: {e}")

def download_songs(songs, audio_type):
    pool = ThreadPool(10)
    for song in songs:
        pool.apply_async(download_song, args=(song, audio_type))
    
    pool.close()
    pool.join()
        
