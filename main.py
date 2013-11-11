#!/usr/bin/python
#-*- coding:utf-8 -*-

import os
import sys
import getopt

import btoa
from btoa.utils import *

try:
    opts, args = getopt.getopt(sys.argv[1:], "ds", ["debug", "silent"])
except getopt.GetoptError as err:
    print str(err)
    sys.exit(2)

config = btoa.conf.BtoaConf(False, False, os.getenv("HOME"))


# Arguments handling
for o, a in opts:
    if o in ("-s", "--silent"):
        config.silent = True
    elif o in ("-d", "--debug"):
        config.debug = True


# Create Banshee database
default_db_path = config.home + '/.config/banshee-1/banshee.db'
db = btoa.database.BtoaDb(config, default_db_path)


# Create device
default_device_music_path = config.home + u"/.gvfs/mtp/Mémoire de stockage interne/Music/"
device = btoa.device.BtoaDev(default_device_music_path)


# Get playlist ID
default_playlist_name = "BansheeToAndroid"
playlist_id = db.get_playlist_id(default_playlist_name)


# Get the tracks stored into this playlist
tracks = db.get_tracks(playlist_id)
print str(len(tracks)) + " tracks in playlist " + default_playlist_name + "."

#
# Begin deleting old files
#


# End deleting old files


#
# Begin copying new files
#

# Get the tracks that are not on device
tocopy = device.get_tocopy_tracks(tracks)

if len(tocopy) > 0:
    
    if config.debug:
        print str(len(tocopy)) + " tracks not present on device."

    if query_yes_no("Proceed to copy ?"):
        tocopy_details = db.get_tocopy_details(tocopy)
        device.copy_tracks(tocopy, tocopy_details)
else:
    print "All tracks are already on the device."

# End copying new files
