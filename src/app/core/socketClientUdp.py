import socket
import random
import json
from functools import partial
from datetime import datetime


class SocketClientUdp ():

  def __init__ (self):
    self.host = ""
    self.port = 5678
    self.sock = False

    # default ID
    self.currentDateTime = datetime.now().strftime("%d%m%Y%H%M%S")
    self.serverUniqueId = f"{self.currentDateTime}{random.random()}"

    self.connectedCallback = False
    self.connectedCallbackArgs = False
    self.receivedCallback = False
    self.message = False
  
  def setServerId (self, id):
    self.serverUniqueId = f"{id}"
    return self
  
  def setHost (self, ip):
    self.host = ip
    return self

  def _startClient (self):

    self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print('UDP CLIENT STARTED')

    self.sock.sendto(f"Hi!".encode(), (self.host, self.port))

    # callback
    if (self.connectedCallback): self.connectedCallback () 

    while True:
      try:
        mess, addr = self.sock.recvfrom(1024)
      
        if mess:
          print(f"CLIENT -> Received from {addr}: {mess.decode()}\n")
          # callback
          if (self.receivedCallback): self.receivedCallback (message = mess, address = addr)  
      except Exception as e:
        print(f"error: {e}")

  def onConnect(self, **args):
    if "callback" in args:
      self.connectedCallback = args["callback"]
      self.connectedCallbackArgs = args
    return self
  
  def onReceive(self, **args):
    if "callback" in args:
      self.receivedCallback = args["callback"]
      self.receivedCallbackArgs = args
    return self
  
  def sendMessage (self, **args):
    if "message" in args:
      print(f"CLIENT:UDP->sending: {args['message']}")
      
      name = ""
      senderId = ""
      ipAddress = ""

      if "name" in args: name = args['name']
      if "senderId" in args: senderId = args['senderId']
      if "ipAddress" in args: ipAddress = args['ipAddress']

      __mess = {
        "id": self.serverUniqueId,
        "senderId": senderId,
        "name": f"{name}",
        "message": f"{args['message']}",
        "timestamp": f"{datetime.now().strftime('%B %d, %Y %I:%M%p')}",
        "ipAddress": f"{ipAddress}"
      }

      self.sock.sendto(f"{json.dumps(__mess)}".encode(), (self.host, self.port))
    return self
  
  def start (self):
    self._startClient ()
    return self
  
  def disconnect (self):
    try:
      self.sock.shutdown ()
    except Exception as e:
      pass