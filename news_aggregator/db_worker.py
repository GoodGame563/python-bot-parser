import sqlite3

class Channels:
  def __init__(self, id, channel ):
    self.id = id
    self.channel = channel

class Key_Words:
  def __init__(self, word):
    self.word = word

class Rss_Channels:
  def __init__(self, link_short, link_long):
    self.link_short = link_short
    self.link_long = link_long


key_words = set()
rss_channels = set()




#cursor.execute('SELECT Word FROM key_words')
#select_words = cursor.fetchall()

#for s_word in select_words:
#  key_words.add(Key_Words(s_word[0]))

#cursor.execute('SELECT Link_short_channel, Link_long_channel FROM rss_channels')
#select_rss = cursor.fetchall()

#for s_rss in select_rss:
 # rss_channels.add(Rss_Channels(s_rss[0], s_rss[1]))



def return_channels():
    channels = {}
    connection = sqlite3.connect('../data/info.db')
    cursor = connection.cursor()

    cursor.execute('SELECT Id_channel, Link_channel FROM telegram_channels')
    select_channel = cursor.fetchall()

    for s_channel in select_channel:
        channels[s_channel[0]] = s_channel[1]
    connection.close()
    return channels


'''

for word in key_words:
  print(word.word)

for rss_channel in rss_channels:
  print(rss_channel.link_short, rss_channel.link_long)
  '''