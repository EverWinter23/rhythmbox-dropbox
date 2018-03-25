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

        mp3_matches = self.dropcon.get_all_song_metadata()
        print("obtained metadata...making changes")
        
        # index for song entry
        
        k = 1
        for each_match in mp3_matches:
            try:
                # pass a dictionary ot create_entry_from_track_data for creating entries...
                # empty dictionary
                print("trying...")
                sound = {}
                # residue = mp3 extension
                sound['name'] = each_match.metadata.name
                sound['path'] = each_match.metadata.path_lower
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
