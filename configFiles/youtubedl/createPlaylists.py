from __future__ import unicode_literals
import sys
import os
import warnings
import codecs
from datetime import datetime
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def createPlaylist(dirName):
    PATH = os.path.abspath(os.getcwd())
    path = "%s/%s"%(PATH,dirName)
    fileNames = [f for f in os.listdir(path) if f.endswith('.mp3')]

    textFile="#EXTM3U\n"
    for fileName in fileNames:
        fileNameWithPath="%s/%s"%(path, fileName)
        audio = MP3(fileNameWithPath)
        time = int(round(audio.info.length))
        songName = fileName.replace(".mp3","")
        textFile+="#EXTINF:%s,%s\n"%(time,songName)
        textFile+="%s\n"%(fileNameWithPath)
        textFile+="\n"
    
    if not os.path.exists('playlists'):
            os.makedirs('playlists')
    playlistFile = "playlists/%s.m3u"%(dirName)
    f = codecs.open(playlistFile,"w+","utf-8")
    f.write(textFile)
    f.close()

def createPlaylists():
    dirName = os.path.abspath(os.getcwd())
    folders = [f for f in os.listdir(dirName) if os.path.isdir(os.path.join(dirName, f))]
    folders.remove("playlists")
    for i in folders:
        print i
        createPlaylist(i)

def main():
#   createPlaylist("polskie hity")
   createPlaylists()

if __name__ == '__main__':
    main()
