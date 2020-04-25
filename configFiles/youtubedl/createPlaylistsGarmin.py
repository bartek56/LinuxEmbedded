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


    if fileNames.count > 5:
        textFile="#EXTM3U\n"
        for fileName in fileNames:
            fileNameWithPath="%s/%s"%(dirName, fileName)
            fileNameWithFullPath="%s/%s"%(path, fileName)
            audio = MP3(fileNameWithFullPath)
            time = int(round(audio.info.length))
            songName = fileName.replace(".mp3","")
            textFile+="#EXTINF:%s,%s\n"%(time,songName)
            textFile+="%s\n"%(fileNameWithPath)
            textFile+="\n"
    
        playlistFile = "%s.m3u"%(dirName)
        f = codecs.open(playlistFile,"w+","utf-8")
        f.write(textFile)
        f.close()

def createPlaylists():
    dirName = os.path.abspath(os.getcwd())
    folders = [f for f in os.listdir(dirName) if os.path.isdir(os.path.join(dirName, f))]
    for i in folders:
        createPlaylist(i)

def createPlaylistForGarmin(folders, listName):
    PATH=os.path.abspath(os.getcwd())
    
    textFile="#EXTM3U\n"

    for folder in folders:
        path="%s/%s"%(PATH,folder)
        fileNames = [f for f in os.listdir(path) if f.endswith('.mp3')]

        for fileName in fileNames:
            fileNameWithPath="%s/%s"%(folder, fileName)
            fileNameWithFullPath="%s/%s"%(path, fileName)
            audio = MP3(fileNameWithFullPath)
            time = int(round(audio.info.length))
            songName = fileName.replace(".mp3","")
            textFile+="#EXTINF:%s,%s\n"%(time,songName)
            textFile+="%s\n"%(fileNameWithPath)
            textFile+="\n"
 
    playlistFile = "%s.m3u"%(listName)
    f = codecs.open(playlistFile,"w+","utf-8")
    f.write(textFile)
    f.close()

def main():

   createPlaylists()
   
   folders=list()
   folders.append("Bachata")
   folders.append("Kizomba")
   folders.append("Semba")
   createPlaylistForGarmin(folders,"taniec")
   
   folders=list()
   folders.append("imprezka")
   folders.append("techno")
   createPlaylistForGarmin(folders,"trening")

   folders=list()
   folders.append("relaks")
   folders.append("chillout")
   folders.append("spokojne-sad")
   createPlaylistForGarmin(folders,"praca")

if __name__ == '__main__':
    main()
