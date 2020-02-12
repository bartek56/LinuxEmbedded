#/bin/bash
sleepTime=10
minVolume=10
maxVolume=80
volumeJump=10

set -e

mpc --wait clear
mpc --wait load alarm
mpc --wait random on
mpc volume $minVolume
mpc play

start=true

echo "start"
sleep $sleepTime

while true ; do
    result=$(mpc volume)
    IFS=':' read -r -a array <<< "$result"
    volume=${array[1]::-1}
    if [ $(($volume >= $maxVolume)) == 1 ]; then
        start=false
	echo "MAX VALUE"
    fi   
    if [ "$start" == true ]; then
        result=$(mpc volume +$volumeJump)
        echo $result
    fi

    sleep $sleepTime
done

