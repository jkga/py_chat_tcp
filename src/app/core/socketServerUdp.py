import socket
import json
from _thread import *
from datetime import datetime

CLIENTS = []

class SocketServerUdp ():

  def __init__ (self):
    global CLIENTS

    self.host = "0.0.0.0"
    self.port = 5678
    self.onStartCallback = False
    self.onErrorCallback = False
    self.onErrorCallback = False
    self.sock = False
    self.clients = []
  
  def _startServer (self):

    self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

    try:
      self.sock.bind((self.host, self.port))

    except Exception as e:
      if self.onErrorCallback:
        self.onErrorCallback(e)
        return  

    # run callback function
    if self.onStartCallback : self.onStartCallback()
    print("SERVER STARTED")
    
    while True:

      mess, addr = self.sock.recvfrom(1024)
    
      try:
        print('CONNECTED DEVICE:', addr)
        if mess:
          print(f"UDP SERVER -> Received from {addr}: {mess.decode()}\n")
          self.sock.sendto(mess, addr)
        else:
          self.sock.sendto(f"UDP SERVER: You are connected".encode(), addr)

        CLIENTS.append(addr)

        if (self.receivedCallback): self.receivedCallback (message = mess)  
      except Exception as e:
        # run callback function
        if self.onErrorCallback : self.onErrorCallback(e) 
        print(e)
        break

  def onReceive(self, **args):
    if "callback" in args:
      self.receivedCallback = args["callback"]
    return self      

  def start (self):
    self._startServer ()
    return self

  def onStart (self, **args):
    if "callback" in args:
      self.onStartCallback = args["callback"]
    return self
  
  def onError(self, **args):
    if "callback" in args:
      self.onErrorCallback = args["callback"]
    return self
  
  def getHostName (self):
    return self.host

  def getPort (self):
    return self.port
  
  def close (self):
    try:
      self.sock.close()
    except Exception as e:
      pass

  def sendMessage (self, **args):
    if "message" in args:
      print(f"SERVER:UDP->broadcasting: {args['message']}")
      
      name = ""
      if "name" in args:
          name = args['name']

      __mess = {
        "id": args["id"],
        "name": f"{name}",
        "message": f"{args['message']}",
        "timestamp": f"{args['timestamp']}"
      }

      # get unique client to prevent sending multiple message
      clientsList = set(CLIENTS)

      for client in clientsList:
        self.sock.sendto(f"{json.dumps(__mess)}".encode(), client)
    return self
  