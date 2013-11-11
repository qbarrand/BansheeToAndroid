#!/usr/bin/python
#-*- coding:utf-8 -*-

import json
import shutil
import os

class BtoaDev:
    
    def __init__(self, config, dev_music_path):
        self.config = config
        self._dev_music_path = dev_music_path
        
        self.remote_db = []

        if not os.path.exists(self._dev_music_path):
            if self.config.debug:
                print "Remote directory " + self._dev_music_path + " not found; creating..."
            os.mkdir(self._dev_music_path)


    def get_todelete_tracks(self, db_tracks):
        self.load_remote_db()

        todelete = []

        for r_track in self.remote_db:
            for l_track in db_tracks:
                if r_track == l_track:
                    todelete.append(r_track)
                    break

        return todelete


    def delete_tracks(self, todelete):
        for track in todelete:
            shutil.rm(self._dev_music_path + str(track_id) + ".mp3")


    def get_tocopy_tracks(self, tracks):
        tocopy = []
        i = 0

        for track in tracks:
            if self.config.debug:
                print "\tResolving track " + str(i + 1) + " / " + str(len(tracks)) +" :",

            track_id = track[0]
            track_path_device = self._dev_music_path + str(track_id) + ".mp3"

            if not os.path.exists(track_path_device):
                tocopy.append([track_id, track_path_device])

                if self.config.debug:
                    print "track does not exists on device."
            else:
                if self.config.debug:
                    print "track already exists on device."

            i += 1

        return tocopy


    def copy_tracks(self, tocopy, tocopy_details):
        i = 0        

        for track in tocopy:
            print "\t[" + str(i + 1) + " / " + str(len(tocopy)) + "] Copying " + tocopy_details[i][1] + "...",
            shutil.copyfile(tocopy_details[i][0], track[1])
            print "done."    

            i += 1


    def scan_tracks(self):
        for track in os.listdir(self._dev_music_path):
            if track.endswith(".mp3"):
                self.remote_db.append(int(track[:-4]))


    def load_remote_db(self):
        device_json_db =  json.loads(open(self._dev_music_path + "/.BansheeToAndroid").read())
        self.remote_db = device_json_db["tracks"]

            
    def write_remote_db(self):
        remote_db = {}

        remote_db["version"] = self.config.version
        remote_db["tracks"] = self.remote_db

        with open(self._dev_music_path + "/.BansheeToAndroid", 'w') as outfile:
            json.dump(remote_db, outfile)