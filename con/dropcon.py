'''
5th march 2017 sunday
file=dropcon.py   lang=python3.5.2
frost_23 billy pilgrim has come unstuck in time
a small library for using dropbox api
'''
# imports
import webbrowser
import os
from dropbox import Dropbox
from dropbox.oauth import DropboxOAuth2Flow
from dropbox.dropbox import Dropbox
from dropbox.oauth import DropboxOAuth2FlowNoRedirect

# keys
APP_KEY = '4np8lmnpzci1ho0'
APP_SECRET = '45w9dbjkkkvyaie'


'''
dropbox object that can access your dropbox folder,
as well as download and upload files to dropbox....
'''
'''
attributes for class DropCon
 client
 dropbox
'''
class DropCon(object):
    '''
    parameters
        auth_code
         for authorizing access to dropbox
    '''
    def __init__(self, auth_code=None):
        '''Constructor'''
        print("establishing dropcon...")
        #if auth_code == None:      # no access_key token no client
        self.client = None      # now DropCon has attribute client
        self.dropbox = None
        self.access_token = None
        self.auth_flow = None
        self.userid = None

    '''
    about
        opens a webpage to authenticate dropbox connection
    '''
    def authenticate(self):
        print("starting authentication process...")
        self.auth_flow = DropboxOAuth2FlowNoRedirect(APP_KEY, APP_SECRET)
        # get the url which contains the authentication code
        auth_url = self.auth_flow.start()
        webbrowser.open_new(auth_url)

    '''
    about
        connects to Dropbox using DropboxOAuth2FlowNoRedirect
    parameters
        auth_code
         obtained from dropbox for authorization
    '''
    def connect(self, auth_code):
        print("trying to connect....")

        
        oauth_result = self.auth_flow.finish(auth_code)
        self.access_token = oauth_result.access_token
        self.client = Dropbox(self.access_token)
        #self.dropbox = Dropbox(self.access_token)
        '''
        except Exception as e:
            print("failed.....")
            print('Error: %s' % (e,))
            return
        '''

    '''
    about
        for the download option in the context menu
    parameters
        path
         the path to the file to be downloaded
        dirc
         file will be downloaded to directory dir
    '''
    def download_file(self, path, dirc):
        '''
        download the file passed
        '''
        filename = os.path.basename(path)
        response, metadata = self.client.get_file_and_metadata(path)

        destination = os.path.join(dirc, filename)

        out = open(destination, 'w')
        with response:
            out.write(response.read())

        return destination, metadata

    '''
    about
        upload a file to dropbox
    '''
    def upload_file(self):
        print("not implemented yet...")

    '''
    about
        returns the dropbox account information, such as
        user's display name, email address
    '''
    def get_account_information(self):
        return self.client.account_info()

    '''
    about
        get all songs from the dropbox
        only gets mp3 files
    '''
    def get_all_song_metadata(self):
        print("getting all song's metada...")
        search_result = self.client.files_search('', '.mp3')
        return search_result.matches

    '''
    about
        returns temporary link to the file, whose
        path has been provided
    '''
    def get_song_uri(self, song_path):
        return self.client.files_get_temporary_link(song_path).link

