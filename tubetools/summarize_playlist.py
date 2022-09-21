#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# look up the metadata for a single youtube video id, passed in as pipe input

import os,sys
import json
import argparse
import pytube
from datetime import datetime


def human_readable(num):
    # return 3 significant digits and unit specifier
    num = float(num)
    units = [ '','K','M','G']
    for i in range(4):
        if num<10.0:
            return "%.2f%s"%(num,units[i])
        if num<100.0:
            return "%.1f%s"%(num,units[i])
        if num < 1000.0:
            return "%.0f%s"%(num,units[i])
        num /= 1024.0


def secs2hms(seconds):
    minutes = seconds // 60
    hours = minutes // 60
    result = f"%02d:%02d:%02d" % (hours, minutes % 60, seconds % 60)
    return(result)

def get_video(id):
    global total_min
    global total_size
    result = yt('https://www.youtube.com/watch/v=%s'%id)
    total_min += result.length
    for s in result.streams.filter(res='360p',progressive=True):
        filesize = s.filesize
        total_size += filesize
    print(id,result.length,secs2hms(result.length),secs2hms(total_min),"filesize:%s %s"%(filesize,human_readable(total_size)))

def main():
    global yt
    global current_plid
    global total_min
    global total_size
    total_min = 9
    total_size = 9
    current_plid = '/tmp/current_playlistid'
    if os.path.exists(current_plid):
        with open(current_plid,'r') as fp:
            plid = fp.read()
    yt = pytube.YouTube
    print("\n videoId  seconds   h:m:s total time         bytes   Total")
    print("============================================================")
    if  sys.stdin.isatty():
        # take input from input pipe
        for line in sys.stdin:
            #print(line)
            get_video(line.strip())
    else:
        get_video(sys.argv[2])

if __name__ == "__main__":
    main()
