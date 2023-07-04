from gtts import gTTS

class TTSWrapper:

    def __init__(self):
        self.lang = "en"

    def getTTS(self, prompt):
        myobj = gTTS(text=prompt, lang=self.lang, slow=False)
        myobj.save("gpt_response.mp3")    


if __name__ == "__main__":     
    tts = TTSWrapper()
    tts.getTTS("this is a test, hello world")   