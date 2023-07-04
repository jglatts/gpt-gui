import openai

class GPTWrapper:

    def __init__(self):
        self.key = "your-api-key"

    def getPrompt(self):
        ret = input("Enter prompt for gpt: ")
        return ret

    def get_response(self, content):
        openai.api_key = self.key
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": content}])
        return response.choices[0].message.content

    def run(self):
        openai.api_key = self.key
        while (True):
            prompt = self.getPrompt()
            if len(prompt) == 0: continue
            content = [{"role": "user", "content": prompt}]
            response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=content)
            reply = response.choices[0].message.content
            print(f"\n{reply}")


if __name__ == "__main__":
    gptWrapper = GPTWrapper()
    gptWrapper.run()