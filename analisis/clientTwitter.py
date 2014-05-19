#!/usr/bin/env python
#encoding:latin-1
import zmq
from datetime import datetime
import os
from twitter import *
from twitter.cmdline import CONSUMER_KEY, CONSUMER_SECRET

MY_TWITTER_CREDS = os.path.expanduser('~/.twitter_oauth')

oauth_token, oauth_secret = read_token_file(MY_TWITTER_CREDS)

twitter = Twitter(auth=OAuth( oauth_token, oauth_secret, CONSUMER_KEY, CONSUMER_SECRET))


context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://raspi:5000")
socket.setsockopt(zmq.SUBSCRIBE, "ecobici1 bici")
while True:
    d = socket.recv().split()
 # Now work with Twitter

    mensaje = datetime.now().strftime("Me parece que vi una bici a las %H:%M:%S")
    print "Twiteando: {msg}".format(msg=mensaje)
    twitter.statuses.update(status=mensaje)
