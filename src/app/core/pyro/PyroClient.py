import Pyro5.api
import netifaces as nic
from Pyro5.api import Daemon
from core.ui.client.ChatWindow import *

Pyro5.api.config.COMMTIMEOUT = 0.5

class CallbackHandler:

  def __init__ (self, *args, **kwargs):
    self.clientName = kwargs["clientName"]
    self.daemon = kwargs["daemon"]

  @Pyro5.api.expose
  @Pyro5.api.callback
  def showChatBox(self):
    print("-----running callback in client-------")
    # show new chat window to the server
    chatWindow = ChatWindow(root = self)
    chatWindow.setClientName(self.clientName)
    chatWindow.show()

    # close daemon to allow reusing the address allocation
    print("-------closing daemon------")
    self.daemon.shutdown ()


class PyroClient:
  def __init__ (self, *args, **kwargs):

    print ('----Pyro Client Object Initialized--')
    self.ipAddress = None
    self.server = None
    self.clientName = "anon"

    if "ipAddress" in kwargs: self.ipAddress = kwargs["ipAddress"]
    if "clientName" in kwargs: self.clientName = kwargs["clientName"]
  
  def connect (self):

    # add host but different port number to allow running callback
    # otherwise, it yields a connection error
    with Daemon(host=nic.ifaddresses(nic.gateways()['default'][2][1])[nic.AF_INET][0]['addr']) as daemon:

      callback = CallbackHandler (ipAddress = self.ipAddress, clientName = self.clientName, daemon = daemon)
      daemon.register(callback)

      with Pyro5.api.Proxy(f"PYRO:PyroServer@{self.ipAddress}:5681") as proxy:
        self.server = proxy
        self.server._pyroOneway.add("run")
        self.server.addCallback (callback)
        pyro = self.server.run(name = self.clientName) 
        print('-------------------PYRO----------------\n')
        print(pyro)
        print('\n----------------------------------------\n')
      
      daemon.requestLoop ()
