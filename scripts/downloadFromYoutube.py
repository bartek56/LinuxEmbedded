from __future__ import unicode_literals
import sys
import youtube_dl
import os

def get_playlist_info(self):
        del self.ydl_opts['noplaylist']
        self.ydl_opts['extract_flat'] = True

        # in case of a radio playist, restrict the number of songs that are downloaded
        # if we received just the id, it is an id starting with 'RD'
        # if its a url, the id is behind a '&list='
        if song_utils.is_radio(self.target):
            self.ydl_opts['playlistend'] = self.musiq.base.settings.max_playlist_items

        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            self.info_dict = ydl.extract_info(self.target, download=False)

        if self.info_dict['_type'] != 'playlist' or 'entries' not in self.info_dict:
            raise NoPlaylistException('Not a Playlist')

        playlist_info = {}
        playlist_info['id'] = self.info_dict['id']
        playlist_info['urls'] = []
        if 'title' in self.info_dict:
            playlist_info['title'] = self.info_dict['title']
        for entry in self.info_dict['entries']:
            playlist_info['urls'].append('https://www.youtube.com/watch?v=' + entry['id'])
        return playlist_info


def download_video_as_mp3(url):
    ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
             }],
        } 
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])




def get_video_list(url):
  """
  Retrieves a list of video URL's from the playlist URL
  Args:
    url: A YouTube playlist URL
  Returns:
    A list of individual URL's for each video in the playlist
  """
  results = youtube_dl.YoutubeDL({'quiet': True}).extract_info(url, download=False)
  urlList =  [i['webpage_url'] for i in results['entries']] 
  nameList = [i['title'] for i in results['entries']] 
  filesName = os.listdir('/mnt/TOSHIBA EXT/muzyka/Youtube list/chillout/')
  for x in range(len(nameList)): 
    for y in range(len(filesName)):
      if nameList[x] in filesName[y]:
          print 'song exist'
        #download_video_as_mp3(urlList[x])
      else:
        print "song do not exist"
        #download_video_as_mp3(urlList[x])
def main():
#    get_playlist_info()
    get_video_list("https://www.youtube.com/playlist?list=PL6uhlddQJkfi5RcPXcTSqnkHN6En7URPS")
    #    print result
#    files_path = [os.path.abspath(x) for x in os.listdir('.')]
     
    
if __name__ == '__main__':
    main()
