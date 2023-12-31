import tkinter
from tkinter import *
from tkinter import messagebox, scrolledtext
from gpt_api import GPTWrapper
from tts_api import TTSWrapper

class GPTGUI:

    def __init__(self, root):
        self.root = root
        self.gpt_api = GPTWrapper()
        self.tts_api = TTSWrapper()
        self.gui_font = "Arial"
        self.text_area = None
        self.gpt_text_area = None

    def setWindow(self):
        self.root.geometry("600x400")
        self.root.resizable(width = False, height = False)
        self.root.title('JDG 2023')
        Label(self.root, text ='ChatGPT GUI/API Wrapper', font=(self.gui_font, 20, "italic")).place(x = 150, y = 5)

    def setTextBoxes(self):
        Label(self.root, text = 'Enter ChatGPT prompt').place(x = 15, y = 70)
        Label(self.root, text = 'GPT Response').place(x = 15, y = 180)

        self.text_area = scrolledtext.ScrolledText(self.root, 
                                      wrap = WORD, 
                                      width = 40, 
                                      height = 1, 
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
        startBtn = Button(self.root, text ="Generate Response", command = self.genResponse)
        startBtn.place(x = 150, y = 340)
        saveTTSBtn = Button(self.root, text ="Generate Text-To-Speech", command = self.prepareTTS)
        saveTTSBtn.place(x = 300, y = 340)

    def prepareTTS(self):
        entry = self.gpt_text_area.get("1.0", "end-1c")    
        if len(entry) < 0 or entry == " ": return None
        self.tts_api.getTTS(entry)

    def genResponse(self):
        entry = self.text_area.get("1.0","end-1c")
        if len(entry) < 0 or entry == " ": return None
        response = self.gpt_api.get_response(entry)
        self.gpt_text_area.insert(END, response + "\n\n")

    def run(self):
        self.setWindow()
        self.setTextBoxes()
        self.root.mainloop() 

if __name__ == "__main__":
    gui = GPTGUI(Tk())    
    gui.run()