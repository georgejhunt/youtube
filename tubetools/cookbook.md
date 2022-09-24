## Communicate the Easiest Setup
#### General observations
* The process of creating Zim files uses many packages (programs) that are not standard in a Linux installation image. The tools for generating zims have been developed over many years by many people. They have been tested, and probably work better, with somewhat older versions of things. Finding the right mix is part of the challenge.
* Libzim is documented to work with Ubuntu 20.04.
* youtube2zim has many references to using python 3.8.
* Ubuntu 22.04 comes with python 3.9, whereas Ubuntu 20.04 installs python 3.8 by default.
* When I tried to install python 3.8 on a rpi debian 11, I had lots of compatibility issues I had not had on Ubuntu 20.04.

#### Proposed strategy
1. All work with "tubetools" requires that you have a goodle account, and are signed in (this gives you access to playlists in your channel).
1. Download https://mirror.pit.teraswitch.com/ubuntu-releases/20.04.5/ (can use another close mirror from https://launchpad.net/ubuntu/+cdmirrors.
1. Load Ubuntu 20.04 iso on vbox -- assumes that most people can be running vbox on whatever machine they usse. To set up vbox:
    * Make sure to size the virtual disk (.vdi file) big enough.
    * Enable guest extensions (under "devices" tab)
    * Enable shared folders with the host.
    * Enable bidirectional use of "Shared Clipboard"
    * Turn on Network Bridging (Devices->Network->Network Settings->attached to "Bridged Adapter"
4. Create a virtual machine with a .vdi (virtual disk image) large enough to hold twice the expected size of the largest zim). I suggest that after Ubuntu 20.04 is running the way you want, that you create a clone, and use that, leaving the cloned image as backup and seed for another project or starting over. (Cloning takes less than a minute, but a full installation can take more than 30 minutes).
5. Install the build dependencies.

```
sudo apt update && sudo apt upgrade
mkdir -p /opt/iiab
sudo apt install wget build-essential libncursesw5-dev libssl-dev \
     libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev
sudo apt-get install ffmpeg curl libzim-dev python3-virtualenv unzip ssh
sudo virtualenv --python /usr/bin/python3.8 /opt/iiab/yt-venv
```
6. Enable the venv and install some python packages in it:
```
source /opt/iiab/yt-venv/bin/activate
pip3 install youtube_dl youtube2zim yt_dlp pytube zimscraperlib
pip install --upgrade google-api-python-client
pip install --upgrade google-auth-oauthlib google-auth-httplib2
pip install --upgrade oauth2client
```
7. get the assets that will be copied into each zim
```
cd /opt/iiab
git clone https://github.com/openzim/youtube2zim
cd /opt/iiab/youtube
./get_js_deps.sh
```
8. I created a bash script to remember the options I wanted to start the program with:
```
#!/bin/bash -x
# top level options for youtube2zim

source /opt/iiab/youtube_env/bin/activate
python3.8 ./youtube2zim --api-key $API_KEY --id PLs2auPpToJpaFnv9vrgKE0BabUH0-1zlM --type playlist --name first
```
9. A folder was created at /output containing a zim file with a size of 2.2GB. Not yet tested.
10. This cookbook is intended to focus on "setup". I will update it from time to time as I discover shortcomings as I work with a new vbox instance.
11. Look for specific "footprints" which will serve as examples of how to use tubetools.
12. Get clear in your mind the difference between loading system software (apt-get install ..) vs installing python programs in yor venv with "pip install"
13. Searching for system programs involves "apt-cache search (look for item)". https://pypi.org is really challenging to find the correct python package -- there are so many of them from authors unknown.
   
NOTE: As I often do, I started working on youtube2zim remotely over ssh.  But it turns out there is a lot of useful logging feedback that flows to dispay 0 (a local screen) that is not forwarded to a remote ssh session.
