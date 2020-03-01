#!/bin/bash

# synchronization between laptop and Brzozowscy server
# catalogs:
# Dell external drive:
#  dokumenty            remote   Brzozowscy server (priv)
#  images_system        local    Brzozowscy server (priv)
#  instalki programy    local    Brzozowscy server (share)
#  Kamera sportowa      local    Brzozowscy server (priv)
#  szkola               local    Brzozowscy server (priv)
#  taniec               remote   Brzozowscy server (share) 
#  tapety               remote   Brzozowscy server (priv)
#  VHS na DVD                    Brzozowscy server (priv)
#  Zdjecia              remote   Brzozowscy server (priv)
#  
# MediaServer
#  movies                        Brzozowscy server (share)
#  TVShows                       Brzozowscy server (share)
#  music                remote   Brzozowscy server (share)
#  books                remote   Brzozowscy server (share)
#


# VARIABLES: user@address
BRZOZOWSCY_REMOTE=
BRZOZOWSCY_REMOTE_ROOT=
MEDIASERVER_REMOTE=

remoteSyncFromDell()
{
  printf "Remote sync From Dell\n"
  printf "mount \n"
  ssh -t $BRZOZOWSCY_REMOTE_ROOT 'mount /dev/sda1 /media/priv'
  
  printf "\nDOKUMENTY \n"
  rsync -srvazz --delete /home/bartosz/Documents/dokumenty $BRZOZOWSCY_REMOTE:/media/priv/

  printf "\nTANIEC \n"
  rsync -srvazz --delete /home/bartosz/Video/taniec $BRZOZOWSCY_REMOTE:/media/share/shareTV/

  printf "\nTAPETY \n"
  rsync -srvazz --delete /home/bartosz/pictures/tapety $BRZOZOWSCY_REMOTE:/media/priv/

  printf "\nZDJECIA \n"
  rsync -srvazz --delete /home/bartosz/pictures/zdjecia $BRZOZOWSCY_REMOTE:/media/priv/

  printf "\numount \n"
  ssh -t $BRZOZOWSCY_REMOTE_ROOT 'umount /media/priv'
}

remoteSyncFromBrzozowscy()
{
  printf "Remote Sync from Brzozowscy\n"	
  printf "MUZYKA \n"
  rsync -srvazz --delete "$MEDIASERVER_REMOTE:/mnt/TOSHIBA EXT/muzyka/" "/media/shareTV/share/music/"

  printf "\nKSIAZKI \n"
  rsync -srvazz --delete "$MEDIASERVER_REMOTE:/mnt/TOSHIBA EXT/books" "/media/shareTV/share/"

}

localSyncInBrzozowscy()
{
  printf "local sync in Brzozowscy"
  printf "images_system \n"       # (priv)
  rsync -srvazz --delete "/media/programmer/Dell HDD/images_system"	"/media/programmer/priv/"

  printf "\ninstalki programy \n"   # (share)
  rsync -srvazz --delete "/media/programmer/Dell HDD/instalki programy" "/media/shareTV/share/"

  printf "\nKamera sportowa \n"     # (priv)
  rsync -srvazz --delete "/media/programmer/Dell HDD/Kamera sportowa" "/media/programmer/priv/"

  printf "\nszkola \n"              # (priv)
  rsync -srvazz --delete "/media/programmer/Dell HDD/szkoła" "/media/programmer/priv/"

  printf "\nDOKUMENTY \n"
  rsync -srvazz --delete "/media/programmer/Dell HDD/dokumenty" "/media/programmer/priv/"

  printf "\nTANIEC \n"
  rsync -srvazz --delete "/media/programmer/Dell HDD/taniec" "/media/shareTV/share/"

  printf "\nTAPETY \n"
  rsync -srvazz --delete "/media/programmer/Dell HDD/tapety" "/media/programmer/priv/"

  printf "\nZDJECIA \n"
  rsync -srvazz --delete "/media/programmer/Dell HDD/Zdjęcia/z telefonu/7 Xiaomi Mi" "/media/programmer/priv/Zdjęcia/z telefonu/"

}

tvshowsToHardDrive()
{
   printf "\nGALILEO \n"
	 filesList=$(rsync -snrvazz "/media/shareTV/share/TVShows/Galileo/" "$MEDIASERVER_REMOTE:/mnt/TOSHIBA EXT/Wideo/TV Shows/Galileo/" | grep -E "*.mkv|*.ts")
   for file in $filesList; do
     printf "%s\n" $file
		 cp -n "/media/shareTV/share/TVShows/Galileo/$file" "/media/programmer/Dell HDD/Galileo/"
	 done
}


set -e

#remoteSyncFromDell
#remoteSyncFromBrzozowscy
#localSyncInBrzozowscy
#tvshowsToHardDrive



