import customtkinter
import os
from PIL import Image
from functools import partial

class InputSection:
    def __init__(self, **kwargs):

        self.inputFrameText = False
        self.inputFrameSend = False
        self.connectedCallback = False

        # input frame
        self.inputFrame = customtkinter.CTkFrame(master=kwargs["root"], corner_radius=0, height=50, fg_color="#0F1D2E")
        self.inputFrame.grid(row=2, column=0, columnspan=3, sticky="nsew")
        self.inputFrame.grid_columnconfigure(0, weight=3)
        self.inputFrame.grid_columnconfigure(1)
        self.inputFrame.grid_rowconfigure(0, weight=1)


        # show default connect to server field
        # self.showIpAddressTextInput ()
    
    def showMessageTextInput (self, **args):
        self.inputFrameText = customtkinter.CTkEntry(master=self.inputFrame, height=50, corner_radius=0, fg_color="#0F1D2E", text_color="#CCCCCC", placeholder_text="What do you want to say?", placeholder_text_color="gray", border_color="#0F1D2E")
        self.inputFrameText.grid(row = 0, column = 0, sticky="nsew")
        # send button image
        self.inputFrameSendImage = customtkinter.CTkImage(dark_image=Image.open(os.path.join(os.path.dirname(__file__),"../assets/img/send.png")),size=(15, 15))
        # send button
        self.inputFrameSend = customtkinter.CTkButton(master=self.inputFrame, text="SEND", corner_radius=0, border_color="#0F1D2E", image=self.inputFrameSendImage, compound="right", anchor="center")

        # bind button click
        if "callback" in args:
          self.inputFrameSend.configure(command = args["callback"])
        self.inputFrameSend.grid(row = 0, column = 1, stick = "nsew")
        return self
    
    def bindSendCommand (self, **args):
      self.inputFrameSend.configure(command = args["command"])
    
    def getMessageTextInputValue (self):
       return self.inputFrameText.get()
    
    def setMessageTextInputValue (self, **args):
      self.inputFrameText = customtkinter.CTkEntry(master=self.inputFrame, height=50, corner_radius=0, fg_color="#0F1D2E", text_color="#CCCCCC", placeholder_text="What do you want to say?", placeholder_text_color="gray", border_color="#0F1D2E")
      self.inputFrameSend.configure(textvariable = args["text"])
      self.inputFrameText.grid(row = 0, column = 0, sticky="nsew")

    def showIpAddressTextInput (self):
        self.inputFrameText = customtkinter.CTkEntry(master=self.inputFrame, height=50, corner_radius=0, fg_color="#0F1D2E", text_color="#CCCCCC", placeholder_text="192.xxx.xxx.xxx", placeholder_text_color="gray", border_color="#0F1D2E")
        self.inputFrameText.grid(row = 0, column = 0, sticky="nsew")
        # send button image
        self.inputFrameSendImage = customtkinter.CTkImage(dark_image=Image.open(os.path.join(os.path.dirname(__file__),"../assets/img/send.png")),size=(15, 15))
        # send button
        self.inputFrameSend = customtkinter.CTkButton(master=self.inputFrame, text="CONNECT", corner_radius=0, border_color="green", fg_color="green", hover_color="#508617")
        self.inputFrameSend.grid(row = 0, column = 1, stick = "nsew")
        self.inputFrameSend.configure(command = partial(self.connect, root = self.inputFrameSend))
        return self
    
    def setMessageTextInputDisable (self):
      self.inputFrameText.configure(state = "disabled")
    
    def setMessageSendButtonDisable (self):
      self.inputFrameSend.configure(state = "disabled")

    def connect (self, **params):
      self.ipAddress = self.inputFrameText.get()
      # prevent empty address
      if not bool(self.ipAddress):
        print ("ERROR: EMPTY ADDRESS")
        return self
      # proceed
      params["root"].configure(state = "disabled")
      params["root"].configure(text = "CONNECTING...")
      
      # run callback
      if(self.connectedCallback): self.connectedCallback ()
      return self
    
    # define callback
    def onConnect (self, func):
      self.connectedCallback = func
      return self