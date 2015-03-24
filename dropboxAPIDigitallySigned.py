# Hrishikesh Potdar
# Student ID 1001048659
# Course CSE 6331 


# Include the Dropbox SDK
import dropbox
import gnupg
import sys
import os
import base64
import webbrowser
import Tkinter, tkFileDialog
from Tkinter import *
import Tkinter, tkFileDialog
from Tkinter import Tk
from tkFileDialog import askopenfilename
import time    


#from tkinter.filedialog import askopenfilename



# Get your app key and secret from the Dropbox developer website
app_key = 'YOUR APP KEY'
app_secret = 'YOUR APP SECRET'

gpg = gnupg.GPG(gnupghome='/home/hduser/Downloads/python-gnupg-0.3.6')
gpg.encoding = 'utf-8'

#input_data = gpg.gen_key_input(key_type="RSA", key_length=1024)
#key = gpg.gen_key(input_data)

flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)

# Have the user sign in and authorize this token
authorize_url = flow.start()
print '1. Go to: ' + authorize_url
print '2. Click "Allow" (you might have to log in first)'
print '3. Copy the authorization code.'
code = raw_input("Enter the authorization code here: ").strip()

access_token, user_id = flow.finish(code)
client = dropbox.client.DropboxClient(access_token)
print 'linked account: ', client.account_info()

# Data with digtal signature
filenamecode = askopenfilename()
print filenamecode
filename=os.path.basename(filenamecode);
stream = open(filename, 'rb')
signed_data = gpg.sign_file(stream)
finalfile = signed_data.data
response = client.put_file(filename, finalfile )
print "uploaded:", response
stream.close()

#sleep till file is uploaded
time.sleep(4)

#download the file
f, metadata = client.get_file_and_metadata(filename)   
out = open(filename, 'wb')
out.write(f.read())
print "Encrypted file has been downloaded" , out
out.close()

#verify the file
out = open(filename, 'rb')


verified = gpg.verify_file(out)
if verified: 
    print "Signature of the downloaded file", filename ,"is verified!" 
else:
    print "not Verified" 
out.close()


#REFERENCES 

#https://pythonhosted.org/python-gnupg/ python GNUPG

#https://www.dropbox.com/developers
