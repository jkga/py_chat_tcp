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

    # show prompt if not exists
    if not kwargs["name"] in self.clients: self.window.openInviteWindow(name = kwargs['name'], onReject = partial(self.onReject, name = kwargs['name']))
    
     # add to clients list
    self.clients[kwargs['name']] = {
      "name": kwargs['name']
    }

    # return data
    data = {"object": "dsds", "method": "self"}
    data = json.dumps(data, ensure_ascii=False, default=lambda o: o.__dict__)
    return data.encode("utf-8")
  
  def onReject (self, name):
    del self.clients[name]
    print (f"Rejected {name}")
  
  def connect(self, *args, **kwargs):
    return self.register (name = kwargs["name"])
  
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
