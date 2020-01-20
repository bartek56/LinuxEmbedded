from __future__ import unicode_literals
import sys
import youtube_dl
import os
from datetime import datetime


def download_video_as_mp3(url, playlistName):
    path='/mnt/TOSHIBA EXT/muzyka/Youtube list/'+playlistName
    ydl_opts = {
            'format': 'bestaudio/best',
            'download_archive': path+'/downloaded_songs.txt',
            'outtmpl': path+'/%(title)s.%(ext)s',
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
    download_video_as_mp3(urlList[x], playlistName)

def main():
   now = datetime.now()
   dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
   print("---------  " + dt_string + "  ---------") 
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
   download_video_playlist("https://www.youtube.com/playlist?list=PL6uhlddQJkfiCtXJW-I0OASdxMc7sGHn5", "chillout")
   download_video_playlist("https://www.youtube.com/playlist?list=PL6uhlddQJkfgHTfI_P_BaACTGN2Km_4Yk", "Bachata")
   download_video_playlist("https://www.youtube.com/playlist?list=PL6uhlddQJkfjahtnJWMf2cW6TDmpfTUqk", "spokojnie-sad")
   download_video_playlist("https://www.youtube.com/playlist?list=PL6uhlddQJkfjKkH06p81TLmGItIfoMnb5", "relaks")
   download_video_playlist("https://www.youtube.com/playlist?list=PL6uhlddQJkfi6xtpV-Di4Hgf3qCHiScyU", "Kizomba")
   download_video_playlist("https://www.youtube.com/playlist?list=PL6uhlddQJkfiB-7Td9IIYbYM0DsPjxAt0", "imprezka")
   download_video_playlist("https://www.youtube.com/playlist?list=PL6uhlddQJkfgRcnKrIsUXb2lEfknbLBWX", "Semba")
   download_video_playlist("https://www.youtube.com/playlist?list=PL6uhlddQJkfiYtX-sgGsQDKbSOuvNZnrj", "Bachata Dominikana")
   download_video_playlist("https://www.youtube.com/playlist?list=PL6uhlddQJkfi5RcPXcTSqnkHN6En7URPS", "salsa")
#   download_video_playlist("", "")

   print "Finished\n\n"
    
if __name__ == '__main__':
    main()
