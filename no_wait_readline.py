#!/usr/bin/env python3

import errno
import io
import random
import socket
import time

from select import select

def is_ready(sockets):
  """
  returns list of all the sockets that are available for a read
  nonblocking. returns empty list if none are ready
  """
  # nonblocking check if read is possible on socket
  ready, _, _ = select([sockets], [], [], 0.0)
  return ready

class LineBuffer:

  def __init__(self):
    self.buf = bytearray()

  def readlines(self, sock, encoding='ascii'):
    """
    readlines on socket
    returns list of lines, or empty list if none are available
    """
    data_available = is_ready(sock)
    if(data_available):
      while True:
        data = sock.recv(4096)
        self.buf.extend(data)
        more = is_ready(sock)
        if(not more):
          lines = self.buf.decode(encoding)
          lst_lines = lines.splitlines()
          if '\n' == lines[-1]:
            self.buf = bytearray() # clear buffer
            return lst_lines
          else: # unfinished message
            # keep unfinished message in buffer
            self.buf = bytearray(lst_lines[-1].encode(encoding))
            return lst_lines[:-1] # return all finished messages
    else:
      return []


"""
Script
"""

sock = socket.socket(socket.AF_INET,
                     socket.SOCK_STREAM)
sock.connect(('localhost', 20000))
sock.setblocking(False)
line_buffer = LineBuffer()

while True:
  lines = line_buffer.readlines(sock)
  if lines:
    for line in lines:
      print("\nSINGLE LINE: " + str(line))
  else:
    print('.', end='')
    time.sleep(0.01)
