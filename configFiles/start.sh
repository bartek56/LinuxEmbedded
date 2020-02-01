#!/bin/bash

pid="$@"

echo $pid

#while process running
while kill -0 $pid 2> /dev/null; do
    # Do stuff
    echo "running"
    sleep 2
done

echo "killed"
/usr/bin/MediaServer
exit 1

