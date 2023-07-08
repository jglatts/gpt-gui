import requests
import html2text
from gpt_api import GPTWrapper
from email_body_gen import EmailBody

class OutlookAPI:

    def __init__(self):
        self.auth_token = ""
        self.outlook_inbox_url = "https://graph.microsoft.com/v1.0/me/mailfolders/inbox/messages"
        self.outlook_send_url = "https://graph.microsoft.com/v1.0/me/sendMail"
        self.outlook_draft_url = "https://graph.microsoft.com/v1.0/me/messages"
        self.headers = { "Authorization": self.auth_token }
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
                "content": EmailBody.email_body_gen("John", content)
             },
            "toRecipients": [{
                "emailAddress": {
                    "address": "johnglatts1@hotmail.com"
                }
            }]
        }
        return my_data
    
    def construct_reply_data(self, to_email, content):
        my_data = {
            "message":{  
                "toRecipients":[{
                    "emailAddress": {
                    "address": str(to_email)
                    }
                }]
            },
            "comment": str(content)
            }
        return my_data

    def send_email(self, content):
        ret = requests.post(self.outlook_send_url, json=self.construct_email_data(content), headers=self.headers) 
        print(ret.status_code)

    def send_email_reply(self, email_id, email_address, content):
        url = self.outlook_draft_url + "/" + str(email_id) + "/createReply"
        ret = requests.post(url, json=self.construct_reply_data(email_address, content), headers=self.headers) 
        print(ret.status_code)

    def send_draft(self, content):
        ret = requests.post(self.outlook_draft_url, json=self.construct_draft_data(content), headers=self.headers) 
        print(ret.status_code)

    def get_email_id(self, res):
        return res['id']    

    def get_email_address(self, res):
        return res['from']['emailAddress']['address']

    def get_email_name(self, res):
        return res['from']['emailAddress']['name']

    def get_email_subject(self, res):
        return res['subject']
    
    def get_email_body(self, res):
        h = html2text.HTML2Text()
        h.ignore_links = True
        h.ignore_images = True
        h.ignore_tables = True
        return h.handle(res['body']['content']).lower()
    
    def gen_gpt_response(self, msg):
        prompt = "write an email response, in a professional tone, to the following message: " + msg
        res = self.gpt_wrapper.get_response(prompt)
        print("\n\nGPT generated the following email response: " + str(res))
        self.send_draft(res)

    def get_mail(self, n):
        url = self.outlook_inbox_url + "?select=subject,from,receivedDateTime,body&$top=" + str(n)
        res = requests.get(url, headers=self.headers)
        return  res.json()["value"]

    def test_get(self, n=5):
        checked_words = []
        data = self.get_mail(n)

        for i in range(n):
            print(self.get_email_address(data[i]))
            print(self.get_email_name(data[i]))
            print(self.get_email_subject(data[i]))
            print(self.get_email_id(data[i]))
            print(self.get_email_body(data[i]))
            if self.get_email_address(data[i]) in checked_words:
                self.gen_gpt_response(self.get_email_body(data[i]))
            print()

    def test_post(self):
        self.send_email("Hello world this a test")    
        self.send_draft("Hello world this a draft")  

    def test_reply(self):
        email_data = self.get_mail(1)
        msg = "write an email response, in a professional tone, to the following email: \n"
        msg += self.get_email_body(email_data[0])
        response = self.gpt_wrapper.get_response(msg)
        self.send_email_reply(self.get_email_id(email_data[0]), self.get_email_address(email_data[0]), response)
        
    def test():
        outApi = OutlookAPI()
        outApi.test_get(n=25)        
        outApi.test_post()  
        outApi.test_reply()      


if __name__ == "__main__":
    OutlookAPI.test()