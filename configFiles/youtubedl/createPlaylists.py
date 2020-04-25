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

#PATH='/tmp/muzyka/Youtube list/'
#PATH='/mnt/TOSHIBA EXT/muzyka/Youtube list/'
#PATH='/media/shareTV/share/music/Youtube list'


def createPlaylist(dirName):
    PATH = os.path.abspath(os.getcwd())
    path = "%s/%s"%(PATH,dirName)
    fileNames = [f for f in os.listdir(path) if f.endswith('.mp3')]
    if fileNames > 5:
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
        print i
        createPlaylist(i)

def main():
   songsCounter = 0
   now = datetime.now()
   dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
   print("---------  " + dt_string + "  ---------") 

   createPlaylists()
   now = datetime.now()
   dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
   print("---------  " + dt_string + "  ---------") 
   summary = "[SUMMARY] downloaded  %s songs"%(songsCounter)
   print bcolors.OKGREEN + summary + bcolors.ENDC

if __name__ == '__main__':
    main()
