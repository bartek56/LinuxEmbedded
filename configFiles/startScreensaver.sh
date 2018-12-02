#!/bin/bash

pid="$@"
echo $pid

sleep 2
DISPLAY=:0 feh -F -D3 -x -S filename /home/pictures/ &
export pid2=$!
echo $pid2
sleep 3

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
