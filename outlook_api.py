import requests
import html2text

class OutlookAPI:

    def __init__(self):
        self.auth_token = ""
        self.auth_token_send = ""
        self.outlook_inbox_url = "https://graph.microsoft.com/v1.0/me/mailfolders/inbox/messages"
        self.outlook_send_url = "https://graph.microsoft.com/v1.0/me/sendMail"
        self.outlook_draft_url = "https://graph.microsoft.com/v1.0/me/messages"

    def construct_email_data(self, content):
        my_data = {
            "message": {
                "subject": "Test email from the API!",
                "body" : {
                        "contentType": "Text",
                        "content": str(content)
                },
                "toRecipients": [{
                    "emailAddress": {
                    "address": "johnglatts1@hotmail.com"
                    }
                }],
            },
            "saveToSentItems": "true"
        }
        return my_data

    def send_email(self, content):
        headers = { "Authorization": self.auth_token_send }  
        ret = requests.post(self.outlook_send_url, json=self.construct_email_data(content), headers=headers) 
        print(ret.text)

    def send_draft(self, content):
        headers = { "Authorization": self.auth_token_send }  
        # need to test in explorer
        ret = requests.post(self.outlook_draft_url, json=self.construct_email_data(content), headers=headers) 
        print(ret.text)        

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
        return h.handle(res['body']['content'])

    def test(self):
        n = 5
        headers = { "Authorization" : self.auth_token }    
        url = self.outlook_inbox_url + "?select=subject,from,receivedDateTime,body&$top=" + str(n)
        res = requests.get(url, headers=headers)
        for i in range(n):
            print(self.get_email_address(res.json()["value"][i]))
            print(self.get_email_name(res.json()["value"][i]))
            print(self.get_email_subject(res.json()["value"][i]))
            print(self.get_email_body(res.json()["value"][i]))
            print()

        self.send_email("Hello world this a test")    
        self.send_draft("Hello world this a draft")  



if __name__ == "__main__":
    outApi = OutlookAPI()
    outApi.test()        