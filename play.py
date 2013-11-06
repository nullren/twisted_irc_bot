from twisted.words.protocols import irc

from twisted.internet import reactor, protocol, ssl
from twisted.python import log

import time, sys

class Logger:
  def __init__(self, filename):
    self.filename = filename
    self.fh = open(filename, "a")

  def log(self, msg):
    timestamp = time.strftime("[%H:%M:%S]",
        time.localtime(time.time()))
    self.fh.write('{} {}\n'.format(timestamp, msg))
    self.fh.flush()

  def close(self):
    self.fh.close()

class Boat(irc.IRCClient):

  def __init__(self, factory):
    self.factory = factory

    self.nickname = self.factory.conf.nickname
    self.realname = self.factory.conf.realname
    self.username = self.factory.conf.username

  ## connection
  def connectionMade(self):
    irc.IRCClient.connectionMade(self)
    self.logger = Logger(self.factory.conf.logfile)
    self.logger.log("[connected at {}]"
        .format(time.asctime(time.localtime(time.time()))))

  def connectionLost(self, reason):
    irc.IRCClient.connectionLost(self, reason)
    self.logger.log("[disconnected at {}]"
        .format(time.asctime(time.localtime(time.time()))))
    self.logger.close()

  def signedOn(self):
    for channel in self.factory.conf.channels:
      self.join(channel)

  def joined(self, channel):
    self.logger.log("[I have joined {}]".format(channel))

  def privmsg(self, user, channel, msg):
    user = user.split('!', 1)[0]
    self.logger.log("<{} to {}> {}".format(user, channel, msg))

    # pm
    if channel == self.nickname:
      return

  def action(self, user, channel, msg):
    user = user.split('!', 1)[0]
    self.logger.log("* {0} {2} (on {1})".format(user, channel, msg))

  def irc_NICK(self, prefix, params):
    old_nick = prefix.split('!')[0]
    new_nick = params[0]
    self.logger.log("{} is now known as {}".format(old_nick, new_nick))

class BoatConfig:
  nickname = "BoatBot"
  realname = "BoatBot"
  username = "BoatBot"

  server = "irc.starfyre.org"
  port = 6697
  ssl = True

  channels = []

  logfile = None

class BoatFactory(protocol.ClientFactory):
  def __init__(self, config):
    self.conf = config

  def buildProtocol(self, addr):
    p = Boat(self)
    return p

  def clientConnectionLost(self, connector, reason):
    connector.connect()

  def clientConnectionFailed(self, connector, reason):
    print("connection failed: ", reason)
    reactor.stop()

if __name__ == '__main__':

  # debug messages to the stdout
  log.startLogging(sys.stdout)

  config = BoatConfig()
  config.nickname = "nullboat"
  config.channels = ["#nullren", "#nullboat"]
  config.logfile = "nullboat.log"

  factory = BoatFactory(config)
  reactor.connectSSL("irc.starfyre.org", 6697, factory,
      ssl.CertificateOptions())
  reactor.run()
