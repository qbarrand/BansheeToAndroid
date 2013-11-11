#!/usr/bin/python
#-*- coding:utf-8 -*-

import os
import sys
import getopt

import btoa
from btoa.utils import *

version = 0.1

try:
    opts, args = getopt.getopt(sys.argv[1:], "ds", ["debug", "silent"])
except getopt.GetoptError as err:
    print str(err)
    sys.exit(2)

config = btoa.conf.BtoaConf(False, False, os.getenv("HOME"), version)


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
default_device_music_path = config.home + u"/.gvfs/mtp/Mémoire de stockage interne/Music/BansheeToAndroid/"
device = btoa.device.BtoaDev(config,default_device_music_path)


# Get playlist ID
default_playlist_name = "BansheeToAndroid"
playlist_id = db.get_playlist_id(default_playlist_name)


# Get the tracks stored into this playlist
db.get_tracks(playlist_id)
print str(len(db.tracks)) + " tracks in playlist " + default_playlist_name + "."

#
# Begin deleting old files
#

print "\nRemoving old tracks from device"

try:
    device.load_remote_db()
    remote_db_present = True
except:
    print "\tRemote database not found, I'll create one for you."
    device.scan_tracks()

    if config.debug:
        print "\t" + str(len(device.remote_db)) + " tracks detected."

    remote_db_present = False

if remote_db_present:
    todelete = device.get_todelete_tracks(db.tracks)
    device.delete_tracks(todelete)

    todelete = device.get_todelete_tracks(db.tracks)

    if len(todelete) > 0:
        print "\t" + len(todelete) + " old tracks to be deleted."

        if query_yes_no("\tProceed to deletion ?"):
            device.delete_tracks(todelete)
    else:
        print "\tNo old tracks to delete."

# End deleting old files


#
# Begin copying new files
#

# Get the tracks that are not on device
print "\nAdding new tracks to device"
print "\tResolving deltas... please wait."

tocopy = device.get_tocopy_tracks(db.tracks)

if len(tocopy) > 0:
    print "\t" + str(len(tocopy)) + " tracks not present on device."

    if query_yes_no("\tProceed to copy ?"):
        tocopy_details = db.get_tocopy_details(tocopy)
        device.copy_tracks(tocopy, tocopy_details)

        if remote_db_present:
            device.remote_db.extend(tocopy)
        else:
            device.remote_db = tocopy

        try:
            device.write_remote_db()
        except:
            print "\tApplication failed to write remote database."

else:
    print "\tAll tracks are already on the device."

print "All operations completed."
# End copying new files
