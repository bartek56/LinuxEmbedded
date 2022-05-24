#!/bin/bash

# synchronization between laptop and Brzozowscy server
# catalogs:
# Dell external drive:
#  dokumenty            Brzozowscy server (priv)    syncFromDell localSyncInBrzozowscy
#  Zdjecia              Brzozowscy server (priv)    syncFromDell localSyncInBrzozowscy
#  tapety               Brzozowscy server (share)   syncFromDell localSyncInBrzozowscy
#  images_system        Brzozowscy server (priv)    localSyncInBrzozowscy
#  szkola               Brzozowscy server (priv)    localSyncInBrzozowscy
#  taniec               Brzozowscy server (share)   localSyncInBrzozowscy
#  instalki programy    Brzozowscy server (share)   localSyncInBrzozowscy
#  VHS na DVD           Brzozowscy server (priv)    localSyncInBrzozowscy 
# TODO
#  Kamera sportowa      Brzozowscy server (priv)    localSyncInBrzozowscy 


# MediaServer
#  movies               Brzozowscy server (share)   WITHOUT_BACKUP
#  TVShows              Brzozowscy server (share)   WITHOUT_BACKUP
#  music                Brzozowscy server (share)   syncFromBrzozowscy
#  books                Brzozowscy server (share)   syncFromBrzozowscy
#  audiobooks           Brzozowscy server (share)   syncFromBrzozowscy


# VARIABLES: user@address
BRZOZOWSCY_REMOTE=
BRZOZOWSCY_REMOTE_ROOT=
MEDIASERVER_REMOTE=
BRZOZOWSCY_PORT=
MEDIASERVER_PORT=

syncFromDell()
{
    printf "Remote sync From Dell\n"
    printf "mount \n"
    ssh -p $BRZOZOWSCY_PORT -t $BRZOZOWSCY_REMOTE_ROOT 'mount /dev/sda1 /media/priv'

    printf "\nDOKUMENTY \n"
    rsync -srvazz -e 'ssh -p $BRZOZOWSCY_PORT' --delete "/home/bartosz/Documents/dokumenty" "$BRZOZOWSCY_REMOTE:/media/priv/"

    printf "\nTAPETY \n"
    rsync -srvazz -e 'ssh -p $BRZOZOWSCY_PORT' --delete "/home/bartosz/Pictures/tapety" "$BRZOZOWSCY_REMOTE:/media/shareTV/share/"

    printf "\nZDJECIA \n"
    rsync -srvazz -e 'ssh -p $BRZOZOWSCY_PORT' --delete "/home/bartosz/Pictures/z telefonu/7 Xiaomi Mi" "$BRZOZOWSCY_REMOTE:/media/priv/Zdjęcia/z telefonu/"

    printf "\numount \n"
    ssh -p $BRZOZOWSCY_PORT -t $BRZOZOWSCY_REMOTE_ROOT 'umount /media/priv'
}

syncFromBrzozowscy()
{
    printf "Remote Sync from Brzozowscy\n"
    printf "MUZYKA \n"
    rsync -srvazz -e 'ssh -p $MEDIASERVER_PORT' --delete "$MEDIASERVER_REMOTE:/mnt/TOSHIBA EXT/muzyka/" "/media/shareTV/share/music/"

    printf "\nKSIAZKI \n"
    rsync -srvazz -e 'ssh -p $MEDIASERVER_PORT'--delete "$MEDIASERVER_REMOTE:/mnt/TOSHIBA EXT/books" "/media/shareTV/share/"

    printf "\nAUDIOBOOKS \n"
    rsync -srvazz -e 'ssh -p $MEDIASERVER_PORT'--delete "$MEDIASERVER_REMOTE:/mnt/TOSHIBA EXT/Audiobooks" "/media/shareTV/share/"
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
    rsync -srvazz --delete "/media/programmer/Dell HDD/tapety" "/media/shareTV/share/"

    printf "\nZDJECIA \n"
    rsync -srvazz --delete "/media/programmer/Dell HDD/Zdjęcia" "/media/programmer/priv/"
}

set -e
argument=$1


if [[ "$argument" == "mediaserver" ]]; then
    printf "mediaserver\n"
elif [[ "$argument" == "brzozowscy" ]]; then
    printf "brzozowscy\n"
    syncFromBrzozowscy
elif [[ "$argument" == "dell" ]]; then 
    printf "dell\n"
    syncFromDell
elif [[ "$argument" == "local" ]]; then 
    printf "local\n"
    localSyncInBrzozowscy
fi

