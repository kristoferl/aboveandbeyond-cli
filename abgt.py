#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import re
import subprocess
import urllib2

print "    _   _                   __       ___                       _ "
print "   /_\ | |__  _____ _____  / _|___  | _ ) ___ _  _ ___ _ _  __| |"
print "  / _ \| '_ \/ _ \ V / -_) > _|_ _| | _ \/ -_) || / _ \ ' \/ _` |"
print " /_/ \_\_.__/\___/\_/\___| \_____|  |___/\___|\_, \___/_||_\__,_|"
print "                                              |__/               "

FEED_URL = "http://static.aboveandbeyond.nu/grouptherapy/podcast.xml"
SUBTITLE_TAG = "{http://www.itunes.com/dtds/podcast-1.0.dtd}subtitle"
ENCLOSURE_TAG = "enclosure"
MUSIC_URL_ATTR = "url"
whitespacePattern = re.compile(r'\s+')
episodes = []
items = []


def download_feed():
    global items
    print "Downloading feed ..."
    feed = urllib2.urlopen(FEED_URL)
    feed_data = feed.read()
    root = ET.fromstring(feed_data)
    items = root.iter('item')


def extract_episodes():
    for item in items:
        episode = {}
        for child in item:
            if child.tag == SUBTITLE_TAG:
                # Some subtitles contains a newline character and multiple whitespace characters
                episode['title'] = re.sub(whitespacePattern, ' ', child.text)
            if child.tag == ENCLOSURE_TAG:
                episode['url'] = child.attrib[MUSIC_URL_ATTR]
        episodes.append(episode)


def show_episodes():
    global episodes
    i = 0
    for episode in episodes:
        print '{0:3d} - {1}'.format(i, episode['title'])
        i += 1


def choose_episode():
    episode_number = raw_input("Choose episode: ")
    episode = episodes[int(episode_number)]
    play_episode(episode)


def play_episode(episode):
    print "Playing: {0}".format(episode['title'])
    subprocess.call(["mplayer", "-vo", "null", "-really-quiet", episode['url']])
    choose_episode()

download_feed()
extract_episodes()
show_episodes()
choose_episode()
