import customtkinter
from PIL import Image
from functools import partial
import os
import socket

class MainHeader:
    def __init__(self,**kwargs):

        self.disconnectedCallback = False
        self.disconnectedCallbackParams = False

        # initial configs
        self.hostname = socket.gethostname()   
        #self.IPAddr = socket.gethostbyname(self.hostname)
        self.serverName = f"Your Address: {self.hostname}"
        
        # full width header with 4x1 config
        self.headerFrame = customtkinter.CTkFrame(kwargs['root'], corner_radius=0, height=50)
        self.headerFrame.grid(row=0, column=0, columnspan=3, sticky="new")
        self.headerFrame.grid_columnconfigure(0, weight=0)
        self.headerFrame.grid_columnconfigure(1, weight=5)
        self.headerFrame.grid_columnconfigure(2, weight=0)

        # image section
        self.headerFrameProfileImage = customtkinter.CTkFrame(master=self.headerFrame, corner_radius=0, height=50, border_width=0, border_color="#373737")
        self.headerFrameProfileImage.grid(row = 0, column=0, sticky="new")

        self.headerFrameProfileImageDefaultIcon = customtkinter.CTkImage(dark_image=Image.open(os.path.join(os.path.dirname(__file__),"../assets/img/user-default.png")),size=(35, 35))

        # image name
        self.headerFrameProfileImageContent = customtkinter.CTkLabel(master=self.headerFrameProfileImage, text=" ", pady="17", padx="2", image=self.headerFrameProfileImageDefaultIcon, anchor="center", compound="right")
        self.headerFrameProfileImageContent.grid()

        # name
        self.headerFrameProfileName = customtkinter.CTkFrame(master=self.headerFrame, corner_radius=0, height=50, border_width=0, border_color="#373737")
        self.headerFrameProfileName.grid(row = 0, column=1, sticky="new")
        self.headerFrameProfileName.grid_columnconfigure(0, weight=1)
        self.headerFrameProfileName.grid_columnconfigure(1, weight=0)
        self.headerFrameProfileName.grid_rowconfigure(0, weight=0)

        # profile name
        self.headerFrameProfileNameContent = customtkinter.CTkLabel(master=self.headerFrameProfileName, text=self.serverName, pady="17", padx="10", anchor="center")
        self.headerFrameProfileNameContent.grid(row = 0, column=0, sticky="new")

        # store
        self.headerFrameProfileStoreContentIcon = customtkinter.CTkImage(dark_image=Image.open(os.path.join(os.path.dirname(__file__),"../assets/img/store.png")),size=(25, 25))
        self.headerFrameProfileStoreContent = customtkinter.CTkButton(master=self.headerFrameProfileName, text="STORE", image=self.headerFrameProfileStoreContentIcon, anchor="center", compound="left", fg_color="#333333", corner_radius=0, height=50)
        self.headerFrameProfileStoreContent.grid(row = 0, column=1, sticky="nsew")

        # exit
        self.headerFrameProfileQuit = customtkinter.CTkFrame(master=self.headerFrame, corner_radius=0, height=50, border_width=0, border_color="#373737")
        self.headerFrameProfileQuit.grid(row=0, column=2, sticky="new")

        # uncomment to show quit button on startup
        # self.showQuitBtn ()
        self.showEmptyBtn ()

    def showQuitBtn (self):
        # exit Image
        self.headerFrameProfileQuitContentIcon = customtkinter.CTkImage(dark_image=Image.open(os.path.join(os.path.dirname(__file__),"../assets/img/shutdown.png")),size=(25, 25))
        self.headerFrameProfileQuitContent = customtkinter.CTkButton(master=self.headerFrameProfileQuit, text=" ", image=self.headerFrameProfileQuitContentIcon, anchor="center", compound="right", fg_color="#373737", corner_radius=0, height=50)
        self.headerFrameProfileQuitContent.grid(row = 0, column=0, sticky="nsew")
    
    def showIPBtn (self):
        # exit Image
        self.headerFrameProfileQuitContentIcon = customtkinter.CTkImage(dark_image=Image.open(os.path.join(os.path.dirname(__file__),"../assets/img/shutdown.png")),size=(25, 25))
        self.headerFrameProfileQuitContent = customtkinter.CTkButton(master=self.headerFrameProfileQuit, text="CONNECT TO IP", fg_color="#373737", corner_radius=0, height=50)
        self.headerFrameProfileQuitContent.grid(row = 0, column=0, sticky="nsew")
    
    def showServerBtn (self):
        # exit Image
        self.headerFrameProfileQuitContentIcon = customtkinter.CTkImage(dark_image=Image.open(os.path.join(os.path.dirname(__file__),"../assets/img/shutdown.png")),size=(25, 25))
        self.headerFrameProfileQuitContent = customtkinter.CTkButton(master=self.headerFrameProfileQuit, text="My Room", fg_color="#373737", corner_radius=0, height=50)
        self.headerFrameProfileQuitContent.grid(row = 0, column=0, sticky="nsew")

    def showDisconnectBtn (self, **params):
        # exit Image
        self.headerFrameProfileQuitContentIcon = customtkinter.CTkImage(dark_image=Image.open(os.path.join(os.path.dirname(__file__),"../assets/img/exit.png")),size=(25, 25))
        self.headerFrameProfileQuitContent = customtkinter.CTkButton(master=self.headerFrameProfileQuit, text=" ", image=self.headerFrameProfileQuitContentIcon, anchor="center", compound="right", fg_color="green", corner_radius=0, height=50)
        self.headerFrameProfileQuitContent.grid(row = 0, column=0, sticky="nsew")
        self.headerFrameProfileQuitContent.configure(command = partial(self.disconnect, root = self.headerFrameProfileQuitContent))
    
    def showEmptyBtn (self):
        # ensure that button and icon is present but not visible
        # this will allow further bindings
        self.headerFrameProfileQuitContentIcon = customtkinter.CTkImage(dark_image=Image.open(os.path.join(os.path.dirname(__file__),"../assets/img/exit.png")),size=(25, 25))
        self.headerFrameProfileQuitContent = customtkinter.CTkButton(master=self.headerFrameProfileQuit, text=" ", image=self.headerFrameProfileQuitContentIcon, anchor="center", compound="right", fg_color="#373737", corner_radius=0, height=50, border_width=0)
        return self
    
    def setServerName (self, **args):
        self.headerFrameProfileNameContent.configure(text=args["text"])
        if "color" in args: self.headerFrameProfileNameContent.configure(text_color=args["color"])
        return self

    def disconnect (self, **params):
        params["root"].configure(state = "disabled")
        params["root"].configure(text = "Disconnecting....")
        params["root"].configure(image = None)
        # connected after some processing
        
        self.showEmptyBtn ()
        # execute callback
        if(self.disconnectedCallbackParams):
            self.disconnectedCallback(self.disconnectedCallbackParams)
        else:
            self.disconnectedCallback()
        return self

    def onQuit (self, func):
        self.headerFrameProfileQuitContent.configure(command=partial(func))
        return self

    def onShowIPButton (self, func):
        self.headerFrameProfileQuitContent.configure(command=partial(func))
        return self

    def onProfilePictureClick (self, func):
        self.headerFrameProfileImageContent.bind("<Button-1>", func)
        return self

    def onShowServerButton (self, func):
        self.headerFrameProfileQuitContent.configure(command=partial(func))
        return self

    def onShowStoreButton(self, func):
        self.headerFrameProfileStoreContent.bind("<Button-1>", func)
        return self
    
    def onDisconnect (self, **params):
      if("callback" in params):
        self.disconnectedCallback = params["callback"]
        if("params" in params):
          self.disconnectedCallbackParams = params["params"]
        else:
          self.disconnectedCallbackParams = False
      else:
        self.disconnectedCallback = False
      return self
    