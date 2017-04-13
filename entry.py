'''
5th march 2017 sunday
file=entry.py     lang=python3.5.2
i have a practical exam tommorrow
'''
# imports
from gi.repository import RB
'''
about
    the most important data structure in the database - RhythmDB
    the entry RB.RhythmDBEntry represents a single track
    each entry has a set of properties with associated values such as
        'title', 'artist', 'play count' and so on...
        'location' which must be unique among all the entries in the db
attributes
    dropcon
     the dropbox client and dropbox
'''
class DropboxEntryType(RB.RhythmDBEntryType):
    '''attributes'''
    client = None

    def __init__(self, dropcon=None):
        # make it dropbox-music later... Done
        RB.RhythmDBEntryType.__init__(self, name='drobox-music')
        if dropcon != None:
            self.client = dropcon.client

    '''
    about
        returns a string containing the playback uri for entry
        returns null if the entry cannot be played...
    '''
    def do_get_playback_uri(self, entry):
        print("getting the playback uri for dropbox-music entry")

        song_path = entry.dup_string(RB.RhythmDBPropType.LOCATION)
        entry_metadata = self.client.media(song_path)
        uri = entry_metadata['url']

        return uri

    def do_can_sync_metadata(self, entry):
        return True
