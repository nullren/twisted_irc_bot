#!/usr/bin/python2

import boat
import collections
import random

brain = collections.defaultdict(lambda : collections.defaultdict(int))
START='___START'
STOP='___STOP'
TRAININGDATA='para_per_line.txt'

def add_to_brain(msg):
  prev = START
  for word in msg.split():
    brain[prev][word] += 1
    prev = word
  brain[prev][STOP] += 1

def pick_brain(key, out, length):
  if length < 1:
    return out
  word = brain[key].keys()[int(random.random() * len(brain[key]))]
  if word == STOP:
    return out
  return pick_brain(word, out + [word], length - 1)

def get_sentence(maxlength=50):
  words = pick_brain(START, [], maxlength)
  return ' '.join(words)

def onmsg(boat, user, channel, msg):
  add_to_brain(msg)
  if msg.find(boat.factory.conf.nickname) >= 0:
    boat.msg(channel, get_sentence())

def load_brain():
  f = open(TRAININGDATA)
  for line in iter(f):
    add_to_brain(line)
  f.close()

def main():
  config = boat.BoatConfig()
  config.nickname = 'nullboat'
  config.channels = ['#stapler']
  config.server = 'irc.freenode.net'

  # callbacks
  config.onmsg = onmsg

  boat.run(config)

if __name__ == '__main__':
  main()
