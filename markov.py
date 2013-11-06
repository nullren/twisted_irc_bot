#!/usr/bin/python2

import boat

def onmsg(boat, user, channel, msg):
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
