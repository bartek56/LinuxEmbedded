#!/bin/bash

set -e

cd /tmp
#git clone https://github.com/ytdl-org/youtube-dl
cd youtube-dl/
rev=$(git rev-list --tags --max-count=1)
git checkout $rev
rm -rf /usr/lib/python2.7/youtube_dl/*
cp -r youtube_dl/* /usr/lib/python2.7/youtube_dl/

