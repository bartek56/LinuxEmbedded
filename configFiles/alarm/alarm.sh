#/bin/bash
minVolume=25
maxVolume=80
defaultVolume=35
growingVolume=8
growingSpeed=25
playlist="Youtube"
theNewestSongs=true


set -e
IFS=$'\n'

#$(ls /mnt/TOSHIBA\ EXT/muzyka/Youtube\ list/  -lRt -1 | grep .mp3 | sort -k6 -r | awk '{for(i=9; i<=NF; ++i) printf "%s ", $i; print ""}' | head -n 10)

if [ "$theNewestSongs" == true ]; then
    countSongs=0
    lastDays=0

    while [ $countSongs -le 2 ]; do
 	      lastDays=$((lastDays + 1))
	      countSongs=$(find "/mnt/TOSHIBA EXT/muzyka/Youtube list" -type f -mtime -$lastDays -name "*.mp3" | wc -l)
    done

    musicList=$(find "/mnt/TOSHIBA EXT/muzyka/Youtube list" -type f -mtime -$lastDays -name "*.mp3" -exec basename '{}' ';' | head -n 10 )
    
    mpc --wait clear
		songs=()
    for songName in $musicList; do
				songs+=($songName)
#        mpc --wait listall | grep $songName | mpc add
    done


    # revert list   
    for ((i=${#songs[@]}-1; i>=0; i-- )); do
        mpc --wait listall | grep ${songs[$i]} | mpc add
    done
		mpc random off
else 
    mpc clear
    mpc --wait load $playlist
    mpc random on
fi

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

