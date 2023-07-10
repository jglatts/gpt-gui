import tkinter
from tkinter import *
from tkinter import messagebox, scrolledtext
from gpt_api import GPTWrapper
from outlook_api import OutlookAPI

class OutlookGUI:

    def __init__(self, root):
        self.root = root
        self.gpt_api = GPTWrapper()
        self.outlook_api = OutlookAPI()
        self.gui_font = "Arial"
        self.text_area = None
        self.gpt_text_area = None
        self.email_idx = 0

    def setWindow(self):
        self.root.geometry("600x400")
        self.root.resizable(width = False, height = False)
        self.root.title('JDG 2023')
        Label(self.root, text ='ChatGPT-Email Helper', font=(self.gui_font, 20, "italic")).place(x = 150, y = 5)

    def setTextBoxes(self):
        Label(self.root, text = 'Current Email').place(x = 15, y = 70)
        Label(self.root, text = 'GPT Response').place(x = 15, y = 180)

        self.text_area = scrolledtext.ScrolledText(self.root, 
                                      wrap = WORD, 
                                      width = 40, 
                                      height = 5, 
                                      font = (self.gui_font,
                                              10))
        self.text_area.grid(column = 5, pady = 10, padx = 10)
        self.text_area.place(x=160, y=75)
        self.gpt_text_area = scrolledtext.ScrolledText(self.root, 
                                      wrap = WORD, 
                                      width = 40, 
                                      height = 9, 
                                      font = (self.gui_font,
                                              10))
        self.gpt_text_area.grid(column = 5, pady = 10, padx = 10)
        self.gpt_text_area.place(x=160, y=180)
        loadEmailBtn = Button(self.root, text ="Load Emails", command = self.loadEmail)
        loadEmailBtn.place(x = 15, y = 90)
        startBtn = Button(self.root, text ="Generate Response", command = self.genResponse)
        startBtn.place(x = 150, y = 340)
        nextEmailBtn = Button(self.root, text ="Next Email", command = self.nextEmail)
        nextEmailBtn.place(x = 300, y = 340)

    def showEmailSubject(self):
        self.emails = self.outlook_api.get_mail(n=50) # get 50 emails
        email_data = self.outlook_api.get_email_body(self.emails[self.email_idx])
        self.text_area.insert(END, email_data + "\n\n")        

    def loadEmail(self):
        self.emails = self.outlook_api.get_mail(n=50) # get 50 emails
        email_data = self.outlook_api.get_email_address(self.emails[self.email_idx]) + "\n" + self.outlook_api.get_email_subject(self.emails[self.email_idx])
        self.text_area.insert(END, email_data + "\n\n")
        self.showEmailSubject()

    def nextEmail(self):
        self.gpt_text_area.delete("1.0", END)
        self.text_area.delete("1.0", END)
        self.email_idx += 1
        self.loadEmail()
            
    def genResponse(self):
        email_address = self.outlook_api.get_email_address(self.emails[self.email_idx])
        email_id = self.outlook_api.get_email_id(self.emails[self.email_idx])
        entry = self.outlook_api.get_email_body(self.emails[self.email_idx])
        if len(entry) < 0 or entry == " ": return None
        msg = "write an email response to the following message: " + entry
        response = self.gpt_api.get_response(msg)
        self.gpt_text_area.insert(END, response + "\n\n")
        self.outlook_api.send_email_reply(email_id, email_address, response)

    def run(self):
        self.setWindow()
        self.setTextBoxes()
        self.root.mainloop() 

if __name__ == "__main__":
    gui = OutlookGUI(Tk())    
    gui.run()