import os.path
import pickle
import requests
import json
import sys
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

class ContactsDownload(object):
    scopes = ['https://www.googleapis.com/auth/contacts.readonly']
    max_results = 25
    contacts_url = 'https://www.google.com/m8/feeds/contacts/default/full?alt=json&max-results=%s' % (max_results)

    def __init__(self, credentials_file='credentials.json', token_file='token.pickle', export_file='contacts.json'):
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.export_file = export_file
        self.token = None
        self.contacts = []

        if os.path.exists(self.token_file):
            with open(self.token_file, 'rb') as credentials:
                self.token = pickle.load(credentials)

        if not self.token or not self.token.valid:
            if self.token and self.token.expired and self.token.refresh_token:
                self.token.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.credentials_file, ContactsDownload.scopes)
                self.token = flow.run_local_server()

            with open(self.token_file, 'wb') as token_file:
                pickle.dump(self.token, token_file)

    def fetch_contacts(self):
        next_url = ContactsDownload.contacts_url
        while next_url:
            print('  Fetching from: %s' % (next_url))
            try:
                request = requests.get(next_url,
                    headers = {
                        'Authorization': 'OAuth %s' % (self.token.token)
                    })

                response = json.loads(request.text)
                self.contacts += response['feed']['entry']
                next_url = [link['href'] for link in response['feed']['link'] if link['rel'] == 'next']
                if next_url:
                    next_url = next_url[0]
            except:
                print('Unexpected error:', sys.exc_info()[0])
                raise

    def export_contacts(self):
        with open(self.export_file, 'w', newline='') as jsonfile:
            jsonfile.write(json.dumps(self.contacts))

if __name__ == '__main__':
    contacts_download = ContactsDownload()

    print('Fetching contacts... (might take a while)')
    contacts_download.fetch_contacts()

    print('Exporting contacts to %s...' % (contacts_download.export_file))
    contacts_download.export_contacts()
