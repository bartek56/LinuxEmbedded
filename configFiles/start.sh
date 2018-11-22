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
/opt/MediaServerApp/bin/MediaServerApp
exit 1

