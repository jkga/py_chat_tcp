import customtkinter
import os
import threading
import json
import random
from datetime import datetime
from core.MainHeader import *
from core.MessageSection import *
from core.InputSection import *
from core.socketServer import *
from core.socketClient import *

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
        customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

        self.protocol("WM_DELETE_WINDOW", self.onAppClose)  
        self.bind('<Control-x>', self.onAppCloseViaKey) 

        # unique ID
        self.currentDateTime = datetime.now().strftime("%d%m%Y%H%M%S")
        self.serverUniqueId = f"{self.currentDateTime}{random.random()}"
        
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
        self.socketServer = SocketServer()
        self.socketServer.onStart(callback = partial(self.serverConnectedCallback))
        self.socketServer.onError(callback = partial(self.serverErrorCallback))
        self.socketServer.onReceive(callback = partial(self.serverReceiveCallback))
        threading.Thread(target=self.socketServer.start).start()

        self.serverConnectedCallback ()

        #mainHeader.onQuit(lambda: os._exit (0))
        #mainHeader.onDisconnect(callback = lambda: os._exit (0))
        #mainHeader.onDisconnect(callback = inputSection.showIpAddressTextInput)
        #inputSection.onConnect(callback = mainHeader.showDisconnectBtn)
        
    def serverErrorCallback (self, error):
        self.mainHeader.setServerName(text = f"{error}", color = "red")
        self.inputSection.setMessageTextInputDisable ()
        self.inputSection.setMessageSendButtonDisable ()
    
    def serverReceiveCallback (self, **args):
        print("---Running Server Calllback---")
        if self.socketServer:
            mess = args['message'].decode()
            if mess:
                try:
                    print("---Decoding Server Calllback---")
                    print(mess)
                    messDecoded = json.loads (mess)
                    if messDecoded["message"] and messDecoded["id"]:
                        self.messageSection.addMessage (message = f"{messDecoded['message']}", id=self.serverUniqueId, senderId=messDecoded["id"], timestamp = f"{messDecoded['timestamp']}")
                except Exception as e:
                    pass

    def serverConnectedCallback (self):
        # show server inputs
        self.mainHeader.setServerName(text = f"ROOM: {self.socketServer.getHostName()}:{self.socketServer.getPort()}")
        self.toggleIPButton ()

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
        self.messageSection.showMessageSection (messages = "")
        self.inputSection.showMessageTextInput ()
        self.inputSection.bindSendCommand(command = partial(self.broadcastMessage))
        self.inputSection.inputFrameText.bind('<Return>', command=self.broadcastMessageViaKey)
        return self

    def connectAsClient(self):
        # create client
        self.socketClient = SocketClient ()
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
            if mess:
                try:
                    print("---Decoding Calllback---")
                    print(mess)
                    messDecoded = json.loads (mess)
                    if messDecoded["message"] and messDecoded["id"]:
                        self.messageSection.addMessage (message = f"{messDecoded['message']}", id=self.serverUniqueId, senderId=messDecoded["id"], timestamp = datetime.now().strftime("%B %d, %Y %I:%M%p"))
                except Exception as e:
                    pass

    # message function for client connection
    def sendMessage (self):
        if bool(self.inputSection.getMessageTextInputValue ()):
            self.socketClient.sendMessage(message = self.inputSection.getMessageTextInputValue ())
            self.inputSection.setMessageTextInputValue (text = '')
            self.inputSection.inputFrameText.bind('<Return>', command=self.sendMessageViaKey)
            self.inputSection.inputFrameText.focus()

    # message function for server connection
    def broadcastMessage (self):
        if bool(self.inputSection.getMessageTextInputValue ()):
            self.socketServer.sendMessage(message = self.inputSection.getMessageTextInputValue (), id=self.serverUniqueId, timestamp = datetime.now().strftime("%B %d, %Y %I:%M%p"))
            self.messageSection.addMessage (message = self.inputSection.getMessageTextInputValue (), id=self.serverUniqueId, senderId=self.serverUniqueId, timestamp = datetime.now().strftime("%B %d, %Y %I:%M%p"))
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

if __name__ == "__main__":
    app = App()
    app.mainloop()