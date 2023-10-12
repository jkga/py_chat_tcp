import customtkinter
import json
from datetime import datetime
from core.ui.client.ClientMessageSection import *
from core.ui.client.ClientInputSection import *

class ChatWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__()

        # parent window
        self.root = kwargs["root"] 
        # parent pyro instance
        self.pyroInstance = kwargs["pyroInstance"]
        self.isRunningOnServer = False
        self.messageCount  = 0

        if "isRunningOnServer" in kwargs: self.isRunningOnServer = True

        # global CONFIG
        customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
        customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

        # change default name
        self.clientName = "Anonymous" 
        self.ipAddress = ""

        self.geometry(f"{500}x{700}")
        self.title("Private Chat Invitation")
        self.protocol("WM_DELETE_WINDOW", self.onAppClose)  

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=4)
        self.grid_rowconfigure(2, weight=0)

        self.rejectCallback = None

    def setClientName (self, name):
        self.clientName = name
        self.title (f"Private Chat Room ({name})")
    
    def setIpAddress (self, ip):
        self.ipAddress = ip

    def show (self):
        self.messageSection = ClientMessageSection (root=self)
        self.inputSection = ClientInputSection (root=self)
        self.inputSection.bindSendCommand(command = self.sendMessage)
    
    def sendMessage (self):
        # add message count
        self.messageCount = self.messageCount + 1

        # show message section for the first message
        if self.messageCount == 1: self.messageSection.showMessageSection ()

        # data
        timestamp = datetime.now().strftime("%B %d, %Y %I:%M%p")
        mess = self.inputSection.getMessageTextInputValue ()

        # use the current thread and send message to pyro server
        if hasattr(self.pyroInstance, '_pyroClaimOwnership') : self.pyroInstance._pyroClaimOwnership() 
        
        if bool(mess):
            # disable input field
            self.inputSection.setMessageTextInputDisable ()
            self.inputSection.setMessageSendButtonDisable ()

            # send message
            payload = {
                "timestamp": timestamp,
                "message" : mess
            }
                    
            try:
                try:
                    if not self.isRunningOnServer:
                        # client pyro
                        self.root.pyroInstance.sendMessage(message = json.dumps(payload))
                    else:
                        self.pyroInstance.receiveMessage(message = json.dumps(payload))
                    self.messageSection.addMessage(name = self.clientName, timestamp = f"{timestamp}", id = "", senderId = "", message = f"{mess}")
                    self.inputSection.setMessageTextInputValue (text = '')
                except Exception as e: pass
                finally:
                    self.inputSection.setMessageTextInputEnable()
                    self.inputSection.setMessageSendButtonEnable()
            except Exception: pass
    
    def receiveMessage (self, message):

        # decode data
        mess = json.loads(message)
        message = mess['message']
        timestamp = mess['timestamp']
        
        print("------ showing message to server ui -------")
        print(message)
        print("------ end showing message to server ui -------")


        # add message count
        self.messageCount = self.messageCount + 1

        # show message section for the first message
        if self.messageCount == 1: self.messageSection.showMessageSection ()

        self.messageSection.addMessage(name = self.clientName, timestamp = f"{timestamp}", id = "", senderId = "none", message = f"{message}")
    
    def onAppClose (self):
        self.destroy ()
        
        
