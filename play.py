from twisted.words.protocols import irc

from twisted.internet import reactor, protocol, ssl
from twisted.python import log

import time, sys

class Logger:
  def __open_file(self):
    self.fh = open(self.file, "a")

  def __init__(self, file):
    self.file = file
    self.__open_file()

  def log(self, msg):
    timestamp = time.strftime("[%H:%M:%S]",
        time.localtime(time.time()))
    self.fh.write('{} {}\n'.format(timestamp, msg))
    self.fh.flush()

  def close(self):
    self.fh.close()

class LogBot(irc.IRCClient):
  nickname = "nullboat"
  realname = "nullrens boat"
  username = "nullboat"

  ## connection
  def connectionMade(self):
    irc.IRCClient.connectionMade(self)
    self.logger = Logger(self.factory.filename)
    self.logger.log("[connected at {}]"
        .format(time.asctime(time.localtime(time.time()))))

  def connectionLost(self, reason):
    irc.IRCClient.connectionLost(self, reason)
    self.logger.log("[disconnected at {}]"
        .format(time.asctime(time.localtime(time.time()))))
    self.logger.close()

  def signedOn(self):
    for channel in self.factory.channels:
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

class BotFactory(protocol.ClientFactory):
  def __init__(self, channels, filename):
    self.channels = channels
    self.filename = filename

  def buildProtocol(self, addr):
    p = LogBot()
    p.factory = self
    return p

  def clientConnectionLost(self, connector, reason):
    connector.connect()

  def clientConnectionFailed(self, connector, reason):
    print("connection failed: ", reason)
    reactor.stop()

if __name__ == '__main__':
  log.startLogging(sys.stdout)

  factory = BotFactory(['#nullren'], "nullboat.out")

  reactor.connectTCP("irc.starfyre.org", 6667, factory)
  reactor.run()
