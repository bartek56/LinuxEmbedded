#/bin/bash
minVolume=30
maxVolume=90
defaultVolume=40
growingVolume=10
growingSpeed=20
playlist="alarm"
theNewestSongs=false


set -e
IFS=$'\n'

#$(ls /mnt/TOSHIBA\ EXT/muzyka/Youtube\ list/  -lRt -1 | grep .mp3 | sort -k6 -r | awk '{for(i=9; i<=NF; ++i) printf "%s ", $i; print ""}' | head -n 10)

if [ "$theNewestSongs" == true ]; then
    countSongs=0
    lastDays=0

    while [ $countSongs -le 10 ]; do
 	lastDays=$((lastDays + 1))
        echo $lastDays
	countSongs=$(find "/mnt/TOSHIBA EXT/muzyka/Youtube list" -type f -mtime -$lastDays -name "*.mp3" | wc -l)
        echo $countSongs
    done

    musicList=$(find "/mnt/TOSHIBA EXT/muzyka/Youtube list" -type f -mtime -$lastDays -name "*.mp3" -exec basename '{}' ';' | head -n 10 )
   
    mpc --wait clear
    for songName in $musicList; do
        mpc --wait listall | grep $songName | mpc add
    done
else 
    mpc clear
    mpc --wait load $playlist
fi

mpc random on
mpc volume $minVolume
mpc play

start=true

echo "start"
sleep $growingSpeed

while true ; do
    result=$(mpc volume)
    IFS=':' read -r -a array <<< "$result"
    volume=${array[1]::-1}
    if [ $(($volume >= $maxVolume)) == 1 ]; then
        start=false
	echo "MAX VALUE"
    fi   
    if [ "$start" == true ]; then
        result=$(mpc volume +$growingVolume)
        echo $result
    fi

    sleep $growingSpeed
done

