#!/usr/bin/env python3

import random
import socket
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('localhost', 20000))
sock.listen()
print("Waiting for connect...")
client, addr = sock.accept()
i = 0
print("Start sending...")
while True:
  i += 1
  if random.random() > 0.3:
    msg = "  Finished message number " + str(i) + '\n'
  else:
    msg = "Unfini"
    client.send(msg.encode('ascii'))
    time.sleep(0.05*random.random())
    msg = "shed message number " + str(i) + '\n'
  client.send(msg.encode('ascii'))
  zzz = 0.01 *random.random()
  time.sleep(zzz)
  print("Round: " + str(i))

