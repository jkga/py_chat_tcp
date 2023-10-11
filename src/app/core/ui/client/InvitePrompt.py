import customtkinter
import threading
from core.ui.client.ChatWindow import *

class InvitePrompt(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # change default name
        self.clientName = "Anonymous" 

        self.geometry("400x130")
        self.title("Private Chat Invitation")
        self.protocol("WM_DELETE_WINDOW", self.onAppClose)  
        self.rejectCallback = None
        self.messageCallback = None

    def setClientName (self, name):
        self.clientName = name
    
    def onRejectCallback (self, func):
        self.rejectCallback = func
    
    def onMessage (self, func):
        self.messageCallback = func

    def show (self):

        self.label = customtkinter.CTkLabel(self, text=f"{self.clientName} wants to invite you to a private chat")
        self.label.pack(padx=20, pady=10)

        self.buttonSection = customtkinter.CTkFrame(master=self, fg_color="transparent", bg_color="transparent")
        self.buttonSection.grid_rowconfigure(0, weight = 1)
        self.buttonSection.grid_columnconfigure(0, weight= 1)
        self.buttonSection.grid_columnconfigure(1, weight= 1)
        self.buttonSection.pack()

        # accept
        self.submitBtn = customtkinter.CTkButton(master=self.buttonSection, text="ACCEPT", fg_color="green", hover_color="#508617", command=self.createNewChatBox)
        self.submitBtn.grid(row = 0, column = 1, sticky="ew", padx = 10, pady = 10)

        # reject
        self.submitBtn = customtkinter.CTkButton(master=self.buttonSection, text="REJECT", fg_color="black", hover_color="gray", command=self.closeBox)
        self.submitBtn.grid(row = 0, column = 0, sticky="ew", padx = 10, pady = 10)
    
    def createNewChatBox (self):

        # close confirmation modal
        self.onAppClose ()
        
        # show new chat window
        chatWindow = ChatWindow()
        chatWindow.setClientName(self.clientName)
        threading.Thread(target=chatWindow.show).start()

    def closeBox(self):
        if self.rejectCallback: self.rejectCallback ()
        self.destroy ()
    
    def onAppClose (self):
        self.closeBox ()
        
        
