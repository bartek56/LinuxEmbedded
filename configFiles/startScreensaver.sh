#!/bin/bash
timeout='6'
path='/home/pictures/rower'
startTime='360000'
random='-z'

pid="$@"
echo $pid

sleep 2
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

kill $pid

echo "killed"
/opt/MediaServerApp/bin/MediaServerApp
exit 1
