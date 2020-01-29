from __future__ import unicode_literals
import sys
import youtube_dl
import os
from datetime import datetime
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3


PATH='/mnt/TOSHIBA EXT/muzyka/Youtube list/'



def convert_song_name(songName):
    songName = songName.replace("(Official Video)", "")
    songName = songName.replace("(Official Video HD)", "")
    songName = songName.replace("[Official Video]", "")
    songName = songName.replace("Official Video", "")
    songName = songName.replace("(OFFICIAL VIDEO)", "")
    songName = songName.replace("(Video Official)", "")
    songName = songName.replace("(Official Video HD)", "")
    songName = songName.replace("[Video Official]", "")
    songName = songName.replace("Video Official", "")
    songName = songName.replace("(VIDEO OFFICIAL)", "")
     
    songName = songName.replace("(Oficial Video)", "")
    songName = songName.replace("(Oficial Video HD)", "")
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
     
    songName = songName+".xyz"
    songName = songName.replace("  .xyz", ".xyz")
    songName = songName.replace(" .xyz", ".xyz")
    songName = songName.replace(".xyz", "")
    return songName

def add_metadata(playListName, songName):
    fileName=songName+".mp3"
    audio = MP3(PATH+playlistName+'/'+fileName, ID3=EasyID3)
    result = audio.pprint()
    albumName="YT "+playlistName
    if(albumName not in result):
      metatag = EasyID3(PATH+playlistName+'/'+fileName)
      metatag['album'] = albumName
      
      slots = songName.split(" - ")
      if len(slots) == 2:
        metatag['artist'] = slots[0]
        metatag['title'] = slots[1]
        print "[ID3] Adding metadata: " + albumName + " " + slots[0] + " " + slots[1]

      else:
        slots = songName.split("-")
        if len(slots) == 2:
          metatag['artist'] = slots[0]
          metatag['title'] = slots[1]
          print "[ID3] Adding metadata: " + albumName + " " + slots[0] + " " + slots[1]
      metatag.save()


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
  
  ydl_opts = {
          'quiet': True,
          'ignoreerrors': True
          }  
  results = youtube_dl.YoutubeDL(ydl_opts).extract_info(url, download=False)
  urlList =  [i['webpage_url'] for i in results['entries']] 
  songsTitleList = [i['title'] for i in results['entries']] 
  for x in range(len(songsTitleList)): 
     songName = songsTitleList[x]
     songName = convert_song_name(songName)
     fileName = songName+".mp3"

     download_video_as_mp3(urlList[x], playlistName, songName)
     add_metadata(playListName, songName):

     
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
   

#   download_video_playlist("", "")

   print "Finished\n\n"
    
if __name__ == '__main__':
    main()
