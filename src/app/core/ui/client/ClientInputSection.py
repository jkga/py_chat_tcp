import customtkinter
import os
from PIL import Image
from functools import partial

class ClientInputSection:
    def __init__(self, **kwargs):
        
        self.root = kwargs["root"]
        self.inputFrameText = False
        self.inputFrameSend = False
        self.connectedCallback = False
        self.clientName = self.root.clientName

        # input frame
        self.inputFrame = customtkinter.CTkFrame(master=kwargs["root"], corner_radius=0, height=50, fg_color="#0F1D2E")
        self.inputFrame.grid(row=2, column=0, columnspan=3, sticky="nsew")
        self.inputFrame.grid_columnconfigure(0, weight=3)
        self.inputFrame.grid_columnconfigure(1)
        self.inputFrame.grid_rowconfigure(0, weight=1)


        # show default connect to server field
        self.showMessageTextInput ()
    
    def showMessageTextInput (self, **args):
        self.inputFrameText = customtkinter.CTkEntry(master=self.inputFrame, height=50, corner_radius=0, fg_color="#0F1D2E", text_color="#CCCCCC", placeholder_text=f"Send private message to {self.clientName} ?", placeholder_text_color="gray", border_color="#0F1D2E")
        self.inputFrameText.grid(row = 0, column = 0, sticky="nsew")
        # send button image
        self.inputFrameSendImage = customtkinter.CTkImage(dark_image=Image.open(os.path.join(os.path.dirname(__file__),"../../../assets/img/send.png")),size=(15, 15))
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
    
    def setMessageTextInputDisable (self):
      self.inputFrameText.configure(state = "disabled")
    
    def setMessageSendButtonDisable (self):
      self.inputFrameSend.configure(state = "disabled")
    
    def setMessageTextInputEnable (self):
      self.inputFrameText.configure(state = "normal")
    
    def setMessageSendButtonEnable (self):
      self.inputFrameSend.configure(state = "normal")