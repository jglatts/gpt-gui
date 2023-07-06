import requests
import html2text

class OutlookAPI:

    def __init__(self):
        self.auth_token = "your-microsoft-token"
        self.outlook_inbox_url = "https://graph.microsoft.com/v1.0/me/mailfolders/inbox/messages"
        self.outlook_sent_images_url = "https://graph.microsoft.com/v1.0/me/mailfolders/SentItems/messages"

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

            

if __name__ == "__main__":
    outApi = OutlookAPI()
    outApi.test()        