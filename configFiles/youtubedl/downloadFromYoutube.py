from __future__ import unicode_literals
import sys
import youtube_dl
import os
import warnings
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

PATH='/mnt/TOSHIBA EXT/muzyka/Youtube list/'
#PATH='/media/shareTV/share/music/Youtube list'
#PATH='/tmp/muzyka/Youtube list/'

def convert_song_name(songName):
    songName = songName.replace("(Oficial Video HD)", "")
    songName = songName.replace("(Official Video HD)", "")
    songName = songName.replace("[Official Video HD]", "")
    songName = songName.replace("[Official Music Video]", "")
    songName = songName.replace("(Official Music Video)", "")

    songName = songName.replace("(Official Lyric Video)", "")

    songName = songName.replace("( Official Video )", "")
    songName = songName.replace("(Official Video)", "")
    songName = songName.replace("[Official Video]", "")
    songName = songName.replace("(official video)", "")
    songName = songName.replace("(Official video)", "")
    songName = songName.replace("[OFFICIAL VIDEO]", "")
    songName = songName.replace("(OFFICIAL VIDEO)", "")
    songName = songName.replace("(Video Official)", "")
    songName = songName.replace("[Video Official]", "")
    songName = songName.replace("(VIDEO OFFICIAL)", "")
      
    songName = songName.replace("(Oficial Video)", "")
    songName = songName.replace("[Oficial Video]", "")
    songName = songName.replace("(OFICIAL VIDEO)", "")
    songName = songName.replace("(Video Oficial)", "")
    songName = songName.replace("[Video Oficial]", "")
    songName = songName.replace("(VIDEO OFICIAL)", "")
  
    songName = songName.replace("Video Oficial", "")
    songName = songName.replace("Video Official", "")
    songName = songName.replace("Oficial Video", "")
    songName = songName.replace("Official Video", "")

    songName = songName.replace("(Audio)", "")
    
    songName = songName.replace("(Official Audio)", "")
    songName = songName.replace("[Official Audio]", "")

    songName = songName.replace("   ", " ")   
    songName = songName.replace("  ", " ")   
    songName = songName.replace("  ", " ")   
    songName = songName.replace(" _", "")

    return songName

def rename_song_name(songName):
    songName = convert_song_name(songName)
    ext = ".xyz"
    songName = "%s%s"%(songName,ext)

    songName = songName+".xyz"
    songName = songName.replace("  .xyz", ".xyz")
    songName = songName.replace(" .xyz", ".xyz")
    songName = songName.replace(".xyz", "")
    
    return songName

def rename_song_file(path, fileName):

    originalFileName = fileName 
    
    fileName = convert_song_name(fileName)

    fileName = fileName.replace("  .mp3", ".mp3")
    fileName = fileName.replace(" .mp3", ".mp3")

    originalFileNameWithPath=os.path.join(path, originalFileName)
    fileNameWithPath = os.path.join(path, fileName)
    os.rename(originalFileNameWithPath, fileNameWithPath)

    return fileName

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

def update_metadata(playlistName):
      path=PATH+playlistName
      albumName="YT "+playlistName

      filesList = [f for f in os.listdir(path) if f.endswith(".mp3")]
      for x in range(len(filesList)):
        originalFileName = filesList[x]

        newFileName = rename_song_file(path, originalFileName)
        newSongName = newFileName.replace(".mp3", "")
        
        metadataSongName = convert_songname_on_metadata(newSongName)
        newFileNameWithPath = os.path.join(path, newFileName)
        if not os.path.isfile(newFileNameWithPath):
            warningInfo="WARNING: %s not exist"%(newFileName)
            warnings.warn(warningInfo, Warning)
            print bcolors.WARNING + warningInfo + bcolors.ENDC
            continue
        metatag = EasyID3(newFileNameWithPath)
        metatag['album'] = albumName
        metatag['artist'] = metadataSongName['artist']
        metatag['title'] = metadataSongName['title']
        metatag.save()
        print bcolors.OKGREEN + "[ID3] Added metadata" + bcolors.ENDC
        audio = MP3(newFileNameWithPath, ID3=EasyID3)
        print newFileNameWithPath
        print audio.pprint()

def add_metadata(trackNumber, playlistName, artist, songName):
    path=PATH+playlistName
    albumName="YT "+playlistName

    mp3ext=".mp3"
    fileName="%s%s"%(songName,mp3ext)
      
    if not os.path.isfile(os.path.join(path, fileName)):
        songName = songName.replace("/", "_")
        songName = songName.replace("|", "_")
        songName = songName.replace("\"", "'")
        fileName="%s%s"%(songName,mp3ext)
    if not os.path.isfile(os.path.join(path, fileName)):
        songName = rename_song_name(songName)
        fileName="%s%s"%(songName,mp3ext)
    if not os.path.isfile(os.path.join(path, fileName)):
        warningInfo="WARNING: %s not exist"%(fileName)
        print bcolors.WARNING + warningInfo + bcolors.ENDC
        return

    newFileName = rename_song_file(path, fileName)
    newSongName = newFileName.replace(".mp3", "")

    metadataSongName = convert_songname_on_metadata(newSongName)
    newFileNameWithPath = os.path.join(path, newFileName)
        
    metatag = EasyID3(newFileNameWithPath)
    metatag['album'] = albumName
    if artist is not None:
        metatag['artist'] = artist
    else:
        metatag['artist'] = metadataSongName['artist']
    metatag['title'] = metadataSongName['title']
    metatag['tracknumber'] = str(trackNumber)
    metatag.save()
    print bcolors.OKGREEN + "[ID3] Added metadata" + bcolors.ENDC
    print newFileNameWithPath
    audio = MP3(newFileNameWithPath, ID3=EasyID3)
    print audio.pprint()

def update_metadata_from_YTplaylist(url, playlistName):
    path=PATH+playlistName
    albumName="YT "+playlistName
    if not os.path.exists(path):
        os.makedirs(path)
    trackNumber = len([f for f in os.listdir(path) if f.endswith('.mp3')])

    ydl_opts = {
            'addmetadata': True,
            }  
    results = youtube_dl.YoutubeDL(ydl_opts).extract_info(url,download=False)
    if not results:
       warningInfo="ERROR: not extract_info in results"
       print bcolors.FAIL + warningInfo + bcolors.ENDC
       return

    artistList = [i['artist'] for i in results['entries']]
    playlistIndexList = [i['playlist_index'] for i in results['entries']]
    songsTitleList = [i['title'] for i in results['entries']]
    for x in range(len(songsTitleList)):
        add_metadata(playlistIndexList[x], playlistName, artistList[x], songsTitleList[x])

def download_video_playlist(url, playlistName):
    path=PATH+playlistName
    if not os.path.exists(path):
      os.makedirs(path)

    ydl_opts = {
          'format': 'bestaudio/best',
          'download_archive': path+'/downloaded_songs.txt',
          'addmetadata': True,
          'outtmpl': path+'/'+'%(title)s.%(ext)s',
          'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
             }],
          'ignoreerrors': True
          }  
    results = youtube_dl.YoutubeDL(ydl_opts).extract_info(url)
    if not results:
        warningInfo="ERROR: not extract_info in results"
        print bcolors.FAIL + warningInfo + bcolors.ENDC
        return

    songsTitleList = [i['title'] for i in results['entries']]
    playlistIndexList = [i['playlist_index'] for i in results['entries']]
    artistList = [i['artist'] for i in results['entries']]
        
    songCounter=0
    for x in range(len(songsTitleList)):
        add_metadata(playlistIndexList[x], playlistName, artistList[x], songsTitleList[x])
        songCounter+=1
  
    info = "[INFO] downloaded  %s songs"%(songCounter)
    print bcolors.OKGREEN + info + bcolors.ENDC
    return songCounter



def main():
   songsCounter = 0
   now = datetime.now()
   dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
   print("---------  " + dt_string + "  ---------") 

#  PART 1
#   songsCounter += download_video_playlist("https://www.youtube.com/playlist?list=PL6uhlddQJkfiCtXJW-I0OASdxMc7sGHn5", "chillout")
#   songsCounter += download_video_playlist("https://www.youtube.com/playlist?list=PL6uhlddQJkfgHTfI_P_BaACTGN2Km_4Yk", "Bachata")
#   songsCounter += download_video_playlist("https://www.youtube.com/playlist?list=PL6uhlddQJkfjahtnJWMf2cW6TDmpfTUqk", "spokojne-sad")
#   songsCounter += download_video_playlist("https://www.youtube.com/playlist?list=PL6uhlddQJkfjKkH06p81TLmGItIfoMnb5", "relaks")
#   songsCounter += download_video_playlist("https://www.youtube.com/playlist?list=PL6uhlddQJkfi6xtpV-Di4Hgf3qCHiScyU", "Kizomba")
#   songsCounter += download_video_playlist("https://www.youtube.com/playlist?list=PL6uhlddQJkfiB-7Td9IIYbYM0DsPjxAt0", "imprezka")
#   songsCounter += download_video_playlist("https://www.youtube.com/playlist?list=PL6uhlddQJkfi2UzQtyRhB4zVClwJlzuHD", "Reggae")
#   songsCounter += download_video_playlist("https://www.youtube.com/playlist?list=PL6uhlddQJkfiC8LyEB92IEsBFlbBjxCj0", "techno")
#   songsCounter += download_video_playlist("https://www.youtube.com/playlist?list=PL6uhlddQJkfgDX6QR1isPJEUNkWRbPa0e", "polskie hity")
#   songsCounter += download_video_playlist("https://www.youtube.com/playlist?list=PL6uhlddQJkfgMkKYQ8zK1wPzLE7nuYbYk", "stare ale jare")
#   songsCounter += download_video_playlist("https://www.youtube.com/playlist?list=PL6uhlddQJkfg4ur-Bk9PCdqguhKoHCfMD", "muzyka filmowa")
#   songsCounter += download_video_playlist("https://www.youtube.com/playlist?list=PL6uhlddQJkfgXRVUHpk-nhxfY4PmNMQp5", "electro Swing")
#   songsCounter += download_video_playlist("https://www.youtube.com/playlist?list=PL6uhlddQJkfhPdw0tTOp-k2WGWkScw6pU", "hip-hop")
#   songsCounter += download_video_playlist("https://www.youtube.com/playlist?list=PL6uhlddQJkfh6_5dWYpBB9bGVIKctGT2Y", "muzyka klasyczna")
#   songsCounter += download_video_playlist("https://www.youtube.com/playlist?list=PL6uhlddQJkfh9AqFWYPJ-AIQag25aa6nL", "taniec")
#   songsCounter += download_video_playlist("https://www.youtube.com/playlist?list=PL6uhlddQJkfi5RcPXcTSqnkHN6En7URPS", "salsa")
#   songsCounter += download_video_playlist("https://www.youtube.com/playlist?list=PL6uhlddQJkfgRcnKrIsUXb2lEfknbLBWX", "Semba")
#   songsCounter += download_video_playlist("https://www.youtube.com/playlist?list=PL6uhlddQJkfiYtX-sgGsQDKbSOuvNZnrj", "Bachata Dominikana")

#  PART 2
#   songsCounter += download_video_playlist("https://www.youtube.com/playlist?list=PL6uhlddQJkfgcWvb2c97oOX773DQHnhjQ", "wesele stare hity")
#   songsCounter += download_video_playlist("https://www.youtube.com/playlist?list=PL6uhlddQJkfh09hGVx2_RreHvFmenLMma", "wesele pop")
#   songsCounter += download_video_playlist("https://www.youtube.com/playlist?list=PL6uhlddQJkfjJaHNCH5XacdQdGOOCjuej", "wesele disco-polo")
#   songsCounter += download_video_playlist("https://www.youtube.com/playlist?list=PL6uhlddQJkfjIGBN67_y2HEUx3lAjLGih", "wesele impreza")


#   update_metadata_from_YTplaylist("https://www.youtube.com/playlist?list=PL6uhlddQJkfjahtnJWMf2cW6TDmpfTUqk", "spokojne-sad")
   
#   songsCounter += download_video_playlist("https://www.youtube.com/playlist?list=PL6uhlddQJkfh4YsbxgPE70a6KeFOCDgG_", "test")
#   update_metadata_from_YTplaylist("https://www.youtube.com/playlist?list=PL6uhlddQJkfh4YsbxgPE70a6KeFOCDgG_", "test")



   now = datetime.now()
   dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
   print("---------  " + dt_string + "  ---------") 
   summary = "[SUMMARY] downloaded  %s songs"%(songsCounter)
   print bcolors.OKGREEN + summary + bcolors.ENDC

if __name__ == '__main__':
    main()
