#!/usr/bin/python
#-*- coding:utf-8 -*-

import shutil
import os

class BtoaDev:
    
    def __init__(self, dev_music_path):
        self._dev_music_path = dev_music_path


    def get_remote_db(dev_path):
        if not os.path.exists(dev_path + ".BansheeToAndroid"):
            raise Exception("Could not find " + dev_path + ".BansheeToAndroid")

        tracks = []

        file = open(dev_path + ".BansheeToAndroid")


        return tracks


    def get_tocopy_tracks(self, tracks):
        tocopy = []

        for track in tracks:
            track_id = track[0]
            track_path_device = self._dev_music_path + str(track_id) + ".mp3"

            if not os.path.exists(track_path_device):
                tocopy.append([track_id, track_path_device])

        return tocopy


    def copy_tracks(self, tocopy, tocopy_details):
        i = 0        

        for track in tocopy:
            print "Copying " + tocopy_details[i][1] + " (" + str(i + 1) + "/" + str(len(tocopy)) + ")...",
            shutil.copyfile(tocopy_details[i][0], track[1])
            print "done."    

            i += 1
