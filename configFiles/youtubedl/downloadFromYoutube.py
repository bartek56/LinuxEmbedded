from __future__ import unicode_literals
import sys
import youtube_dl
import os
from datetime import datetime
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3


PATH='/home/bartosz/Music/Youtube list/'

def rename_song_file(path, fileName):

    originalFileName = fileName 
    fileName = fileName.replace("(Official Video)", "")
    fileName = fileName.replace("( Official Video )", "")
    fileName = fileName.replace("(Official Video HD)", "")
    fileName = fileName.replace("[Official Video]", "")
    fileName = fileName.replace("[Official Video]", "")   
    fileName = fileName.replace("[OFFICIAL VIDEO]", "")
    fileName = fileName.replace("(OFFICIAL VIDEO)", "")
    fileName = fileName.replace("(Video Official)", "")
    fileName = fileName.replace("(Official Video HD)", "")
    fileName = fileName.replace("[Video Official]", "")
    fileName = fileName.replace("Video Official", "")
    fileName = fileName.replace("(VIDEO OFFICIAL)", "")
    fileName = fileName.replace("(official video)", "")    
    fileName = fileName.replace("[Official Music Video]", "")

    fileName = fileName.replace("(Oficial Video)", "")
    fileName = fileName.replace("(Oficial Video HD)", "")
    fileName = fileName.replace("[Oficial Video]", "")
    fileName = fileName.replace("Oficial Video", "")
    fileName = fileName.replace("(OFICIAL VIDEO)", "")
    fileName = fileName.replace("(Video Oficial)", "")
    fileName = fileName.replace("(Oficial Video HD)", "")
    fileName = fileName.replace("[Video Oficial]", "")
    fileName = fileName.replace("Video Oficial", "")
    fileName = fileName.replace("(VIDEO OFICIAL)", "")

    fileName = fileName.replace("(Audio)", "")
    fileName = fileName.replace("(Official Audio)", "")
    fileName = fileName.replace("[Official Audio]", "")

    fileName = fileName.replace("(Official Music Video)", "")
    fileName = fileName.replace("/", " ")
     
    fileName = fileName.replace("  .mp3", ".mp3")
    fileName = fileName.replace(" .mp3", ".mp3")

    originalFileNameWithPath=os.path.join(path, originalFileName)
    fileNameWithPath = os.path.join(path, fileName)
    os.rename(originalFileNameWithPath, fileNameWithPath)

    return fileName

def add_metadata(playlistName, fileName):
    songName=fileName.replace(".mp3","")
    path=PATH+playlistName
    fileNameWithPath = os.path.join(path, fileName)
    audio = MP3(fileNameWithPath, ID3=EasyID3)
    result = audio.pprint()
    albumName="YT "+playlistName
    if(albumName not in result):
      trackNumber = len([f for f in os.listdir(path) if f.endswith('.mp3')])
      trackNumber += 1
      metatag = EasyID3(fileNameWithPath)
      metatag['album'] = albumName
      metatag['tracknumber'] = str(trackNumber)
      slots = songName.split(" - ")
      info = " "
      if len(slots) == 2:
        metatag['artist'] = slots[0]
        metatag['title'] = slots[1]
        info = " " + slots[0] + " " + slots[1]
      else:
        slots = songName.split("-")
        if len(slots) == 2:
          metatag['artist'] = slots[0]
          metatag['title'] = slots[1]
          info = " " + slots[0] + " " + slots[1]
        else:  
          metatag['title'] = songName

      metatag.save()
      print ("[ID3] Added metadata")

def download_video_as_mp3(url, playlistName, songName):
    path=PATH+playlistName
    ydl_opts = {
            'format': 'bestaudio/best',
            'download_archive': path+'/downloaded_songs.txt',
            'addmetadata': True,
            'outtmpl': path+'/'+songName+'.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
             }],
            'ignoreerrors': True
               } 
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        
        ydl.download([url])

def download_video_playlist(url, playlistName):
  path=PATH+playlistName
  ydl_opts = {
          'ignoreerrors': True, 
          'format': 'bestaudio/best',
          'download_archive': path+'/downloaded_songs.txt',
          'addmetadata': True,
          'outtmpl': path+'/'+'%(title)s.%(ext)s',
          'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
             }],
          'playlist-start': 8
          }  
  #results = youtube_dl.YoutubeDL(ydl_opts).extract_info(url, download=False)
  
  with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
  
  filesList = [f for f in os.listdir(path) if f.endswith('.mp3')]
  
  for x in range(len(filesList)):
     originalFileName = filesList[x]
     newFileName = rename_song_file(path, originalFileName)
     add_metadata(playlistName, newFileName)
     
def main():
   now = datetime.now()
   dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
   print("---------  " + dt_string + "  ---------") 


#  PART 1
   download_video_playlist("https://www.youtube.com/playlist?list=PL6uhlddQJkfiCtXJW-I0OASdxMc7sGHn5", "chillout")
#   download_video_playlist("https://www.youtube.com/playlist?list=PL6uhlddQJkfgHTfI_P_BaACTGN2Km_4Yk", "Bachata")
#   download_video_playlist("https://www.youtube.com/playlist?list=PL6uhlddQJkfjahtnJWMf2cW6TDmpfTUqk", "spokojne-sad")
#   download_video_playlist("https://www.youtube.com/playlist?list=PL6uhlddQJkfjKkH06p81TLmGItIfoMnb5", "relaks")
#   download_video_playlist("https://www.youtube.com/playlist?list=PL6uhlddQJkfi6xtpV-Di4Hgf3qCHiScyU", "Kizomba")
#   download_video_playlist("https://www.youtube.com/playlist?list=PL6uhlddQJkfiB-7Td9IIYbYM0DsPjxAt0", "imprezka")
#   download_video_playlist("https://www.youtube.com/playlist?list=PL6uhlddQJkfi2UzQtyRhB4zVClwJlzuHD", "Reggae")


#  PART 2
   download_video_playlist("https://www.youtube.com/playlist?list=PL6uhlddQJkfgDX6QR1isPJEUNkWRbPa0e", "polskie hity")
#   download_video_playlist("https://www.youtube.com/playlist?list=PL6uhlddQJkfgMkKYQ8zK1wPzLE7nuYbYk", "stare ale jare")
#   download_video_playlist("https://www.youtube.com/playlist?list=PL6uhlddQJkfg4ur-Bk9PCdqguhKoHCfMD", "muzyka filmowa")
#   download_video_playlist("https://www.youtube.com/playlist?list=PL6uhlddQJkfgcWvb2c97oOX773DQHnhjQ", "wesele stare hity")
#   download_video_playlist("https://www.youtube.com/playlist?list=PL6uhlddQJkfh09hGVx2_RreHvFmenLMma", "wesele pop")
#   download_video_playlist("https://www.youtube.com/playlist?list=PL6uhlddQJkfjJaHNCH5XacdQdGOOCjuej", "wesele disco-polo")
#   download_video_playlist("https://www.youtube.com/playlist?list=PL6uhlddQJkfjIGBN67_y2HEUx3lAjLGih", "wesele impreza")
#   download_video_playlist("https://www.youtube.com/playlist?list=PL6uhlddQJkfgXRVUHpk-nhxfY4PmNMQp5", "electro Swing")
#   download_video_playlist("https://www.youtube.com/playlist?list=PL6uhlddQJkfhPdw0tTOp-k2WGWkScw6pU", "hip-hop")
#   download_video_playlist("https://www.youtube.com/playlist?list=PL6uhlddQJkfiC8LyEB92IEsBFlbBjxCj0", "techno")
#   download_video_playlist("https://www.youtube.com/playlist?list=PL6uhlddQJkfh6_5dWYpBB9bGVIKctGT2Y", "muzyka klasyczna")
#   download_video_playlist("https://www.youtube.com/playlist?list=PL6uhlddQJkfh9AqFWYPJ-AIQag25aa6nL", "taniec")
#   download_video_playlist("https://www.youtube.com/playlist?list=PL6uhlddQJkfi5RcPXcTSqnkHN6En7URPS", "salsa")
#   download_video_playlist("https://www.youtube.com/playlist?list=PL6uhlddQJkfgRcnKrIsUXb2lEfknbLBWX", "Semba")
#   download_video_playlist("https://www.youtube.com/playlist?list=PL6uhlddQJkfiYtX-sgGsQDKbSOuvNZnrj", "Bachata Dominikana")
   

#   download_video_playlist("", "")

   print ("Finished\n\n")
    
if __name__ == '__main__':
    main()
