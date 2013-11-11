#!/usr/bin/python
#-*- coding:utf-8 -*-

## @package btoa_db
#
# BansheeToAndroid's database-related elements and services.

import sqlite3
import urllib
import sys

## 
#
#
class BtoaDb:

    ## Constructor.
    def __init__(self, config, db_path):
        self.config = config
        self.path = db_path

        self.tracks = []


    ## Connect to the database.
    def _connect(self):
        try:
            self._connection = sqlite3.connect(self.path)
            self._c = self._connection.cursor()

        except sqlite3.OperationalError:
            print 'The connection to the Banshee database could not be initiated. Exiting.'
            sys.exit(1)


    ## Get the PlaylistID of the specified playlist name. 
    #
    #
    def get_playlist_id(self, playlist_name):
        try:
            self._connect()

            args = (playlist_name, )
            self._c.execute("SELECT PlaylistID FROM CorePlaylists WHERE Name like ?;", args)

            playlist_id = self._c.fetchone()[0]

            if self.config.debug:
                print "Playlist " + playlist_name + " has ID #" + str(playlist_id) + "."

            self._close()

            return playlist_id

        except sqlite3.OperationalError:
            print "Playlist " + playlist_name + " was not found in your Banshee database. Please create this playlist and re-run this app."
            sys.exit(1)


    ## Get a list of the tracks in the specified playlist.
    #
    # Details
    def get_tracks(self, playlist_id):
        try:
            self._connect()

            args = (playlist_id, )
            self.tracks = self._c.execute('SELECT TrackID FROM CorePlaylistEntries WHERE PlaylistID = ?;', args).fetchall()
        
            self._close()

        except sqlite3.OperationalError:
            print "Could not fetch tracks in the playlist from the Banshee database."
            if self.config.debug:
                print "DEBUG Playlist ID : " + playlist_id
            sys.exit(1)


    def get_tocopy_details(self, tocopy):
        self._connect()

        tocopy_details = []

        for track in tocopy:
            args = (track[0], )

            if self.config.debug:
                print "\tFetching details from database for track #" + str(track[0]) +"..."

            try:
                track_details = self._c.execute("SELECT Uri, Title FROM CoreTracks WHERE TrackID = ?;", args).fetchone()
                track_path = urllib.unquote(track_details[0])[7:].encode('latin1')
                track_title = urllib.unquote(track_details[1])
                tocopy_details.append([track_path, track_title])
                print "done."
            except:
                print "FAIL."
                sys.exit(2)

        self._close()

        return tocopy_details




    ## Close the connection to the database.
    #
    #
    def _close(self):
        try:
            self._connection.close()
        except:
            print "Connection to the database could not be closed. This could be bad, exiting."
            sys.exit(1)
