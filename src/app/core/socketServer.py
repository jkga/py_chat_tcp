import socket
import json
from datetime import datetime

class SocketServer ():

  def __init__ (self):
   
    self.host = "127.0.0.1"
    self.port = 5678
    self.onStartCallback = False
    self.onErrorCallback = False

  def _startServer (self):
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
      self.sock.bind((self.host, self.port))
      self.sock.listen (5)
    except Exception as e:
      if self.onErrorCallback:
        self.onErrorCallback(e)
        return  

    # run callback function
    if self.onStartCallback : self.onStartCallback()
    print("SERVER STARTED")

    # wait for connection
    while True:
      print('waiting for a connection')
      conn, addr = self.sock.accept()
      try:
        print('CONNECTED DEVICE:', addr)
        # broadcast to all connected device
        conn.sendall(f"SERVER -> CONNECTED: {addr}\r\n".encode())

        while True:
          message = conn.recv(1024)

          if message:
            print(f"SERVER -> RECEIVED: {message.decode()}\n")

            # broadcast message
            mess = {
              "id" : "s",
              "message" : f"{message.decode()}"
            }

            messJson = json.dumps(mess)

            conn.send(message)
          else:
            print('no data from', addr)
            break
      except Exception as e:
        # run callback function
        if self.onErrorCallback : self.onErrorCallback(e)    
      finally:
        # Clean up the connection
        conn.close()
        

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



#server = SocketServer ()
#server.start ()