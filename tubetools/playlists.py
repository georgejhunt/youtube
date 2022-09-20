#!/usr/bin/env python
# coding: utf-8

# List, create, delete videos in a specific playlist, authenticate access to Youtube 
# ### Playlists Program Manipulates Youtube Playlists
# example: https://github.com/youtube/api-samples/blob/master/python/quickstart_web.py
# * Google has established a complicated process for a program to get permission from the owner of a channel (A channel is the storage unit for an individual Google user identity).

import os,sys
import json
import argparse
import requests

import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery

from googleapiclient.discovery import build
from  google.oauth2.credentials import Credentials
from oauth2client.client import OAuth2WebServerFlow

# Get the json file I created which holds config for tubetools
with open('/root/youtube/config.json','r') as fp:
    config_dict = json.loads(fp.read())

# this is the json file downloaded from google about project ID
CLIENT_ID_FILE = config_dict['CLIENT_ID_FILE'] 

with open(CLIENT_ID_FILE,'r') as fp:
    client_info = json.loads(fp.read())

category = 'installed'
CLIENT_ID = client_info[category]['client_id']
CLIENT_SECRET = client_info[category]['client_secret']

# Where to write the returned google credentials
CREDENTIALS_FILE = config_dict['CREDENTIALS_FILE'] 

# This OAuth 2.0 access scope allows for full read/write access to the
SCOPES = ['https://www.googleapis.com/auth/youtube']

API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'


def parse_args():
    parser = argparse.ArgumentParser(description="Operate on Youtube Playlists that belong to you.")
    parser.add_argument("-c","--create", help='Create playlist with this name.')
    parser.add_argument("-d","--delete", help='Delete playlist by number.',type=int)
    parser.add_argument("-i","--items_file", help='Insert Ids into default playlist')
    parser.add_argument("-l","--list", help='List numbers,names,itemCount in Channel.',action='store_true')
    parser.add_argument("-p","--setPL", help='Set the playlist to work on')
    parser.add_argument("-v","--videolist", help='List videos in current playlist.',action='store_true')
    parser.add_argument("-x","--xvideo", help='Remove this video from current playlist')
    return parser.parse_args()

def get_youtube_object():
    flow = OAuth2WebServerFlow(CLIENT_ID, CLIENT_SECRET, " ".join(SCOPES))

    if not os.path.exists(CREDENTIALS_FILE):
        # Step 1: get user code and verification URL
        # https://developers.google.com/accounts/docs/OAuth2ForDevices#obtainingacode
        flow_info = flow.step1_get_device_and_user_codes()
        print("Enter the following code at {0}: {1}".format(flow_info.verification_url,
                                                            flow_info.user_code))
        print("Then press Enter.")
        input()

        # Step 2: get credentials
        # https://developers.google.com/accounts/docs/OAuth2ForDevices#obtainingatoken
        credentials = flow.step2_exchange(device_flow_info=flow_info)
        print("Access token:  {0}".format(credentials.access_token))
        print("Refresh token: {0}".format(credentials.refresh_token))
        # Write the credentials for future use elsewhere
        with open(CREDENTIALS_FILE,'w') as fp:
          fp.write(credentials.to_json())
    else:
        credentials = Credentials.from_authorized_user_file(CREDENTIALS_FILE)

    # Return YouTube service
    # https://developers.google.com/accounts/docs/OAuth2ForDevices#callinganapi
    youtube = build('youtube', 'v3', credentials=credentials)
    return youtube

def get_my_playlists():
    global my_playlists
    playlists_list_response = youtube.playlists().list(
        part='contentDetails,snippet',
        mine = True
        ).execute()
    my_playlists = []
    for item in playlists_list_response['items']:
        my_playlists.append([item['id'],item['snippet']['title'],item['contentDetails']['itemCount']])
    return my_playlists


def delete_playlist(list_index):
    my_playlists = get_my_playlists()
    if list_index not in range(1,len(my_playlists)+1):
        print('Please use the Playlist index from the list command')
        return
    response = input('Do you want to delete %s? y/N'%my_playlists[list_index-1][1])
    if response != 'Y' and response != 'y':
        print('Aborting Delete')
        return
    response = youtube.playlists().delete(id=my_playlists[list_index-1][0]).execute()
    print(response)

def get_current_playlistid():
    if not os.path.exists(current_plid):
        print('Please set a default playlist ID with the -p option.`')
        sys.exit(5)
    with open(current_plid,'r') as fp:
        plid = fp.read()
        return plid

def set_playlist_id(playlist_index):
    global playlistid
    my_playlists = get_my_playlists()
    if len(my_playlists) == 1:
        # just set it and  be done
        with open(current_plid,'w') as fp:
            fp.write(my_playlists[0][0])
            print('You own only one playlist. . . . setting it as default')
            return
    print(str(my_playlists),playlist_index, len(my_playlists))
    if not (int(playlist_index) < len(my_playlists)+1 and int(playlist_index) >0):
        print('Please use the Playlist index from the list command')
        return
    response = input('Do you want to set PlaylistId to %s? y/N'%my_playlists[playlist_index-1][0])
    if response != 'Y' and response != 'y':
        print('Aborting playist change')
        return
    with open(current_plid,'w') as fp:
        fp.write(my_playlists[playlist_index-1][0])

def add_playlist(title):
  global youtube
  body = dict(
    snippet=dict(
      title=title,
      description="This is a temporary Playslist which is used as source for the Openzim 'youtube2zim' program."
    ),
    status=dict(
      privacyStatus='public'
    ) 
  ) 
  playlists_insert_response = youtube.playlists().insert(
    part='snippet,status',
    body=body
  ).execute()
  print('New playlist ID: %s' % playlists_insert_response['id'])
  with open(current_plid,'w') as fp:
    fp.write(playlists_insert_response['id'])

def get_video_ids(playlistid):
    global plcontents
    request = youtube.playlistItems().list(
        part="snippet,contentDetails",
        playlistId = playlistid,
        maxResults=25,
    )
    try:
        responses = request.execute()
    except Exception as e:
        print(str(e))
    #print(str(responses))
    plcontents = {}
    num = 1
    for i in range(len(responses['items'])):
        print(num,responses['items'][i]['snippet']['title'],\
                responses['items'][i]['snippet']['resourceId']['videoId'])
        plcontents[responses['items'][i]['id']] = (responses['items'][i])
        num += 1
    with open('/tmp/playlist_%s'%playlistid,'w') as fp:
        fp.write(json.dumps(plcontents,indent=3))
    return responses

def add_items_to_playlist(target):
    global plcontents
    playlistid = get_current_playlistid()
    get_video_ids(playlistid)  # this writes /tmp with current contents of playlist
    insertIds = []
    with open(args.items_file,'r') as fp:
        for line in fp.readlines():
            insertIds.append(line.strip())
    if os.path.exists('/tmp/playlist_%s'%playlistid):
        with open('/tmp/playlist_%s'%playlistid,'r') as fp:
            vids = (json.loads(fp.read()))
    else:
        vids = {}
    for insertId in insertIds:
        videoId = insertId.strip()
        # skip this videoId if alreaady present
        vpresent = False
        for key,value in vids.items():
            if vids[key]['contentDetails']['videoId'] == videoId:
                vpresent = True
        if vpresent:
            print("%s is already in playlist. . .SKIPPING"%insertId)
            continue
        print('inserting %s'%videoId)
        abody = """{
                "snippet": {
                        "playlistId":"%s", 
                        "position": 0,
                        "resourceId": {
                            "kind": "youtube#video",
                            "videoId": "%s"
                        }}}"""%(playlistid,videoId,)
        okjson = json.loads(abody)
        #print(json.dumps(okjson,indent=2))
        request = youtube.playlistItems().insert(
            part="snippet",
            body = okjson
        )
        try:
            responses = request.execute()
        except Exception as e:
            print(str(e))
            continue
        #print(str(responses))

def delete_video(list_index):
    global playlistid
    plid = get_current_playlistid()
    # refresh the list of videos in this playlist
    get_video_ids(plid)
    with open('/tmp/playlist_%s'%plid,'r') as fp:
        vids = (json.loads(fp.read()))
    num = 1
    my_index = {}
    for key,video in vids.items():
        print(num,key,vids[key]['contentDetails']['videoId'])
        my_index[str(num)] = key
        num += 1
    if not int(list_index) in range(1, len(vids)+1):
        print('Please use the Video index from the list displayed')
        return
    response = input('\n\nDo you want to delete %s? y/N'%my_index[list_index])
    if response != 'Y' and response != 'y':
        print('Aborting Delete')
        return
    id = my_index[str(list_index)]
    response = youtube.playlistItems().delete(id=id).execute()
    print(response)


def main():
   global args
   global target_playlist
   global youtube
   global current_plid
   current_plid = '/tmp/current_playlistid'
   # Following will generate credentials file if it is missing via "device" dumb Oauth method
   youtube = get_youtube_object()
    
   args = parse_args()
   if args.create:
       print('Create %s'%args.create)
       add_playlist(args.create)
       sys.exit(0)
   if args.list:
        print('list')
        my_playlists = get_my_playlists()
        num = 1
        for pl in my_playlists:
            print(num,pl)
            num += 1
        sys.exit(0)
   if args.delete:
        print('delete playlist by number %s'%args.delete)
        delete_playlist(args.delete)
        sys.exit(0)
   if args.items_file:
        my_playlists = get_my_playlists()
        target_playlist = my_playlists[0][0]
        print('target playlistlist: %s'%target_playlist)
        num = 1
        for pl in my_playlists:
            print(num,pl)
            num += 1
        add_items_to_playlist(target_playlist)
   if args.setPL != None:
        set_playlist_id(args.setPL)
        sys.exit(0)
   if args.xvideo:
        print('delete video by number %s'%args.delete)
        delete_video(args.xvideo)
        sys.exit(0)
   if args.videolist:
        plid = get_current_playlistid()
        print('List videos in playlist:%s'%plid)
        get_video_ids(plid)
        sys.exit(0)

    
if __name__ == "__main__":
    main()
# looks good: https://stackoverflow.com/questions/61702338/adding-multiple-videos-to-youtube-playlist-via-api-python
