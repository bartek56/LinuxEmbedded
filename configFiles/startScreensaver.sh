#!/bin/bash
timeout='8'
path='/home/Pictures/tapety'
startTime='120000'
random='-z'


xinit -- -nocursor &

export pid1=$!

sleep 1
DISPLAY=:0 feh "$random" -F -D"$timeout" -x "$path" &
export pid2=$!
echo $pid2
sleep 4

#while process running
while kill -0 $pid2 2> /dev/null; do
 # Do stuff
 echo "running"
 sleep 2
done

kill $pid1

echo "killed"
systemctl start start
exit 1
