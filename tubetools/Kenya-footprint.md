### Objective: Make a zim file with items in a google spreadsheet
1. There was an initial list of youtube videos which appeared to be exam preparation for upper level students.
2. My initial concern was that the list was too long, and that navigation to find the correct video within the zim file might not be very friendly.
3. The customer cut down the list to 37 videos, which still seems long, but better.
4. The input was a google spread sheet at https://docs.google.com/spreadsheets/d/1yxm93GH8SAerAeoomKZaqQIVGulfgxO_oqn6z0_xS-w/edit#gid=0
5. Looking for a way to bring the list down to my machine, I noticed the "Download to cvs" uption under the "File" tab.
6. Once the list downloaded to my machine, I wrote the short python program to pick out just the video Id (11 random characters). See csv2ytid.py.
7. This created a file with 37 lines:
```
kaYVL4FDvZA
iDixml4rTeE
qyLevPfnIZ8
ybsNFgVIQ0w
. . .
```
8. Then I wrote a python program that uses google's youbute api (applicatin interface) to create and load these video Id's into a youtube playlist. The playlist.py program has a help screen
```
./playlists.py -h
usage: playlists.py [-h] [-c CREATE] [-d DELETE] [-i ITEMS_FILE] [-l] [-p SETPL] [-v] [-x XVIDEO]

Operate on Youtube Playlists that belong to you.

optional arguments:
  -h, --help            show this help message and exit
  -c CREATE, --create CREATE
                        Create playlist with this name.
  -d DELETE, --delete DELETE
                        Delete playlist by number.
  -i ITEMS_FILE, --items_file ITEMS_FILE
                        Insert Ids into default playlist
  -l, --list            List playlistss in your Channel.
  -p SETPL, --setPL SETPL
                        Set the playlist to work on
  -v, --videolist       List videos in current playlist.
  -x XVIDEO, --xvideo XVIDEO
                        Remove this video from current playlist
```
9. Pytube is a python-to-youtube interface which is pretty easy to understand. I wrote a program to recieve youtube Id's on an input pipe, and accumulate the length in time and the number of bytes:
```
(yt-venv) root@ubuntu2094:/opt/iiab/youtube/tubetools# cat addthese |./summarize_playlist.py 

 videoId  seconds   h:m:s total time         bytes   Total
============================================================
kaYVL4FDvZA 4194 01:09:54 01:10:03 filesize:203270836 194M
iDixml4rTeE 3421 00:57:01 02:07:04 filesize:164312044 351M
. . .
XTrmeop-N9s 7134 01:58:54 53:38:02 filesize:132046075 7.21G
b7HGsomAMD0 8513 02:21:53 55:59:55 filesize:146761298 7.35G
6k_y-Y6c5Uw 8088 02:14:48 58:14:43 filesize:149928866 7.49G
(yt-venv) root@ubuntu2094:/opt/iiab/youtube/tubetools# 
```
Note the use of "cat" command to feed the video Id's into local summarize_paylist.py (requireing "./" as a prefix). The summarize program indicates a total of 58 hours, and a size of approximately 7.49GB.  We intent to select the "--low-quality option" to conserve space, and hope that the quality will be good enough.

10. When I ran the start script with the "--low-quality" option:
```
python3.8 ../youtube2zim --api-key $API_KEY  --low-quality --id  PLs2auPpToJpbLTwPQ1fSGq5wCSY8rmgB0 --type playlist --name kenya
```
the zim generatiion seemed to stall trying to run ffmpeg (a re-encoding process), and the cpu utilization zoomed to 100%. So I removed that optionn. I'm in the middle of a zim generation that looks as it will take about 12 hours. I don't think the slowness is cpu related, since user space utilication is about 3%, and the machine is 90% idle. It must be google throttling.
