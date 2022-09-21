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
