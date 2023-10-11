import customtkinter
from PIL import Image
import os
from core.ui.client.InviteWindow import *


class MessageSection:
    def __init__(self, **kwargs):
        self.index = 0
        self.root = kwargs["root"]
        self.inviteWindow = None
        # text frame
        self.contentFrame = customtkinter.CTkFrame(master=self.root, corner_radius=0, fg_color="transparent")
        self.contentFrame.grid(row=1, column=1, sticky="nsew")

        self.contentFrame.grid_columnconfigure(0, weight = 1)
        self.contentFrame.grid_rowconfigure(0, weight = 1)

        self.showEmptyBanner ()

    
    def showEmptyBanner (self):
        # message banner
        self.contentEmptyBanner = customtkinter.CTkImage(dark_image=Image.open(os.path.join(os.path.dirname(__file__),"../assets/img/message-default.png")),size=(300, 200))
        self.contentEmptyBannerImage = customtkinter.CTkLabel(self.contentFrame, image=self.contentEmptyBanner, text="", fg_color="transparent")
        self.contentEmptyBannerImage.grid(row=0, column=0, sticky="nsew")
        return self

    def showNothing (self):
        # message banner
        self.contentEmptyBanner = customtkinter.CTkImage(dark_image=Image.open(os.path.join(os.path.dirname(__file__),"../assets/img/message-call-sepia.png")),size=(300, 200))
        self.contentEmptyBannerImage = customtkinter.CTkLabel(self.contentFrame, image=self.contentEmptyBanner, text="", fg_color="transparent")
        self.contentEmptyBannerImage.grid(row=0, column=0, sticky="nsew")
        return self
    
    def showMessageSection (self, **args):
        self.messageSection = customtkinter.CTkScrollableFrame(master=self.contentFrame)
        self.messageSection.grid(row=0, column=0, sticky="nsew")
        label = customtkinter.CTkLabel(master=self.messageSection, text="Messages", text_color="gray")

        if "title" in args:
            label.configure(text = args["title"])
        label.pack()

        return self
    
    def addMessage (self, **args):
        frame = customtkinter.CTkFrame(master=self.messageSection, corner_radius=0)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=2)
        frame.grid_columnconfigure(2, weight=0)
        frame.grid_rowconfigure(0, weight=1)
        
        frameContent = customtkinter.CTkLabel(master=frame, height=50, text="", corner_radius=0, pady=10, justify="right")
        frameContent.grid(row = 0, column = 1, sticky = "nsew")
        frameContent.grid_columnconfigure(0, weight=1)
        frameContent.grid_rowconfigure(0, weight=1)

        frameContentMessage = customtkinter.CTkLabel(master=frameContent, text=f"{args['message']}", text_color="#ffffff", fg_color="gray", corner_radius=10, justify="right")
        frameContentMessage.grid(row = 0, column = 1, sticky = "e")

        frameContentMessageSub = customtkinter.CTkLabel(master=frameContent, text="", padx="10", height=5, font=('', 9), text_color="gray")
        frameContentMessageSub.grid(row = 0, column = 0, sticky = "e")

        if "timestamp" in args: frameContentMessageSub.configure(text=f"{args['timestamp']}")

        if "id" in args and "senderId" in args:
            if args["id"] == args["senderId"]:
                frameContentMessage.configure(fg_color="gray")
            else:
                frameContentMessage.configure(fg_color="green")         
                # add name
                if "timestamp" in args and "name" in args: frameContentMessageSub.configure(text=f"{args['timestamp']} | {args['name']}")
                # add user icon
                frameIcon = customtkinter.CTkImage(dark_image=Image.open(os.path.join(os.path.dirname(__file__),"../assets/img/user-default.png")),size=(25, 25))
                frameIconLabel = customtkinter.CTkButton(master=frameContent, image=frameIcon, text="", anchor="e", width=40, bg_color="transparent", fg_color="transparent", hover_color="#212121", command=partial(self.showInviteMessage, name = args['name'], ipAddress = args['ipAddress']))
                frameIconLabel.grid(row=0, column=2, sticky="w")


        frame.pack(fill="both")
        return self

    def showInviteMessage (self, **args):

        if not "ipAddress" in args: return
        print("----------------PYRO WILL SEND REQUEST TO IP-------------")
        print(args["ipAddress"])
        print("----------------PYRO END------------------")

        if self.inviteWindow is None or not self.inviteWindow.winfo_exists():
            self.inviteWindow = InviteWindow ()
            self.inviteWindow.setRoot (self.root)
            self.inviteWindow.setClientName (args["name"])
            if "ipAddress" in args: self.inviteWindow.setIpAddress(args["ipAddress"])
            self.inviteWindow.show ()
        else:
            self.inviteWindow.focus()