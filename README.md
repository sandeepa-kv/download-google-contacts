# download-google-contacts

## Requirements

1. Python 3.x
2. pip compatible with Python 3.x

### Generate a Google Application and export credentials
1. Create a project here: https://console.developers.google.com/
2. Select "Enable APIs and Services" and enable Contacts API
3. Under "Credentials", run "Create Credentials" and create a "OAuth client ID"
4. Place the created file under "credentials.json" in the project

### Install dependencies

pip3 install -r requirements.txt

## Usage

python3 download_google_contacts.py

* Login to your Google account when prompted.
* Ignore the "This app isn't verified" warning as this is a test application.

## Test 

python3 -m unittest test_download_google_contacts.py

## Scenarions automated
* Getting user contact list
* Empty contact list
* Error scenario
  
## Scenario can't be automated
* Google login test automation. Google oauthplayground doesn't allow a pure programmatic way to test token based authentication.
