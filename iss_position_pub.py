#!/usr/bin/python
# coding: utf8
 
############################################################
# Author Bachar Wehbi <me@bachwehbi.net>
# Copyright (c) 2013-2014 Beebotte <contact@beebotte.com>
# This program is published under the MIT License 
# Check http://opensource.org/licenses/MIT for details.
#
# This code uses the Beebotte API, you must have an account.
# You can register here: http://beebotte.com/register
#
# This program computes the position of the ISS in real-time
# and publishes it to Beebotte.
# 
# Use the pip package manager to install dependencies:
# $ pip install pyephem
# $ pip install beebotte
############################################################

import time
from beebotte import *
import ephem
import datetime
import urllib2
from math import degrees

### URL where we will fetch TLE data
url = "http://www.celestrak.com/NORAD/elements/stations.txt"

### Replace CHENNL_TOKEN with that of your channel's (this code assumes the channel name is "ISS")
CHANNEL_TOKEN = None
bbt = BBT(token = CHANNEL_TOKEN)
### Otherwise, use your Access and Secret keys to connect to Beebotte
### Replace ACCESS_KEY and SECRET_KEY with those of your account
# ACCESS_KEY = None
# SECRET_KEY = None
# bbt = BBT(ACCESS_KEY, SECRET_KEY)


### Change channel name and resource name as suits you
iss_position_resource = Resource(bbt, 'ISS', 'position')
iss = None
count = 0

def update_tle():
  global iss

  ### This is what TLE looks like. It will be updated every hour
  # line1 = "ISS (ZARYA)"
  # line2 = "1 25544U 98067A   16070.60802946  .00010558  00000-0  16731-3 0  9999"
  # line3 = "2 25544  51.6423 189.6478 0001642 260.2328 233.0609 15.53995147989640"

  try:
    ### Fetch and extract ISS TLE data
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    data = response.read()

    tle = data.split('\n')[0:3]
    if len(tle) >= 3:
      line1 = tle[0]
      line2 = tle[1]
      line3 = tle[2]
      iss = ephem.readtle(line1, line2, line3)

  except Exception as inst:
    print type(inst)     ### the exception instance
    print inst.args      ### arguments stored in .args
    print inst           ###

def run():
  global count
  update_tle()

  while True:

    ### update the TLE data once per hour
    if count > 3600:
      update_tle()
      count = 0
    count += 1

    try:
      ### compute the ISS position
      now = datetime.datetime.utcnow()
      iss.compute(now)
      print('longitude: %f - latitude: %f' % (degrees(iss.sublong), degrees(iss.sublat)))
      ### Send temperature to Beebotte
      iss_position_resource.publish({
        "timestamp": round(time.time()), 
        ### transform longitude and latitude to degrees
        "position": { 
          "long": degrees(iss.sublong), 
          "lat": degrees(iss.sublat) 
        } 
      })

    except Exception as inst:
      print type(inst)     ### the exception instance
      print inst.args      ### arguments stored in .args
      print inst           ###

    ### sleep some time
    time.sleep( 1 )
 
run()

