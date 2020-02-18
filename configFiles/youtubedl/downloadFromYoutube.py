from __future__ import unicode_literals
import sys
import youtube_dl
import os
from datetime import datetime
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3


PATH='/tmp/muzyka/Youtube list/'

def convert_song_name(songName):
    songName = songName.replace("(Official Video)", "")
    songName = songName.replace("( Official Video )", "")
    songName = songName.replace("(Official Video HD)", "")
    songName = songName.replace("[Official Video]", "")
    songName = songName.replace("[OFFICIAL VIDEO]", "")
    songName = songName.replace("Official Video", "")
    songName = songName.replace("(OFFICIAL VIDEO)", "")
    songName = songName.replace("(Video Official)", "")
    songName = songName.replace("(Official Video HD)", "")
    songName = songName.replace("[Video Official]", "")
    songName = songName.replace("Video Official", "")
    songName = songName.replace("(VIDEO OFFICIAL)", "")
    songName = songName.replace("(official video)", "")
    songName = songName.replace("[Official Music Video]", "")
  
    songName = songName.replace("(Oficial Video)", "")
    songName = songName.replace("[Oficial Video]", "")
    songName = songName.replace("Oficial Video", "")
    songName = songName.replace("(OFICIAL VIDEO)", "")
    songName = songName.replace("(Video Oficial)", "")
    songName = songName.replace("(Oficial Video HD)", "")
    songName = songName.replace("[Video Oficial]", "")
    songName = songName.replace("Video Oficial", "")
    songName = songName.replace("(VIDEO OFICIAL)", "")

    songName = songName.replace("(Audio)", "")
    songName = songName.replace("(Official Audio)", "")
    songName = songName.replace("[Official Audio]", "")

    songName = songName.replace("(Official Music Video)", "")
    songName = songName.replace("/", " ")
    return songName

def rename_song_name(songName):
    songName = convert_song_name(songName)
    songName = songName.lstrip()
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
        
        metatag = EasyID3(newFileNameWithPath)
        metatag['album'] = albumName
        metatag['artist'] = metadataSongName['artist']
        metatag['title'] = metadataSongName['title']
        metatag.save()
        print "[ID3] updated metadata from YouTube"
        audio = MP3(newFileNameWithPath, ID3=EasyID3)
        print audio.pprint()

def add_metadata(trackNumber, playlistName, songName):
      path=PATH+playlistName
      albumName="YT "+playlistName

      filesList = [f for f in os.listdir(path) if f.startswith(songName)]
      for x in range(len(filesList)):
        originalFileName = filesList[x]

        newFileName = rename_song_file(path, originalFileName)
        newSongName = newFileName.replace(".mp3", "")
        
        metadataSongName = convert_songname_on_metadata(newSongName)
        newFileNameWithPath = os.path.join(path, newFileName)
        
        metatag = EasyID3(newFileNameWithPath)
        metatag['album'] = albumName
        metatag['artist'] = metadataSongName['artist']
        metatag['title'] = metadataSongName['title']
        metatag['tracknumber'] = str(trackNumber)
        metatag.save()
        print "[ID3] Added metadata"
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
#'playlist-start': 8
          }  
  results = youtube_dl.YoutubeDL(ydl_opts).extract_info(url,download=False)
  
  playlistIndexList = [i['playlist_index'] for i in results['entries']]
  songsTitleList = [i['title'] for i in results['entries']]
  for x in range(len(songsTitleList)):
     songName = songsTitleList[x]
     mp3ext=".mp3"
     fileName="%s%s"%(songName,mp3ext)

     newFileName = rename_song_file(path, fileName)
     newSongName = newFileName.replace(".mp3", "")    
     metadataSongName = convert_songname_on_metadata(newSongName)
     newFileNameWithPath = os.path.join(path, newFileName)    
     metatag = EasyID3(newFileNameWithPath)
     metatag['album'] = albumName
     metatag['artist'] = metadataSongName['artist']
     metatag['title'] = metadataSongName['title']
     metatag['tracknumber'] = str(trackNumber)
     metatag.save()
     print "[ID3] updated metadata from YouTube"
     audio = MP3(newFileNameWithPath, ID3=EasyID3)
     print audio.pprint()

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
#'playlist-start': 8
          }  
  results = youtube_dl.YoutubeDL(ydl_opts).extract_info(url)
  
  songsTitleList = [i['title'] for i in results['entries']]
  playlistIndexList = [i['playlist_index'] for i in results['entries']]
  for x in range(len(songsTitleList)):
     songName = songsTitleList[x]
     add_metadata(playlistIndexList[x], playlistName, songName)


def main():
   now = datetime.now()
   dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
   print("---------  " + dt_string + "  ---------") 

#  PART 1
   download_video_playlist("https://www.youtube.com/playlist?list=PL6uhlddQJkfiCtXJW-I0OASdxMc7sGHn5", "chillout")
   download_video_playlist("https://www.youtube.com/playlist?list=PL6uhlddQJkfgHTfI_P_BaACTGN2Km_4Yk", "Bachata")
   download_video_playlist("https://www.youtube.com/playlist?list=PL6uhlddQJkfjahtnJWMf2cW6TDmpfTUqk", "spokojne-sad")
   download_video_playlist("https://www.youtube.com/playlist?list=PL6uhlddQJkfjKkH06p81TLmGItIfoMnb5", "relaks")
   download_video_playlist("https://www.youtube.com/playlist?list=PL6uhlddQJkfi6xtpV-Di4Hgf3qCHiScyU", "Kizomba")
   download_video_playlist("https://www.youtube.com/playlist?list=PL6uhlddQJkfiB-7Td9IIYbYM0DsPjxAt0", "imprezka")
   download_video_playlist("https://www.youtube.com/playlist?list=PL6uhlddQJkfi2UzQtyRhB4zVClwJlzuHD", "Reggae")


#  PART 2
   download_video_playlist("https://www.youtube.com/playlist?list=PL6uhlddQJkfgDX6QR1isPJEUNkWRbPa0e", "polskie hity")
   download_video_playlist("https://www.youtube.com/playlist?list=PL6uhlddQJkfgMkKYQ8zK1wPzLE7nuYbYk", "stare ale jare")
   download_video_playlist("https://www.youtube.com/playlist?list=PL6uhlddQJkfg4ur-Bk9PCdqguhKoHCfMD", "muzyka filmowa")
   download_video_playlist("https://www.youtube.com/playlist?list=PL6uhlddQJkfgcWvb2c97oOX773DQHnhjQ", "wesele stare hity")
   download_video_playlist("https://www.youtube.com/playlist?list=PL6uhlddQJkfh09hGVx2_RreHvFmenLMma", "wesele pop")
   download_video_playlist("https://www.youtube.com/playlist?list=PL6uhlddQJkfjJaHNCH5XacdQdGOOCjuej", "wesele disco-polo")
   download_video_playlist("https://www.youtube.com/playlist?list=PL6uhlddQJkfjIGBN67_y2HEUx3lAjLGih", "wesele impreza")
   download_video_playlist("https://www.youtube.com/playlist?list=PL6uhlddQJkfgXRVUHpk-nhxfY4PmNMQp5", "electro Swing")
   download_video_playlist("https://www.youtube.com/playlist?list=PL6uhlddQJkfhPdw0tTOp-k2WGWkScw6pU", "hip-hop")
   download_video_playlist("https://www.youtube.com/playlist?list=PL6uhlddQJkfiC8LyEB92IEsBFlbBjxCj0", "techno")
   download_video_playlist("https://www.youtube.com/playlist?list=PL6uhlddQJkfh6_5dWYpBB9bGVIKctGT2Y", "muzyka klasyczna")
   download_video_playlist("https://www.youtube.com/playlist?list=PL6uhlddQJkfh9AqFWYPJ-AIQag25aa6nL", "taniec")
   download_video_playlist("https://www.youtube.com/playlist?list=PL6uhlddQJkfi5RcPXcTSqnkHN6En7URPS", "salsa")
   download_video_playlist("https://www.youtube.com/playlist?list=PL6uhlddQJkfgRcnKrIsUXb2lEfknbLBWX", "Semba")
   download_video_playlist("https://www.youtube.com/playlist?list=PL6uhlddQJkfiYtX-sgGsQDKbSOuvNZnrj", "Bachata Dominikana")



#   download_video_playlist("https://www.youtube.com/playlist?list=PL6uhlddQJkfh4YsbxgPE70a6KeFOCDgG_", "test")
#   update_metadata("test")
#   update_metadata_from_YTplaylist("https://www.youtube.com/playlist?list=PL6uhlddQJkfh4YsbxgPE70a6KeFOCDgG_", "test")

#   download_video_playlist("", "")

   print ("Finished\n\n")
    
if __name__ == '__main__':
    main()
