#!/usr/bin/python2

import boat
import collections

START='__________..START'
STOP='__________..STOP'
brain = collections.defaultdict(set)

def add_to_brain(msg):
  words = [START] + msg.split() + [STOP]
  

def onmsg(boat, user, channel, msg):
  add_to_brain(msg)
  boat.msg(channel, "lol, you said: {}".format(msg))

def main():
  config = boat.BoatConfig()
  config.nickname = 'nullbutt'
  config.channels = ['#nullren', '#nullboat']

  # callbacks
  config.onmsg = onmsg

  boat.run(config)

if __name__ == '__main__':
  main()
