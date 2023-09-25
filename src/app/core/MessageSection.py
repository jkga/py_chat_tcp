import customtkinter
from PIL import Image
import os


class MessageSection:
    def __init__(self, **kwargs):
        # text frame
        self.contentFrame = customtkinter.CTkFrame(master=kwargs["root"], corner_radius=0, fg_color="transparent")
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
        label.pack()
        return self
    
    def addMessage (self, **args):
        frame = customtkinter.CTkFrame(master=self.messageSection, corner_radius=0)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=2)
        frame.grid_rowconfigure(0, weight=1)
        
        frameContent = customtkinter.CTkLabel(master=frame, height=50, text="", corner_radius=0, pady=10, justify="right")
        frameContent.grid(row = 0, column = 1, sticky = "nsew")
        frameContent.grid_columnconfigure(0, weight=1)
        frameContent.grid_rowconfigure(0, weight=1)

        frameContentMessage = customtkinter.CTkLabel(master=frameContent, text=f"{args['message']}", text_color="#ffffff", fg_color="gray", corner_radius=10, justify="right")
        frameContentMessage.grid(row = 0, column = 0, sticky = "e")

        if "id" in args and "senderId" in args:
            if args["id"] == args["senderId"]:
                frameContentMessage.configure(fg_color="green")
            else:
                frameContentMessage.configure(fg_color="gray")

        frame.pack(fill="both")
        return self