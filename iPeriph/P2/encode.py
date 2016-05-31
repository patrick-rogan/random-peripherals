# simple encode file, see twitter.proto for the very simple Tweet schema

from pdb import set_trace
from json import loads
from itertools import imap
from twitter_pb2 import *
import time

tweets = Tweets()
with file('file.json', 'r') as f:
  for line in imap(loads, f):
    tweet = tweets.tweets.add()
    insert = tweet.insert
    insert.text = line['text']
    insert.id = line['id']
    insert.u_id = line['u_id']
    insert.u_name = line['u_name']
    insert.model = line['model']
    insert.created_at = line['created_at']
    insert.created_at = time.strftime('%m/%d/%Y', 
				time.strptime(line['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))

with file('twitter.pb', 'w') as f:
  f.write(tweets.SerializeToString())


