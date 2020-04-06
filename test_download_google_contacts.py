import unittest
import httpretty
import json
import re

from download_google_contacts import ContactsDownload

class downloadContactsTest(unittest.TestCase):
    @httpretty.activate
    def setUp(self):
        self.contactsDownload = ContactsDownload(credentials_file='credentials.json', token_file='token.pickle',
                                    export_file='contacts.json')

    @httpretty.activate
    def test_contacts_list(self):
        url = re.compile("https://www.google.com/m8/feeds/contacts/(\*)")
        with open('contacts_list_mock.json') as json_res:
            body = json.load(json_res)
        httpretty.register_uri(
            httpretty.GET,
            url,
            body= body
        )
        self.contactsDownload.fetch_contacts()
        last_request = httpretty.last_request()
        self.assertEqual(last_request.method, 'GET')
        self.assertTrue(self.contactsDownload.contacts)
        self.assertEqual(len(self.contactsDownload.contacts), 1)

    @httpretty.activate
    def test_empty_contact_list(self):
        url = re.compile("https://www.google.com/m8/feeds/contacts/(\*)")
        with open('empty_contacts_mock.json') as json_res:
            body = json.load(json_res)
        httpretty.register_uri(
            httpretty.GET,
            url,
            body=body
        )
        self.contactsDownload.fetch_contacts()
        last_request = httpretty.last_request()
        self.assertEqual(last_request.method, 'GET')
        self.assertFalse(self.contactsDownload.contacts)

    @httpretty.activate
    def test_errors(self):
        url = re.compile("https://www.google.com/m8/feeds/contacts/(\*)")
        httpretty.register_uri(
            httpretty.GET,
            url,
            body='{"error": "Not Found"}'
        )
        self.contactsDownload.fetch_contacts()
        last_request = httpretty.last_request()
        self.assertEqual(last_request.method, 'GET')
        self.assertFalse(self.contactsDownload.contacts)


    if __name__ == '__main__':
        import xmlrunner

        unittest.main(
            testRunner=xmlrunner.XMLTestRunner(output='test-reports'),
            failfast=False,
            buffer=False,
            catchbreak=False)

