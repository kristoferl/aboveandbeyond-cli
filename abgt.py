#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import re
import subprocess
import urllib2
from subprocess import Popen, PIPE, STDOUT

print "    _   _                   __       ___                       _ "
print "   /_\ | |__  _____ _____  / _|___  | _ ) ___ _  _ ___ _ _  __| |"
print "  / _ \| '_ \/ _ \ V / -_) > _|_ _| | _ \/ -_) || / _ \ ' \/ _` |"
print " /_/ \_\_.__/\___/\_/\___| \_____|  |___/\___|\_, \___/_||_\__,_|"
print "                                              |__/               "

FEED_URL = "http://static.aboveandbeyond.nu/grouptherapy/podcast.xml"
SUBTITLE_TAG = "{http://www.itunes.com/dtds/podcast-1.0.dtd}subtitle"
ENCLOSURE_TAG = "enclosure"
MUSIC_URL_ATTR = "url"
EPISODE_TMP_LOCATION = "/tmp/abgt"
whitespacePattern = re.compile(r'\s+')
episodes = []
items = []

def downloadFeed():
  global items
  print "Downloading feed ..."
  feed = urllib2.urlopen(FEED_URL)
  feedData = feed.read()
  root = ET.fromstring(feedData)
  items = root.iter('item')

def extractEpisodes():
  for item in items:
    episode = {}
    for child in item:
      if child.tag == SUBTITLE_TAG:
        # Some subtitles contains a newline character and multiple whitespace characters
        episode['title'] = sentence = re.sub(whitespacePattern, ' ', child.text)
      if child.tag == ENCLOSURE_TAG:
        episode['url'] = child.attrib[MUSIC_URL_ATTR]
    episodes.append(episode)

def showEpisodes():
  global episodes
  i = 0;
  for episode in episodes:
    print '{0:3d} - {1}'.format(i, episode['title'])
    i = i+1;

def chooseEpisode():
  episodeNumber = raw_input("Choose episode: ")
  episode = episodes[int(episodeNumber)]
  playEpisode(episode)

def playEpisode(episode):
  print "Downloading: {0}".format(episode['title'])
  subprocess.call(["curl", "--location", "-#", "-o", EPISODE_TMP_LOCATION, episode['url']])
  print "Playing: {0}".format(episode['title'])
  subprocess.call(["afplay", "-q", "1", EPISODE_TMP_LOCATION])
  chooseEpisode()

downloadFeed()
extractEpisodes()
showEpisodes()
chooseEpisode()
