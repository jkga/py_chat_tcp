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

class SocketServer ():

  def __init__ (self):
    global CLIENTS
    global CONFIG

    self.host = ""
    self.port = 5678
    self.onStartCallback = False
    self.onErrorCallback = False
    self.onErrorCallback = False
    self.sock = False
    self.clients = []
  
  def _startServer (self):

    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

    try:
      self.sock.bind((self.host, self.port))
      self.sock.listen ()

    except Exception as e:
      if self.onErrorCallback:
        self.onErrorCallback(e)
        return  

    # run callback function
    if self.onStartCallback : self.onStartCallback()
    print("SERVER STARTED")
    
    while True:
      print('waiting for a connection')
      conn, addr = self.sock.accept()
    
      try:
        print('CONNECTED DEVICE:', addr)

        # broadcast to all connected device
        conn.send(f"SERVER -> CONNECTED: {addr}\r\n".encode())
        start_new_thread (handleClient, (conn, addr, self.receivedCallback))

        # add to connection pool for sending broadcast messages
        CLIENTS.append(conn)

      except Exception as e:
        # run callback function
        if self.onErrorCallback : self.onErrorCallback(e) 
        print(e)
        break

    self.sock.close()

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
      print(f"TCP SERVER->broadcasting: {args['message']}")
      
      name = ""
      senderId = ""

      if "name" in args: name = args['name']
      if "senderId" in args: senderId = args['senderId']

      __mess = {
        "id": args["id"],
        "senderId": senderId,
        "name": f"{name}",
        "message": f"{args['message']}",
        "timestamp": f"{args['timestamp']}"
      }

      print(json.dumps(__mess))

      for client in CLIENTS:
        client.send(f"{json.dumps(__mess)}".encode())
    return self
  