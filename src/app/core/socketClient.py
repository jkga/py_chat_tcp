import socket
import random
import json
from functools import partial
from datetime import datetime

class SocketClient ():

  def __init__ (self):
    self.host = "127.0.0.1"
    self.port = 5678
    self.sock = socket.socket()

    # default ID
    self.currentDateTime = datetime.now().strftime("%d%m%Y%H%M%S")
    self.serverUniqueId = f"{self.currentDateTime}{random.random()}"

    self.connectedCallback = False
    self.connectedCallbackArgs = False
    self.message = False
  
  def setServerId (self, id):
    self.serverUniqueId = f"{id}"
    return self

  def _startClient (self):
    self.sock.connect ((self.host, self.port))
  
    # callback
    if (self.connectedCallback): self.connectedCallback ()  

    while True:
      try:
        mess = self.sock.recv(1024)
        if mess:
          print(f"CLIENT -> Received from Server: {mess.decode()}\n")
          print(f"{mess}")
          # callback
          if (self.receivedCallback): self.receivedCallback (message = mess)  
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
      print(f"CLIENT->sending: {args['message']}")

      __mess = {
        "id": self.serverUniqueId,
        "message": f"{args['message']}"
      }

      self.sock.sendall(f"{json.dumps(__mess)}".encode())
    return self
  
  def start (self):
    #threading.Thread(target=self._startClient).start()
    self._startClient ()
    return self
  
  def disconnect (self):
    try:
      self.sock.shutdown ()
    except Exception as e:
      pass