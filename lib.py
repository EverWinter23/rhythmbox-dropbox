'''
5th match 2017 sunday
file=lib.py     lang=python3.5.2
'''
from gi.repository import GObject
from source import DropboxSource

# inherits from DropboxSource
class DropboxLibrary(DropboxSource):
    '''
    attributes
        dropcon
         an object of class DropCon
    '''
    def load_songs(self):
        print("loading songs using dropcon...")

        (mp3_metadata, mp3_tags) = self.dropcon.get_all_song_paths()
        print("obtained metadata...")
        print(mp3_metadata)
        print('=============================================')
        print(mp3_tags)
        '''
        right now i straight away add the song paths
        to the shell... 5th march 2017 sunday
        '''
        '''
        song_list = []
        for each_metadata in mp3_metadata:
            if each_metadata['mime_type'] == 'audio/mpeg':
                song_list.append(each_metadata['path'])
        '''

        # index for song entry
        k = 1
        for each_metadata in mp3_metadata:
            try:
                # pass a dictionary ot create_entry_from_track_data for creating entries...
                # empty dictionary
                print("trying...")
                sound = {}
                # residue = mp3 extension
                sound['name'], residue = (each_metadata['path'].split('/')[-1]).split('.')
                sound['path'] = each_metadata['path']
                sound['trackNumber'] = k
                k += 1
                print("sending information for creation of track data...")
                print("adding entry to query model...")
                entry = self.create_entry_from_track_data(sound)
                self.props.base_query_model.add_entry(entry, -1)
                print("entry added to query model...")
            except TypeError:   # already in db
                print("Type error")
                pass
        shell = self.props.shell
        shell.props.db.commit()
        print("the songs have been loaded...")
# register the source or it will produce segmentation fault later...
GObject.type_register(DropboxLibrary)
