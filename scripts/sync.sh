#!/bin/bash

# synchronization between laptop and Brzozowscy server
# catalogs:
# Dell external drive:
#  dokumenty            remote   Brzozowscy server (priv)    remoteSyncFromDell
#  images_system        local    Brzozowscy server (priv)    localSyncInBrzozowscy
#  instalki programy    local    Brzozowscy server (share)   localSyncInBrzozowscy
#  Kamera sportowa      local    Brzozowscy server (priv)    localSyncInBrzozowscy
#  szkola               local    Brzozowscy server (priv)    localSyncInBrzozowscy
#  taniec               remote   Brzozowscy server (share)   remoteSyncFromDell
#  tapety               remote   Brzozowscy server (priv)    remoteSyncFromDell
#  VHS na DVD                    Brzozowscy server (priv)    
#  Zdjecia              remote   Brzozowscy server (priv)    remoteSyncFromDell
#  
# MediaServer
#  movies                        Brzozowscy server (share)   
#  TVShows                       Brzozowscy server (share)
#  music                remote   Brzozowscy server (share)   remoteSyncFromBrzozowscy
#  books                remote   Brzozowscy server (share)   remoteSyncFromBrzozowscy
#  audiobooks           remote   Brzozowscy server (share)   remoteSyncFromBrzozowscy


# VARIABLES: user@address
BRZOZOWSCY_REMOTE=
BRZOZOWSCY_REMOTE_ROOT=
MEDIASERVER_REMOTE=

remoteSyncFromDell()
{
  printf "Remote sync From Dell\n"
  printf "mount \n"
  ssh -p 20022 -t $BRZOZOWSCY_REMOTE_ROOT 'mount /dev/sda1 /media/priv'
  
  printf "\nDOKUMENTY \n"
  rsync -srvazz -e 'ssh -p 20022' --delete "/home/bartosz/Documents/dokumenty" "$BRZOZOWSCY_REMOTE:/media/priv/"

  printf "\nTANIEC \n"
  rsync -srvazz -e 'ssh -p 20022' --delete "/home/bartosz/Videos/taniec" "$BRZOZOWSCY_REMOTE:/media/shareTV/share/"

  printf "\nTAPETY \n"
  rsync -srvazz -e 'ssh -p 20022' --delete "/home/bartosz/Pictures/tapety" "$BRZOZOWSCY_REMOTE:/media/priv/"

  printf "\nZDJECIA \n"
  rsync -srvazz -e 'ssh -p 20022' --delete "/home/bartosz/Pictures/z telefonu/7 Xiaomi Mi" "$BRZOZOWSCY_REMOTE:/media/priv/Zdjęcia/z telefonu/"

  printf "\numount \n"
  ssh -p 20022 -t $BRZOZOWSCY_REMOTE_ROOT 'umount /media/priv'
}

remoteSyncFromBrzozowscy()
{
  printf "Remote Sync from Brzozowscy\n"	
  printf "MUZYKA \n"
  rsync -srvazz --delete "$MEDIASERVER_REMOTE:/mnt/TOSHIBA EXT/muzyka/" "/media/shareTV/share/music/"

  printf "\nKSIAZKI \n"
  rsync -srvazz --delete "$MEDIASERVER_REMOTE:/mnt/TOSHIBA EXT/books" "/media/shareTV/share/"

	printf "\nAUDIOBOOKS \n"
  rsync -srvazz --delete "$MEDIASERVER_REMOTE:/mnt/TOSHIBA EXT/Audiobooks" "/media/shareTV/share/"
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
  rsync -srvazz --delete "/media/programmer/Dell HDD/Zdjęcia" "/media/programmer/priv/"

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



