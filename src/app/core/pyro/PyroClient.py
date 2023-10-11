import Pyro5.api

class PyroClient:
  def __init__ (self, *args, **kwargs):

    print ('----Pyro Client Object Initialized--')
    self.ipAddress = None
    self.server = None
    self.clientName = "anon"

    if "ipAddress" in kwargs: self.ipAddress = kwargs["ipAddress"]
    if "clientName" in kwargs: self.clientName = kwargs["clientName"]
  
  def connect (self):
    self.server = Pyro5.api.Proxy(f"PYRO:PyroServer@{self.ipAddress}:5681")
    pyro = self.server.run(name = self.clientName) 
    print('-------------------PYRO----------------\n')
    print(pyro)
    print('\n----------------------------------------\n')