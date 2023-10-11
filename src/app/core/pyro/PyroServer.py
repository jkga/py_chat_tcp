import Pyro5.api
import json
from functools import partial

@Pyro5.api.expose
class PyroServer:
  def __init__ (self, *args, **kwargs):
    print ('Intializing pyro Object')
    self.window = None
    self.clients = {}
    self.pyroAddress = ''
    self.onConnect = None

    if 'window' in kwargs: self.window = kwargs["window"]


  def register(self, *args, **kwargs):
    print('------regestering--------')

    # show prompt if not exists
    # method used is part of the mainloop to be able to call other functions
    if not kwargs["name"] in self.clients: self.window.openInvitePromptWindow(name = kwargs['name'], onReject = partial(self.onReject, name = kwargs['name']))
    
     # add to clients list
    self.clients[kwargs['name']] = {
      "pyroInstance": kwargs["pyroInstance"]
    }

    if self.window.openInvitePromptWindow.onMessage:
      # return data
      data = {"object": "dsds", "method": "self"}
      data = json.dumps(data, ensure_ascii=False, default=lambda o: o.__dict__)
      self.window.openInvitePromptWindow.onMessage (data.encode("utf-8"))
      return data.encode("utf-8")
  
  def onReject (self, name):
    del self.clients[name]
    print (f"Rejected {name}")
  
  def run(self, *args, **kwargs):
    print ('----connected-----')
    return self.register (name = kwargs["name"], pyroInstance = kwargs["pyroInstance"])
  
  def getPyroAddress (self):
    return self.pyroAddress
  
  def startServer (self):
    # Start server and expose the TimeTaggerRPC class
    with Pyro5.api.Daemon(host='', port=5681) as daemon:
        # Register class with Pyro
        addr = daemon.register(self, 'PyroServer')
        self.pyroAddress = addr
        print(addr)
        if self.onConnect: self.onConnect (self)
        daemon.requestLoop()
