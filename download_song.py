from song import *
from pytube import YouTube
import os
import re
import urllib.request
import urllib.parse
import shutil


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

def download_audio(url, song):
    filename = song.get_name().replace(" ", "_") + '.mp3' 
    yt = YouTube(url)
    song.length = yt.length;
    video = yt.streams.filter(only_audio=True).first()
    path = os.getcwd() + "\\" + SONGSFOLDER + "\\"
    print(path)
    audio_file = video.download(output_path= '.')
    song.set_filename(filename)
    os.rename(audio_file, path + filename) 

def download_song(song):
    url = get_url(song.get_name(), song.get_artist())
    download_audio(url, song)
    print('File name is: ' + song.get_filename())
    print('Song name is: ' + song.get_name())
    return True

    