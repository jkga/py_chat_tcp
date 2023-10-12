import Pyro5.api
import json
import threading
from functools import partial
from core.ui.client.ChatWindow import *

@Pyro5.api.expose
class PyroServer:
  def __init__ (self, *args, **kwargs):
    print ('Intializing pyro Object')
    self.window = None
    self.clients = {}
    self.pyroAddress = ''
    self.onConnect = None
    self.callback = None
    self.pyroInstance = None
    self.chatWindow = None

    if 'window' in kwargs: self.window = kwargs["window"]


  def register(self, *args, **kwargs):
    print('------regestering--------')

    # prompt
    self.prompt = True

    # return data
    data = {"ipAddress": self.window.ipAddress, "method": "self", "clientName" :kwargs['name']}
    #data = json.dumps(data, ensure_ascii=False, default=lambda o: o.__dict__)
    
    # show prompt if not exists
    # method used is part of the mainloop to be able to call other functions
    if not kwargs["name"] in self.clients:
      self.window.openInvitePromptWindow(name = kwargs['name'], onReject = partial(self.onReject, name = kwargs['name']), onAccept = partial(self.onAccept, data = data))
    
     # add to clients list
    self.clients[kwargs['name']] = {
      "pyroInstance": kwargs['name']
    }

    return data
  
  def onReject (self, name):
    del self.clients[name]
    print (f"Rejected {name}")
  
  @Pyro5.api.oneway
  def onAccept (self, data):
    print('---accepted----')
    print(data)

    # show new chat window to the server
    self.chatWindow = ChatWindow(root = self, pyroInstance = self.callback, isRunningOnServer = True)
    self.chatWindow.setClientName(data["clientName"])
    self.chatWindow.show()

    # show chat window to the client
    self.callback._pyroClaimOwnership() 
    self.callback.showChatBox ()

  def run(self, *args, **kwargs):
    print ('----connected-----')
    return self.register (name = kwargs["name"])

  # executed in the server by client's request
  def sendMessage(self, *args, **kwargs):
    mess = kwargs["message"]
    self.chatWindow.receiveMessage (message = mess)
    print("--------Received----------")
    print(mess)
    print("-------------------------\n")
    return mess
  
  def getPyroAddress (self):
    return self.pyroAddress

  def addCallback (self, func):
    print ('--- SERVER: adding callback----')
    self.callback = func
  
  def startServer (self):
    # Start server and expose the TimeTaggerRPC class
    with Pyro5.api.Daemon(host='', port=5681) as daemon:
        # Register class with Pyro
        self.pyroInstance = daemon
        addr = daemon.register(self, 'PyroServer')
        self.pyroAddress = addr
        print(addr)
        if self.onConnect: self.onConnect (self)
        daemon.requestLoop()
