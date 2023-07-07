import requests
import html2text
from gpt_api import GPTWrapper

class OutlookAPI:

    def __init__(self):
        self.auth_token = ""
        self.auth_token_send = ""
        self.outlook_inbox_url = "https://graph.microsoft.com/v1.0/me/mailfolders/inbox/messages"
        self.outlook_send_url = "https://graph.microsoft.com/v1.0/me/sendMail"
        self.outlook_draft_url = "https://graph.microsoft.com/v1.0/me/messages"
        self.gpt_wrapper = GPTWrapper()


    def construct_email_data(self, content):
        my_data = {
            "message": {
                "subject": "Test email from the API!",
                "body" : {
                        "contentType": "HTML",
                        "content": str(content)
                },
                "toRecipients": [{
                    "emailAddress": {
                    "address": "johnglatts1@hotmail.com"
                    }
                }],
            }
        }
        return my_data
    
    def construct_draft_data(self, content):
        my_data = {
            "subject": "This is a draft",
            "body": {
                "contentType": "HTML",
                "content": str(content)
             },
            "toRecipients": [{
                "emailAddress": {
                    "address": "johnglatts1@hotmail.com"
                }
            }]
        }
        return my_data

    def send_email(self, content):
        headers = { "Authorization": self.auth_token_send }  
        ret = requests.post(self.outlook_send_url, json=self.construct_email_data(content), headers=headers) 
        print(ret.status_code)

    def send_draft(self, content):
        headers = { "Authorization": self.auth_token_send }  
        ret = requests.post(self.outlook_draft_url, json=self.construct_draft_data(content), headers=headers) 
        print(ret.status_code)

    def get_email_address(self, res):
        return res['from']['emailAddress']['address']

    def get_email_name(self, res):
        return res['from']['emailAddress']['name']

    def get_email_subject(self, res):
        return res["subject"]
    
    def get_email_body(self, res):
        h = html2text.HTML2Text()
        h.ignore_links = True
        h.ignore_images = True
        h.ignore_tables = True
        # will need to some addnlt work to go through the table
        return h.handle(res['body']['content']).lower()
    
    def gen_gpt_response(self, msg):
        prompt = "write an email response, in a professional tone, to the following message: " + msg
        res = self.gpt_wrapper.get_response(prompt)
        print("\n\nGPT generated the following email response: " + str(res))
        self.send_draft(res)

    def test_get(self, n=5):
        headers = { "Authorization" : self.auth_token }    
        url = self.outlook_inbox_url + "?select=subject,from,receivedDateTime,body&$top=" + str(n)
        res = requests.get(url, headers=headers)
        
        for i in range(n):
            print(self.get_email_address(res.json()["value"][i]))
            print(self.get_email_name(res.json()["value"][i]))
            print(self.get_email_subject(res.json()["value"][i]))
            print(self.get_email_body(res.json()["value"][i]))
            print()

    def test_post(self):
        self.send_email("Hello world this a test")    
        self.send_draft("Hello world this a draft")  


if __name__ == "__main__":
    outApi = OutlookAPI()
    outApi.test_get(n=5)        
    #outApi.test_post()