import customtkinter
import os
from PIL import Image

class StoreWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.geometry("1024x700")
        self.title("Store")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # parent frame
        self.mainFrame = customtkinter.CTkFrame(master=self, fg_color="#0F1D2E", corner_radius=0)
        self.mainFrame.grid_rowconfigure(0, weight=1)
        self.mainFrame.grid_columnconfigure(0, weight=3)
        self.mainFrame.grid_columnconfigure(1, weight=1)
        self.mainFrame.grid(row=0, column=0, sticky="nsew")

        # items section frame
        self.storeSection = customtkinter.CTkFrame(master=self.mainFrame, fg_color="transparent", corner_radius=0)
        self.storeSection.grid_columnconfigure(0, weight=1)
        self.storeSection.grid_rowconfigure(0, weight=0)
        self.storeSection.grid_rowconfigure(1, weight=1)
        self.storeSection.grid(row=0, column=0, sticky="nsew")

        # item section status
        self.storeStatusSection = customtkinter.CTkFrame(master=self.storeSection, fg_color="transparent", corner_radius=0, height=40)
        self.storeStatusSection.grid(row=0, column=0, sticky="nsew")

        self.storeContentSection = customtkinter.CTkScrollableFrame(master=self.storeSection, fg_color="transparent", corner_radius=0)
        self.storeContentSection.grid(row=1, column=0, sticky="nsew")

        self.storeSectionHeader = customtkinter.CTkFrame(master=self.storeContentSection, fg_color="transparent")
        self.storeSectionHeader.pack()
        
        self.storeSectionHeaderContent = customtkinter.CTkLabel(master=self.storeSectionHeader, text="Auction", text_color="white", font=customtkinter.CTkFont(size=16, weight="bold"), anchor="w", compound="top")
        self.storeSectionHeaderContent.pack()
        self.storeSectionSubHeaderContent = customtkinter.CTkLabel(master=self.storeSectionHeader, text="List of items for bidding", text_color="#ccc", anchor="w", justify="left", font=customtkinter.CTkFont(size=12))
        self.storeSectionSubHeaderContent.pack()

        self.addItem ()
        self.addItem ()
        self.addItem ()


    def addItem (self):
              

        # item
        item = customtkinter.CTkFrame(master=self.storeContentSection, fg_color="transparent", bg_color="transparent", height=300)
        item.pack(fill="x", padx=50, pady=10)

        itemContent = customtkinter.CTkFrame(master=item, fg_color="#142C4A", corner_radius=25)
        itemContent.grid_rowconfigure(0, weight=0)
        itemContent.grid_columnconfigure(0, weight=0)
        itemContent.grid_columnconfigure(1, weight=3)
        itemContent.grid_columnconfigure(2, weight=0)
        itemContent.pack(fill="both", pady=10)

        itemContentIcon = customtkinter.CTkImage(dark_image=Image.open(os.path.join(os.path.dirname(__file__),"../../../../assets/img/bag.png")),size=(25, 25))
        itemContentImage = customtkinter.CTkLabel(master=itemContent, text=" ", image=itemContentIcon, anchor="n", compound="top", fg_color="transparent", padx=20, pady=10, width=50, corner_radius=50)
        itemContentImage.grid(row = 0, column=0, sticky="nsew")

        itemContentTextSection = customtkinter.CTkFrame(master=itemContent, fg_color="transparent")
        itemContentTextSection.grid_columnconfigure(0, weight=1)
        itemContentTextSection.grid_rowconfigure(0, weight=0)
        itemContentTextSection.grid_rowconfigure(1, weight=0)
        itemContentTextSection.grid_rowconfigure(2, weight=0)
        itemContentTextSection.grid(row=0, column=1, sticky="nsew")

        itemContentTitle = customtkinter.CTkTextbox(master=itemContentTextSection, text_color="white", font=customtkinter.CTkFont(size=14, weight="bold"), fg_color="transparent", padx=10, pady=10, height=30)
        itemContentTitle.insert("0.0", "Lorem ipsum dolor sit amet")
        itemContentTitle.configure(state="disabled")
        itemContentTitle.grid(row=0, column=0, sticky="new")

        itemContentDescription = customtkinter.CTkTextbox(master=itemContentTextSection, text_color="white", fg_color="transparent", height=100, padx=10)
        itemContentDescription.insert("0.0", "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.")
        itemContentDescription.configure(state="disabled")
        itemContentDescription.grid(row=1, column=0, sticky="new")

        itemContentCreator = customtkinter.CTkFrame(master=itemContentTextSection, height=80, fg_color="transparent")
        itemContentCreator.grid_rowconfigure(0, weight=0)
        itemContentCreator.grid_columnconfigure(0, weight=0)
        itemContentCreator.grid_columnconfigure(1, weight=1)
        itemContentCreator.grid(row=2, column=0, sticky="nsew")

        itemContentCreatorIcon = customtkinter.CTkImage(dark_image=Image.open(os.path.join(os.path.dirname(__file__),"../../../../assets/img/user-default.png")),size=(25, 25))
        itemContentCreatorIcon = customtkinter.CTkLabel(master=itemContentCreator, text=" ", image=itemContentCreatorIcon, anchor="n", compound="top", fg_color="transparent", corner_radius=0, padx=20, pady=10, width=50)
        itemContentCreatorIcon.grid(row = 0, column=0, sticky="nsew")

        itemContentCreatorSection = customtkinter.CTkFrame(master=itemContentCreator, fg_color="transparent")
        itemContentCreatorSection.grid_columnconfigure(0, weight=1)
        itemContentCreatorSection.grid_rowconfigure(0, weight=0)
        itemContentCreatorSection.grid_columnconfigure(1, weight=0)
        itemContentCreatorSection.grid(row=0, column=1, sticky="nsew")

        itemContentCreatorName = customtkinter.CTkLabel(master=itemContentCreatorSection, text_color="white", text="John Hey Doe", anchor="w", compound="top", height=10)
        itemContentCreatorName.grid(row=0, column=0, sticky="nsew")

        itemContentCreatorTime = customtkinter.CTkLabel(master=itemContentCreatorSection, text_color="white", text="January 01, 2023 3:00PM", font=customtkinter.CTkFont(size=10), anchor="w", compound="top")
        itemContentCreatorTime.grid(row=1, column=0, sticky="nsew")

        # item status btn section
        itemContentStatusSection  = customtkinter.CTkFrame(master=itemContent, width=80, fg_color="transparent")
        itemContentStatusSection.grid(row=0, column=2, sticky="nsew", padx=20, pady=10)

        itemContentStatusSectionLabel = customtkinter.CTkLabel(master=itemContentStatusSection, text="OPEN", fg_color="#217749", corner_radius=10, width=50)
        itemContentStatusSectionLabel.pack()

        itemContentStatusSectionBidLabel = customtkinter.CTkLabel(master=itemContentStatusSection, text="115 bids", fg_color="transparent", corner_radius=10, width=50)
        itemContentStatusSectionBidLabel.pack()

        self.showInfoSection ()
        self.showInputSection ()
        self.addBid ()
        self.addBid ()

    def showInfoSection (self):
        # store item section
        self.storeItemInfoSection = customtkinter.CTkFrame(master=self.mainFrame, fg_color="#182F4A", corner_radius=0, width=300)
        self.storeItemInfoSection.grid_columnconfigure(0, weight=1)
        self.storeItemInfoSection.grid_rowconfigure(0, weight=0)
        self.storeItemInfoSection.grid_rowconfigure(1, weight=2)
        self.storeItemInfoSection.grid_rowconfigure(2, weight=0)
        self.storeItemInfoSection.grid(row=0, column=1, sticky="nsew")

        self.storeItemInfoSectionHeader = customtkinter.CTkFrame(master=self.storeItemInfoSection, fg_color="#142C4A", corner_radius=0)
        self.storeItemInfoSectionHeader.grid_rowconfigure(0, weight=0)
        self.storeItemInfoSectionHeader.grid_columnconfigure(0, weight=0)
        self.storeItemInfoSectionHeader.grid_columnconfigure(1, weight=3)
        self.storeItemInfoSectionHeader.grid(row=0, column=0, sticky="nsew")

        self.storeItemInfoSectionHeaderIcon = customtkinter.CTkImage(dark_image=Image.open(os.path.join(os.path.dirname(__file__),"../../../../assets/img/bag.png")),size=(25, 25))
        self.storeItemInfoSectionHeaderIcon = customtkinter.CTkLabel(master=self.storeItemInfoSectionHeader, text=" ", image=self.storeItemInfoSectionHeaderIcon, anchor="n", compound="top", fg_color="transparent", corner_radius=0, padx=20, pady=10, width=50)
        self.storeItemInfoSectionHeaderIcon.grid(row = 0, column=0, sticky="nsew")


        self.storeItemInfoSectionHeaderContent = customtkinter.CTkFrame(master=self.storeItemInfoSectionHeader, fg_color="#142C4A")
        self.storeItemInfoSectionHeaderContent.grid_columnconfigure(0, weight=1)
        self.storeItemInfoSectionHeaderContent.grid_rowconfigure(0, weight=0)
        self.storeItemInfoSectionHeaderContent.grid_rowconfigure(1, weight=0)
        self.storeItemInfoSectionHeaderContent.grid_rowconfigure(2, weight=0)
        self.storeItemInfoSectionHeaderContent.grid(row=0, column=1, sticky="nsew")

        self.storeItemInfoSectionHeaderTitle = customtkinter.CTkTextbox(master=self.storeItemInfoSectionHeaderContent, text_color="white", font=customtkinter.CTkFont(size=14, weight="bold"), fg_color="transparent", padx=10, pady=10, height=30)
        self.storeItemInfoSectionHeaderTitle.insert("0.0", "Product Name")
        self.storeItemInfoSectionHeaderTitle.configure(state="disabled")
        self.storeItemInfoSectionHeaderTitle.grid(row=0, column=0, sticky="new")

        self.storeItemInfoSectionHeaderDescription = customtkinter.CTkTextbox(master=self.storeItemInfoSectionHeaderContent, text_color="white", fg_color="transparent", height=100, padx=10)
        self.storeItemInfoSectionHeaderDescription.insert("0.0", "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.")
        self.storeItemInfoSectionHeaderDescription.configure(state="disabled")
        self.storeItemInfoSectionHeaderDescription.grid(row=1, column=0, sticky="new")


        self.storeItemInfoSectionHeaderCreator = customtkinter.CTkFrame(master=self.storeItemInfoSectionHeaderContent, fg_color="transparent")
        self.storeItemInfoSectionHeaderCreator.grid_columnconfigure(0, weight=0)
        self.storeItemInfoSectionHeaderCreator.grid_columnconfigure(1, weight=0)
        self.storeItemInfoSectionHeaderCreator.grid_rowconfigure(0, weight=0)
        self.storeItemInfoSectionHeaderCreator.grid(row=2, column=0, sticky="nsew")

        self.storeItemInfoSectionHeaderCreatorIcon = customtkinter.CTkImage(dark_image=Image.open(os.path.join(os.path.dirname(__file__),"../../../../assets/img/user-default.png")),size=(25, 25))
        self.storeItemInfoSectionHeaderCreatorIcon = customtkinter.CTkLabel(master=self.storeItemInfoSectionHeaderCreator, text=" ", image=self.storeItemInfoSectionHeaderCreatorIcon, anchor="n", compound="top", fg_color="transparent", corner_radius=0, padx=20, pady=10, width=50)
        self.storeItemInfoSectionHeaderCreatorIcon.grid(row = 0, column=0, sticky="nsew")

        self.storeItemInfoSectionHeaderCreatorSection = customtkinter.CTkFrame(master=self.storeItemInfoSectionHeaderCreator, fg_color="transparent")
        self.storeItemInfoSectionHeaderCreatorSection.grid_columnconfigure(0, weight=0)
        self.storeItemInfoSectionHeaderCreatorSection.grid_rowconfigure(0, weight=0)
        self.storeItemInfoSectionHeaderCreatorSection.grid_rowconfigure(1, weight=0)
        self.storeItemInfoSectionHeaderCreatorSection.grid(row=0, column=1, sticky="nsew")

        self.storeItemInfoSectionHeaderCreatorName = customtkinter.CTkLabel(master=self.storeItemInfoSectionHeaderCreatorSection, text_color="white", text="John Hey Doe", anchor="w", compound="top", fg_color="transparent", height=10)
        self.storeItemInfoSectionHeaderCreatorName.grid(row=0, column=1, sticky="new")
        self.storeItemInfoSectionHeaderCreatorTime = customtkinter.CTkLabel(master=self.storeItemInfoSectionHeaderCreatorSection, text_color="white", text="January 01, 2023 3:00PM", font=customtkinter.CTkFont(size=10), anchor="w", compound="top", fg_color="transparent")
        self.storeItemInfoSectionHeaderCreatorTime.grid(row=1, column=1, sticky="new")

        # bids from users
        self.storeItemInfoSectionBody = customtkinter.CTkScrollableFrame(master=self.storeItemInfoSection, corner_radius=0)
        self.storeItemInfoSectionBody.grid(row=1, column=0, sticky="nsew")

        emptySection = customtkinter.CTkFrame(master=self.storeItemInfoSectionBody, fg_color="transparent", height=10)
        emptySection.pack()

    def showInputSection(self):
        # input frame
        self.inputFrame = customtkinter.CTkFrame(master=self.storeItemInfoSection, corner_radius=0, height=50, fg_color="#0B1826")
        self.inputFrame.grid(row=2, column=0, sticky="nsew")
        self.inputFrame.grid_columnconfigure(0, weight=3)
        self.inputFrame.grid_columnconfigure(1)
        self.inputFrame.grid_rowconfigure(0, weight=1)

        self.inputFrameText = customtkinter.CTkEntry(master=self.inputFrame, height=50, corner_radius=0, fg_color="transparent", text_color="#CCCCCC", placeholder_text="ENTER BID AMOUNT", placeholder_text_color="gray", border_color="#0F1D2E")
        self.inputFrameText.grid(row = 0, column = 0, sticky="nsew")
        # send button image
        self.inputFrameSendImage = customtkinter.CTkImage(dark_image=Image.open(os.path.join(os.path.dirname(__file__),"../../../../assets/img/bag.png")),size=(25, 25))
        # send button
        self.inputFrameSend = customtkinter.CTkButton(master=self.inputFrame, text=" ", corner_radius=0, border_color="#0F1D2E", image=self.inputFrameSendImage, compound="right", anchor="center")
        self.inputFrameSend.grid(row = 0, column = 1, stick = "nsew")


    def addBid (self):
        item = customtkinter.CTkFrame(master=self.storeItemInfoSectionBody, fg_color="#1C2E42", height=100, corner_radius=25)
        item.grid_rowconfigure(0, weight=0)
        item.grid_columnconfigure(0, weight=0)
        item.grid_columnconfigure(1, weight=1)
        item.pack(fill="both", padx=10, pady=3)

        itemAmountSection = customtkinter.CTkFrame(master=item, fg_color="transparent", corner_radius=15)
        itemAmountSection.grid_columnconfigure(0, weight=0)
        itemAmountSection.grid_rowconfigure(0, weight=0)
        itemAmountSection.grid_rowconfigure(1, weight=0)
        itemAmountSection.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        itemAmount = customtkinter.CTkLabel(master=itemAmountSection, text="PHP 3,000.00", fg_color="transparent", text_color="#A19C22")
        itemAmount.grid(row=0, column=0, sticky="nsew")

        itemAmountAwardButton = customtkinter.CTkButton(master=itemAmountSection, text="AWARD", fg_color="#217749", corner_radius=10, width=50)
        itemAmountAwardButton.grid(row=1, column=0, sticky="nsew")

        # user
        itemHeaderCreator = customtkinter.CTkFrame(master=item, fg_color="transparent")
        itemHeaderCreator.grid_rowconfigure(0, weight=0)
        itemHeaderCreator.grid_columnconfigure(0, weight=1)
        itemHeaderCreator.grid_columnconfigure(1, weight=0)
        itemHeaderCreator.grid(row=0, column=1, sticky="nsew", padx=10, pady=20)

        itemHeaderCreatorIcon = customtkinter.CTkImage(dark_image=Image.open(os.path.join(os.path.dirname(__file__),"../../../../assets/img/user-default.png")),size=(25, 25))
        itemHeaderCreatorIcon = customtkinter.CTkLabel(master=itemHeaderCreator, text=" ", image=itemHeaderCreatorIcon, anchor="n", compound="top", fg_color="transparent", corner_radius=0, padx=20, pady=10, width=50)
        itemHeaderCreatorIcon.grid(row = 0, column=1, sticky="nsew")

        itemHeaderCreatorSection = customtkinter.CTkFrame(master=itemHeaderCreator, fg_color="transparent")
        itemHeaderCreatorSection.grid_columnconfigure(0, weight=1)
        itemHeaderCreatorSection.grid_rowconfigure(0, weight=0)
        itemHeaderCreatorSection.grid_rowconfigure(1, weight=0)
        itemHeaderCreatorSection.grid(row=0, column=0, sticky="nsew")

        itemHeaderCreatorSectionHeaderCreatorName = customtkinter.CTkLabel(master=itemHeaderCreatorSection, text_color="white", text="John Hey Doe", anchor="e", compound="top", fg_color="transparent", height=10)
        itemHeaderCreatorSectionHeaderCreatorName.grid(row=0, column=0, sticky="new")

        itemHeaderCreatorSectionHeaderCreatorTime = customtkinter.CTkLabel(master=itemHeaderCreatorSection, text_color="white", text="January 01, 2023 3:00PM", font=customtkinter.CTkFont(size=10), anchor="e", compound="top", fg_color="transparent")
        itemHeaderCreatorSectionHeaderCreatorTime.grid(row=1, column=0, sticky="new")
       
