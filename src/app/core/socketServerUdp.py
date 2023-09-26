import socket
import json
from _thread import *
from datetime import datetime

CLIENTS = []

def handleClient (conn, addr, onReceiveCallback):
  global CLIENTS
  while True:
    if conn:
      message = conn.recv(1024)
      if message:
        print(f"SERVER -> RECEIVED: {message.decode()}\n")
        # run callback
        if onReceiveCallback: onReceiveCallback (message = message)
        # broadcast message
        for client in CLIENTS:
          client.send(message)
    else:
      print('no data from', addr)
  conn.close()

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
        self.sock.sendto(f"UDP SERVER: You are connected".encode(), addr)
        CLIENTS.append(addr)
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

      __mess = {
        "id": args["id"],
        "message": f"{args['message']}",
        "timestamp": f"{args['timestamp']}"
      }

      for client in CLIENTS:
        self.sock.sendto(f"{json.dumps(__mess)}".encode(), client)
    return self
  