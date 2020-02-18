from __future__ import unicode_literals
import sys
import os
import warnings
from datetime import datetime
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3


#PATH='/tmp/muzyka/Youtube list/'


def convert_songname_on_metadata(songName):
    slots = songName.split(" - ")
    metadata ={ 'tracknumber': "1",}
    if len(slots) == 2:
      metadata['artist'] = slots[0]
      metadata['title'] = slots[1]
    elif len(slots) < 2:
      slots = songName.split("-")
      if len(slots) == 2:
        metadata['artist'] = slots[0]
        metadata['title'] = slots[1]
      else:
        metadata['title'] = songName
        metadata['artist'] = ""
    else:
      metadata['artist'] = slots[0]
      name=""
      i=0
      for slots2 in slots:
        if i > 0:
          if i > 1:
            name+="-"
          name+=slots[i]
        i=i+1  
      metadata['title'] = name

    return metadata

def add_metadata_manual(playlistName, trackNumber, musicPath, fileName):
    albumNamePart = "YT "
    albumName = "%s%s"%(albumNamePart, playlistName)
    path = "%s%s"%(musicPath, playlistName)
    songName=fileName.replace(".mp3", "")
    metadata = convert_songname_on_metadata(songName)
    fileNameWithPath = os.path.join(path, fileName)
    metatag = EasyID3(fileNameWithPath)
    metatag['tracknumber'] = str(trackNumber)
    metatag['album'] = albumName
    metatag['artist'] = metadata['artist']
    metatag['title'] = metadata['title']
    metatag.save()
    print "added metadata"
    print fileNameWithPath
    audio = MP3(fileNameWithPath, ID3=EasyID3)
    print audio.pprint()


def add_metadata_manual_without_number(playlistName, musicPath, fileName):
    albumNamePart = "YT "
    albumName = "%s%s"%(albumNamePart, playlistName)
    path = "%s%s"%(musicPath, playlistName)
    songName=fileName.replace(".mp3", "")
    metadata = convert_songname_on_metadata(songName)
    fileNameWithPath = os.path.join(path, fileName)
    metatag = EasyID3(fileNameWithPath)
    metatag['album'] = albumName
    metatag['artist'] = metadata['artist']
    metatag['title'] = metadata['title']
    metatag.save()
    print "added metadata"
    print fileNameWithPath
    audio = MP3(fileNameWithPath, ID3=EasyID3)
    print audio.pprint()




def main():

    PATH='/mnt/TOSHIBA EXT/muzyka/Youtube list/'   
    
    add_metadata_manual("Bachata", 102, PATH, "Joan Soriano - Tu me estas matando.mp3")
#    add_metadata_manual_without_number(albumName, PATH, fileName)

    print ("Finished")
    
if __name__ == '__main__':
    main()
