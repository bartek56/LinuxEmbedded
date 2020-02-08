#/bin/bash

set -e

mpc --wait clear
mpc --wait load alarm
mpc --wait random on
mpc --wait repeat on
mpc volume 10
mpc play

SECONDS=0

while true ; do
    result=$(mpc volume +5)
    echo $result
    if echo $result | grep -q "volume: 40%"; then
        mpc stop
        exit 0
    fi
    sleep 8
done
