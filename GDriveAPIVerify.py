

import httplib2
import pprint
import gnupg
from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from oauth2client.client import OAuth2WebServerFlow

gpg = gnupg.GPG(gnupghome='/home/hduser/Downloads/python-gnupg-0.3.6')
gpg.encoding = 'utf-8'

# Copy your credentials from the console
CLIENT_ID = 'YOUR CLIENT ID'
CLIENT_SECRET = 'YOUR CLIENT SECRET'

# Check https://developers.google.com/drive/scopes for all available scopes
OAUTH_SCOPE = 'https://www.googleapis.com/auth/drive'

# Redirect URI for installed apps
REDIRECT_URI = 'https://www.example.com/oauth2callback'

# Path to the file to upload
FILENAME = 'document.txt'

# Run through the OAuth flow and retrieve credentials
flow = OAuth2WebServerFlow(CLIENT_ID, CLIENT_SECRET, OAUTH_SCOPE, REDIRECT_URI)
authorize_url = flow.step1_get_authorize_url()
print 'Go to the following link in your browser: ' + authorize_url
code = raw_input('Enter verification code: ').strip()
credentials = flow.step2_exchange(code)

# Create an httplib2.Http object and authorize it with our credentials
http = httplib2.Http()
http = credentials.authorize(http)

drive = build('drive', 'v2', http=http)

# Downloading the file 

r = drive.files().list().execute()
files = r['items']
pprint.pprint(files[0]['title'])

f1 = files[0]
url = f1['downloadUrl']
r, c = http.request(url)
out = open('gdrive.txt', 'wb')
out.write(c)
out.close()
print "File Downloaded from Google Drive"
#Verifying the file
out = open('gdrive.txt', 'rb')
verified = gpg.verify_file(out)
if verified: 
    print "File downloaded from Google drive is verified!" 
else:
    print "not Verified" 
out.close()


#REFERENCES 

#https://developers.google.com/drive/web/about-sdk

#Google Drive SDK Downloading files youtube demo https://www.youtube.com/watch?v=SGR7TA4kyto

