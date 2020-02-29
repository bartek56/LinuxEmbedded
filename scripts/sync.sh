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
  print "Remote Sync from Brzozowscy\n"	
  printf "MUZYKA \n"
  rsync -srvazz --delete $MEDIASERVER_REMOTE:/mnt/TOSHIBA EXT/ /media/priv

  printf "\nKSIAZKI \n"
  rsync -srvazz --delete $MEDIASERVER_REMOTE:/mnt/TOSHIBA EXT/ /media/priv

}

localSyncInBrzozowscy()
{
  print "local sync in Brzozowscy"
  printf "images_system \n"       # (priv)
  rsync -srvazz --delete /mnt/TOSHIBA EXT/ /media/priv

  printf "\ninstalki programy \n"   # (share)
  rsync -srvazz --delete /mnt/TOSHIBA EXT/ /media/priv

  printf "\nKamera sportowa \n"     # (priv)
  rsync -srvazz --delete /mnt/TOSHIBA EXT/ /media/priv

  printf "\nszkola \n"              # (priv)
  rsync -srvazz --delete /mnt/TOSHIBA EXT/ /media/priv

}

set -e

#remoteSyncFromDell()
#remoteSyncFromBrzozowscy()
#localSyncInBrzozowscy()


