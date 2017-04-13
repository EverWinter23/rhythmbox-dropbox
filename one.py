'''
5th march 2017 sunday
file=plugin.py       lang=python3.5.2
rich guys with frozen ass sets
'''
# imports
import rb
from gi.repository import GObject, Peas, RB, Gio, Gtk
import dropbox
from con.dropcon import DropCon
#from source import DropboxSource
#from lib import DropboxLibrary

# keys
APP_KEY = '4np8lmnpzci1ho0'
APP_SECRET = '45w9dbjkkkvyaie'

dbx = None
client = None

# only for me
APP_TOKEN = 'bMxXoASKyNAAAAAAAAAAYlWGtAUZiosUo3zpKVCWKZJmhC9PvKDBLYZP6sHIbPsv'

'''
attributes
    object
     a reference to the shell object
    source
     contains all entries of songs from dropbox
'''
class DropboxPlugin(GObject.Object, Peas.Activatable):
    '''attributes'''
    # the following object is a reference to the shell object
    __gtype_name = 'DropboxPlugin'
    object = GObject.property(type=GObject.GObject)
    #source = None

    def __init__(self):
        # inherit from GObject.GObject
        GObject.Object.__init__(self)

    '''
    about
        called by rhythmbox when the plugin is activated. it creates the plugin's
        source and connects signals to manage the plugin's preferences
    '''
    def do_activate(self):
        print("plugin activating...")

        #self.do_deactivate()
         # get a reference to the DropboxPlugin object
        shell = self.object
        # add folder dropbox-music/icons for getting the icon
        rb.append_plugin_source_path(self, 'icons')
        # get a database reference for shell database
        db = shell.props.db     # the RB.RhythmDB
        # query model for sorting by artist, album...
        # new_empty() constructs a new empty query model
        model = RB.RhythmDBQueryModel.new_empty(db)

        # setup dropbox source
        # GObject.new() takes * parameters
        #   a. object_type <- this is my source
        #   b. parameters  <- can be multiple
        # parameters is an array of GObject.Parameter
        self.source = GObject.new(DropboxLibrary,
                                    shell=shell,
                                    name=_('Dropbox'),
                                    query_model=model,
                                    plugin=self,
                                    icon=Gio.ThemedIcon.new('dropboxO'))
        # setup source
        print("setting up source...")
        self.source.setup()
        print("source setup completed...")

        # get the group from the shell
        group = RB.DisplayPageGroup.get_by_id('library')
        # add the source to the music library
        shell.append_display_page(self.source, group)
        print("plugin activated...")

    # deactivate the plugin
    def do_deactivate(self):
        print("deactivating the plugin...")
        self.source.delete_thyself()
        self.source = None      # avoid dangling pointer


'''
5th march 2017 sunday
file=entry.py     lang=python3.5.2
i have a practical exam tommorrow
'''

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
    #client = None

    def __init__(self):
        # make it dropbox-music later
        RB.RhythmDBEntryType.__init__(self, name='droboxmusic')
        #if dropcon != None:
        #    self.client = dropcon.client

    '''
    about
        returns a string containing the playback uri for entry
        returns null if the entry cannot be played...
    '''
    def do_get_playback_uri(self, entry):
        global client
        print("getting the playback uri for dropbox-music entry")

        song_path = entry.dup_string(RB.RhythmDBPropType.LOCATION)
        entry_metadata = client.media(song_path)
        uri = entry_metadata['url']

        return uri

    def do_can_sync_metadata(self, entry):
        return True

# only for me
# to be removed
'''
class
 inherits from RB.Source
attributes
    songs_view
     creates the page for viewing songs
    shell
     a reference to the shell object
    browser
     to browse all the songs
    search_widget
     a widget to search for a particular song
    top_box
     to add login button and the label
     ? what label... The Label
    dropcon
     for connecting to dropbox


'''


dropbox_entry = DropboxEntryType()
class DropboxSource(RB.Source):
    def setup(self):
        # RB.Source.props.shell
        shell = self.props.shell
        self.songs_view = RB.EntryView.new(
            db = shell.props.db,
            shell_player = shell.props.shell_player,
            is_drag_source=True,
            is_drag_dest=False,
        )

        # columns to add to the songs_view
        # I prefer play_count, title and duration
        #self.songs_view.append_column(RB.EntryViewColumn.PLAY_COUNT, True,)
        self.songs_view.append_column(RB.EntryViewColumn.TITLE, True,)
        #self.songs_view.append_column(RB.EntryViewColumn.DURATION, True,)

        # what does this do??
        self.songs_view.connect('notify::sort-order',
            lambda *args, **kwargs: self.songs_view.resort_model(),
        )
        self.songs_view.connect('entry-activated',
            lambda view, entry: shell.props.shell_player.play_entry(entry, self),
        )

        self.vbox = Gtk.Paned.new(Gtk.Orientation.VERTICAL)
        self.top_box = Gtk.VBox()

        # need to remove the login option...
        #global dbx
        if dbx != None:
            print('done...........................')
            self.init_authenticated()
            print('killing box')

        if 1 == 1:
            infobar = Gtk.InfoBar()
            self.top_box.pack_start(infobar, True, True, 0)
            infobar.set_message_type(Gtk.MessageType.INFO)
            # add a login button
            auth_btn = infobar.add_button(_("Login"), 1)
            auth_btn.connect('clicked', self.auth)
            # the label for authorization
            label = Gtk.Label(_("Requires authorization for accessing Dropbox..."))
            infobar.get_content_area().add(label)
        self.browser = RB.LibraryBrowser.new(shell.props.db, dropbox_entry)
        self.browser.set_model(self.props.base_query_model, False)
        self.browser.connect("notify::output-model", self.update_view)
        self.browser.set_size_request(-1, 200)

        self.search_widget = RB.SearchEntry.new(False)
        self.search_widget.connect("search", self.on_search)

        # sets the position for the search box...
        # gkt.Alignment(xalign, yalign, xscale, yscale)
        # argumetns are floating point numbers from 0.0 to 1.0
        search_box = Gtk.Alignment.new(0.99, 0, 0.1, 1)

        #search_box = Gtk.Alignment.new(1, 0, 0, 1)
        search_box.add(self.search_widget)

        self.top_box.pack_start(search_box, False, False, 5)
        self.top_box.pack_start(self.browser, True, True, 0)

        # kinda self explanatory...
        self.update_view()

        self.vbox.add1(self.top_box)
        self.vbox.add2(self.songs_view)
        self.pack_start(self.vbox, True, True, 0)
        print("finishing source set up...")

        # make the gui visible
        self.show_all()

    def do_impl_show_entry_popup(self):
        menu = Gtk.Menu.new_from_model(self.__popup)
        menu.attach_to_widget(self, None)
        menu.popup(None, None, None, None, 3, Gtk.get_current_event_time())


    def on_search(self, entry, text):
        db = self.props.shell.props.db
        query_model = RB.RhythmDBQueryModel.new_empty(db)
        query = GLib.PtrArray()
        db.query_append_params(
            query, RB.RhythmDBQueryType.FUZZY_MATCH,
            RB.RhythmDBPropType.COMMENT, text.lower(),
        )
        db.query_append_params(
            query, RB.RhythmDBQueryType.EQUALS,
            RB.RhythmDBPropType.GENRE, 'dropbox-music',  # shit!
        )
        db.do_full_query_parsed(query_model, query)
        self.browser.set_model(query_model, False)
        self.update_view()

    def update_view(self, *args):
        self.songs_view.set_model(self.browser.props.output_model)
        self.props.query_model = self.browser.props.output_model

    def init_authenticated(self):
        print("authenticating...")

        if hasattr(self, 'auth_box'):
            print("removing the top box...")
            self.top_box.remove(self.auth_box)

        self.load_songs()

    def auth(self, widget):
        access_token = APP_TOKEN
        print("connecting to dropbox...")

        #mp3 = dbx.files_search('', '*.mp3', start=0, max_results=100, mode=dropbox.files.SearchMode('filename', None))
        #print(mp3)

        # make a dropbox connection
        #self.dropcon = DropCon(access_token)
        '''copy pasted code'''
        global dbx
        global client
        dbx = dropbox.Dropbox(access_token)
        client = dropbox.client.DropboxClient(access_token)
        #mp3 = dbx.files_search('', '*.mp3', start=0, max_results=100, mode=dropbox.files.SearchMode('filename', None))
        #print(mp3)
        if dbx != None:
            print('connected.............')
            self.init_authenticated()

        '''
        if self.dropcon != None:
            print('connected.............')
            self.init_authenticated()
        '''
        '''
        dialog = AuthDialog()
        response = dialog.run()
        flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)

        authorize_url = flow.start()
        webbrowser.open_new(authorize_url)

        if response == Gtk.ResponseType.OK:
            access_token = dialog.login_input.get_text()
            #password = dialog.password_input.get_text()
            #set_credentials(login)
            dbx = dropbox.Dropbox(access_token)
        dialog.destroy()
        '''

    def do_impl_get_entry_view(self):
        return self.songs_view

    def create_entry_from_track_data(self, path):
        shell = self.props.shell
        db = shell.props.db

        print('creating entry for path', path)
        print("path printed")

        #tag = stagger.read_tag(path)
        #print(tag.title)

        #dropbox_entry = DropboxEntryType()
        entry = RB.RhythmDBEntry.new(
            db, dropbox_entry, path,
            )

        db.entry_set(
            entry, RB.RhythmDBPropType.TITLE,
            path
            )
        print('done............')
        '''
        full_title.append(track['title'])
        if 'durationMillis' in track:
            db.entry_set(
                entry, RB.RhythmDBPropType.DURATION,
                int(track['durationMillis']) / 1000,
                )
        if 'album' in track:
            db.entry_set(
                entry, RB.RhythmDBPropType.ALBUM,
                track['album'],
                )
            full_title.append(track['album'])
        if 'artist' in track:
            db.entry_set(
                entry, RB.RhythmDBPropType.ARTIST,
                track['artist'],
                )
            full_title.append(track['artist'])
        if 'trackNumber' in track:
            db.entry_set(
                entry, RB.RhythmDBPropType.TRACK_NUMBER,
                int(track['trackNumber']),
                )
        if 'albumArtRef' in track:
            db.entry_set(
                entry, RB.RhythmDBPropType.MB_ALBUMID,
                track['albumArtRef'][0]['url'],
                )
        # rhytmbox OR don't work for custom filters
        db.entry_set(
            entry, RB.RhythmDBPropType.COMMENT,
            ' - '.join(full_title).lower(),
            )
        # rhythmbox segfoalt when new db created from python
        db.entry_set(
            entry, RB.RhythmDBPropType.GENRE,
            'google-play-music',
            )
        '''
        return entry

    def load_songs(self):
        raise NotImplementedError


# inherits from DropboxSource
class DropboxLibrary(DropboxSource):
    '''
    attributes
        dropcon
         an object of class DropCon
    '''
    def load_songs(self):

        '''
        print("loading songs...")

        mp3_metadata = self.dropcon.get_all_song_paths()
        print("here...")

        right now i straight away add the song paths
        to the shell... 5th march 2017 sunday

        song_list = []
        for each_metadata in mp3_metadata:
            if each_metadata['mime_type'] == 'audio/mpeg':
                song_list.append(each_metadata['path'])

        for each_song_path in song_list:
            try:
                entry = self.create_entry_from_track_data(each_song_path)
                self.props.base_query_model.add_entry(entry, -1)
            except TypeError:   # already in db
                pass
        shell = self.props.shell
        shell.props.db.commit()
        '''

        #client = self.dropcon.client
        print('loading songs..........')
        shell = self.props.shell
        global client
        list_mp3 = client.search('/', '.mp3')

        '''
        #folder_metadata = client.metadata("/")
        #print(folder_metadata)
        #folder_contents = folder_metadata['contents']
        print('==============================================')
        print(folder_contents)
        print('============================================')
        if bool(folder_contents) == False:
            return None
        '''
        song_list = []
        for file_meta in list_mp3:
            print('==============================================')
            print(file_meta)
            print('============================================')
            if file_meta['mime_type'] == 'audio/mpeg':
                song_list.append(file_meta['path'])
        print('The song_list is')
        print(song_list)
        for song in song_list:
            try:
                entry = self.create_entry_from_track_data(song)
                self.props.base_query_model.add_entry(entry, -1)
            except TypeError:  # Already in db
                pass
        shell.props.db.commit()

        print("end of the line......................")

        print("the songs have been loaded...")

# register the source or it will produce segmentation fault later...
GObject.type_register(DropboxLibrary)
