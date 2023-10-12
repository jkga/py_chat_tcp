import customtkinter
import os
import threading
import json
import random
import netifaces as nic
from dotenv import load_dotenv
from datetime import datetime
from core.MainHeader import *
from core.MessageSection import *
from core.InputSection import *
from core.socketServer import *
from core.socketServerUdp import *
from core.socketClient import *
from core.socketClientUdp import *
from core.settingsWindow import *
from core.ui.client.InvitePrompt import *
from core.pyro.PyroServer import *

# global configurations
load_dotenv ()
CLIENTS = []

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        #global CONFIG
        customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
        customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

        self.protocol("WM_DELETE_WINDOW", self.onAppClose)  
        self.bind('<Control-x>', self.onAppCloseViaKey) 
        self.settingsWindow = None
        self.inviteWindow = None

        # unique ID
        self.currentDateTime = datetime.now().strftime("%d%m%Y%H%M%S")
        self.serverUniqueId = f"{self.currentDateTime}{random.random()}"
        self.connectionType = os.getenv("CONNECTION_TYPE")
        self.clientName = ""
        self.ipAddress = ""

        # configure window
        self.customTitle = "Chat Application"
        self.title(self.customTitle)
        self.geometry(f"{500}x{700}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=4)
        self.grid_rowconfigure(2, weight=0)

        # initilize main interface
        self.mainHeader = MainHeader (root=self) 
        self.messageSection = MessageSection (root=self)
        self.inputSection = InputSection (root=self)

        # show connecting message
        self.mainHeader.setServerName (text = "Connecting . . .")
        self.socketClient = False

        if self.connectionType == "TCP":
            self.socketServer = SocketServer()
        else:
           self.socketServer = SocketServerUdp()

        self.socketServer.onStart(callback = partial(self.serverConnectedCallback))
        self.socketServer.onError(callback = partial(self.serverErrorCallback))
        self.socketServer.onReceive(callback = partial(self.serverReceiveCallback))
        threading.Thread(target=self.socketServer.start).start()

        self.serverConnectedCallback ()

        # show servername window
        self.openWindow (None)

        # start pyro
        pyroServer = PyroServer (window = self)
        pyroServer.onConnect = self.onConnectedPyroCallback
        threading.Thread(target = pyroServer.startServer).start ()

        #mainHeader.onQuit(lambda: os._exit (0))
        #mainHeader.onDisconnect(callback = lambda: os._exit (0))
        #mainHeader.onDisconnect(callback = inputSection.showIpAddressTextInput)
        #inputSection.onConnect(callback = mainHeader.showDisconnectBtn)
    def onConnectedPyroCallback (self, pyroInstance):
        print('----------------------------------------------------------------\n')
        print(f"------RUNNING PYRO SERVER-------: {pyroInstance.getPyroAddress ()}")
        print('----------------------------------------------------------------\n')

    def renderClientName (self):
        self.mainHeader.setServerName(text = f"{self.clientName}: {self.socketServer.getHostName()}:{self.socketServer.getPort()}")

    def serverErrorCallback (self, error):
        self.mainHeader.setServerName(text = f"{error}", color = "red")
        self.inputSection.setMessageTextInputDisable ()
        self.inputSection.setMessageSendButtonDisable ()
    
    def serverReceiveCallback (self, **args):
        print("---Running Server Calllback---")
        if self.socketServer:
            mess = args['message'].decode()
            addr = ''
            
            # get IP address of the sender
            if 'address' in args:
                addr = args['address'][0]
            
            if mess:
                try:
                    print("---Decoding Server Calllback---")
                    print(mess)
                    messDecoded = json.loads (mess)
                    if messDecoded["message"] and messDecoded["id"]:
                        self.messageSection.addMessage (message = f"{messDecoded['message']}", id=self.serverUniqueId, senderId=messDecoded["senderId"], timestamp = f"{messDecoded['timestamp']}", name=f"{messDecoded['name']}", ipAddress=addr)
                        # broadcast to all connected clients for UDP connection
                        if self.connectionType == "UDP": self.socketServer.sendMessage(message = f"{messDecoded['message']}", id=self.serverUniqueId, senderId=messDecoded["senderId"], timestamp = f"{messDecoded['timestamp']}", name=f"{messDecoded['name']}", ipAddress=addr)
                except Exception as e:
                    pass

    def serverConnectedCallback (self):
        # show server inputs
        self.mainHeader.setServerName(text = f"ROOM: {self.socketServer.getHostName()}:{self.socketServer.getPort()}")
        self.toggleIPButton ()
        # set ipaddress from gateways
        # most of the time, sock address returns the local or broadcast address
        gateways = nic.gateways() 
        default = gateways['default'][2][1] 
        ip = nic.ifaddresses(default)[nic.AF_INET][0]['addr']
        self.ipAddress = ip

    def toggleServerButton (self):
        self.inputSection.showIpAddressTextInput ()
        self.inputSection.onConnect(self.connectAsClient)
        self.mainHeader.showServerBtn()
        self.mainHeader.onShowServerButton (self.toggleIPButton)
        self.messageSection.showEmptyBanner ()

        return self

    def toggleIPButton (self):
        self.mainHeader.showIPBtn ()
        self.mainHeader.onShowIPButton (self.toggleServerButton)
        self.mainHeader.onProfilePictureClick (self.openWindow)
        self.messageSection.showMessageSection (messages = "")
        self.inputSection.showMessageTextInput ()
        self.inputSection.bindSendCommand(command = partial(self.broadcastMessage))
        self.inputSection.inputFrameText.bind('<Return>', command=self.broadcastMessageViaKey)
        return self

    def connectAsClient(self):
        # create client
        if self.connectionType == "TCP":
            self.socketClient = SocketClient ()
        else:
            self.socketClient = SocketClientUdp ()

        self.socketClient.setServerId (self.serverUniqueId)
        self.socketClient.setHost(self.inputSection.getMessageTextInputValue())
        self.socketClient.onConnect(callback = partial(self.clientConnectedCallback))
        self.socketClient.onReceive(callback = partial(self.clientReceivedCallback))
        self.socketClientThread = threading.Thread(target=self.socketClient.start).start()

    def clientConnectedCallback (self):
        if self.socketClient:
            self.messageSection.showMessageSection (title=self.inputSection.getMessageTextInputValue())
            self.inputSection.showMessageTextInput ()
            self.inputSection.bindSendCommand(command = partial(self.sendMessage))
            self.inputSection.inputFrameText.bind('<Return>', command=self.sendMessageViaKey)
            self.inputSection.inputFrameText.focus()

    def clientReceivedCallback (self, **args):
        print("---Running Calllback---")
        if self.socketClient:
            mess = args['message'].decode()
            addr = ''

            # get IP address of the sender
            if 'address' in args:
                addr = args['address'][0]
            if mess:
                try:
                    print("---Decoding Calllback---")
                    print(mess)
                    messDecoded = json.loads (mess)
                    if messDecoded["message"] and messDecoded["id"]:
                        timestamp = datetime.now().strftime("%B %d, %Y %I:%M%p")
                        name = ""
                        if messDecoded["timestamp"]: timestamp = messDecoded["timestamp"]
                        if messDecoded["name"]: name = messDecoded["name"]
                        #if messDecoded["id"] != self.serverUniqueId:
                        self.messageSection.addMessage (message = f"{messDecoded['message']}", id=self.serverUniqueId, senderId=messDecoded["senderId"], timestamp = timestamp, name=name, ipAddress = addr)
                except Exception as e:
                    pass

    # message function for client connection
    def sendMessage (self):
        if bool(self.inputSection.getMessageTextInputValue ()):
            timestamp = datetime.now().strftime("%B %d, %Y %I:%M%p")
            self.socketClient.sendMessage(message = self.inputSection.getMessageTextInputValue (), id=self.serverUniqueId, senderId=self.serverUniqueId, timestamp = timestamp, name=self.clientName)
            self.inputSection.setMessageTextInputValue (text = '')
            self.inputSection.inputFrameText.bind('<Return>', command=self.sendMessageViaKey)
            self.inputSection.inputFrameText.focus()

    # message function for server connection
    def broadcastMessage (self):
        if bool(self.inputSection.getMessageTextInputValue ()):
            timestamp = datetime.now().strftime("%B %d, %Y %I:%M%p")
            self.socketServer.sendMessage(message = self.inputSection.getMessageTextInputValue (), id=self.serverUniqueId, senderId=self.serverUniqueId, timestamp = timestamp, name=self.clientName, ipAddress = self.ipAddress)
            self.messageSection.addMessage (message = self.inputSection.getMessageTextInputValue (), id=self.serverUniqueId, senderId=self.serverUniqueId, timestamp = timestamp, name=self.clientName, ipAddress = self.ipAddress)
            self.inputSection.setMessageTextInputValue (text = '')
            self.inputSection.inputFrameText.bind('<Return>', command=self.broadcastMessageViaKey)
            self.inputSection.inputFrameText.focus()
    
    def broadcastMessageViaKey(self, event):
        self.broadcastMessage ()

    def sendMessageViaKey(self, event):
        self.sendMessage ()
    
    def onAppClose (self):
        if self.socketServer : self.socketServer.close()
        if self.socketClient : self.socketClient.disconnect()
        os._exit (0)

    def onAppCloseViaKey (self, event):
        self.onAppClose ()
    
    def openWindow(self, event):
        if self.settingsWindow is None or not self.settingsWindow.winfo_exists():
            self.settingsWindow = SettingsWindow(self)
        else:
            self.settingsWindow.focus()

    def openInvitePromptWindow(self, *args, **kwargs):
        self.inviteWindow = InvitePrompt(self)
        self.inviteWindow.setClientName(kwargs["name"])
        if "onReject" in kwargs: self.inviteWindow.onRejectCallback(kwargs["onReject"])
        if "onAccept" in kwargs: self.inviteWindow.onAcceptCallback(kwargs["onAccept"])
        self.inviteWindow.show ()
        self.inviteWindow.focus()
    

if __name__ == "__main__":
    app = App()
    app.mainloop()
    input("Press enter to continue...")