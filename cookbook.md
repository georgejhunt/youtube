## Communicate the Easiest Setup
#### General observations
* Libzim is documented to work with Ubuntu 20.04.
* youtube2zim has many references to using python 3.8.
* Ubuntu 22.04 comes with python 3.9, whereas Ubuntu 20.04 installs python 3.8.
* When I tried to install python 3.8 on a rpi debian 11, I had lots of compatibility issue I had not hade on Ubuntu 20.04.

#### Proposed strategy
1. Load Ubuntu 20.04 iso on vbox -- assumes that most people can be vbox running on whatever machinne they usse.
2. Download https://mirror.pit.teraswitch.com/ubuntu-releases/20.04.5/ (can use another close mirror from https://launchpad.net/ubuntu/+cdmirrors.
3. Create a virtual machine with a .vdi (virtual disk image) large enough to hold twice the expected size of the largest zim). I suggest that after Ubuntu 20.04 is running the way you want, that you create a clone, and us that, leaving the cloned image as backup and seed for other projects. (Cloning takes less than a minute, but a full installation can take more than 30 minutes).
4. Install the build dependencies.

```
sudo apt update && sudo apt upgrade
sudo apt install wget build-essential libncursesw5-dev libssl-dev \
     libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev
sudo apt-get install ffmpeg curl libzim-dev
sudo virtualenv --python /usr/bin/python3.8 /opt/iiab/youtube-venv
```
5. Enable the venv and install some python packages in it:
```
source /opt/iiab/youtube_venv/bin/activate
pip3 install youtube_dl youtube2zim yt_dlp
```
6. get the assets that will be copied into each zim
```
./get_js_deps.sh
```
7. I created a bash script to remember the options I wanted to start the program with:
```
#!/bin/bash -x
# top level options for youtube2zim

source /opt/iiab/youtube_env/bin/activate
python3.8 ./youtube2zim --api-key $API_KEY --id PLs2auPpToJpaFnv9vrgKE0BabUH0-1zlM --type playlist --name first
```
8. A folder was created at /output containing a zim file with a size of 2.2GB. Not yet teste.
