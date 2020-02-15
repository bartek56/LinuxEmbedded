#/bin/bash
minVolume=26
maxVolume=70
growingVolume=16
growingSpeed=11
playlist=""
theNewestSongs=true


set -e

mpc --wait clear
mpc --wait load $playlist
mpc --wait random on
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

