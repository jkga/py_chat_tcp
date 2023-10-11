import customtkinter
from core.ui.client.ClientMessageSection import *
from core.ui.client.ClientInputSection import *

class ChatWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__()

        #global CONFIG
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
    
    def onAppClose (self):
        self.destroy ()
        
        
