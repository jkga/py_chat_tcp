import customtkinter

class SettingsWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.geometry("400x200")
        self.title("Settings")

        self.label = customtkinter.CTkLabel(self, text="Client Name")
        self.label.pack(padx=20, pady=10)

        self.nameEntry = customtkinter.CTkEntry(master=self, placeholder_text=f"{self.master.clientName}")
        self.nameEntry.pack(padx=20, pady=10)

        self.submitBtn = customtkinter.CTkButton(master=self, text="SUBMIT", fg_color="green", hover_color="#508617", command=self.saveName)
        self.submitBtn.pack(padx=20, pady=10)
    
    def saveName(self):
        self.master.clientName = self.nameEntry.get()
        self.master.renderClientName ()
        self.destroy ()
        
