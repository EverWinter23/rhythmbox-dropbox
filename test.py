import webbrowser
import os
from dropbox import Dropbox
from dropbox.oauth import DropboxOAuth2Flow
from dropbox.dropbox import Dropbox
from dropbox.oauth import DropboxOAuth2FlowNoRedirect

APP_KEY = '4np8lmnpzci1ho0'
APP_SECRET = '45w9dbjkkkvyaie'


auth_flow = DropboxOAuth2FlowNoRedirect(APP_KEY, APP_SECRET)
webbrowser.open_new(auth_flow.start())
auth_code = input('enter auth code... ')
access_token = auth_flow.finish(auth_code)

dbx = Dropbox(access_token)


search_result = dbx.files_search('', '.mp3')
