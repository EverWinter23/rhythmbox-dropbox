'''
5th match 2017 sunday
file=source.py     lang=python3.5.2
'''

from gi.repository import RB
from gi.repository import Gtk
from entry import DropboxEntryType

gentry = DropboxEntryType(None)
class DropboxSource(RB.Source):
    def setup(self):
        shell = self.props.shell        # RB.Source.props.shell
        self.songs_view = RB.EntryView.new(
            db = shell.props.db,
            shell_player = shell.props.shell_player,
            is_drag_source=True,
            is_drag_dest=False,
        )

        self.songs_view.append_column(
            RB.EntryViewColumn.TRACK_NUMBER, True,
        )
        self.songs_view.append_column(
            RB.EntryViewColumn.TITLE, True,
        )
        self.songs_view.append_column(
            RB.EntryViewColumn.DURATION, True,
        )
        self.songs_view.connect('notify::sort-order',
            lambda *args, **kwargs: self.songs_view.resort_model(),
        )
        self.songs_view.connect('entry-activated',
            lambda view, entry: shell.props.shell_player.play_entry(entry, self),
        )

        self.vbox = Gtk.Paned.new(Gtk.Orientation.VERTICAL)
        self.top_box = Gtk.VBox()

        '''
        if dbx != None:
            print('done...........................')
            self.init_authenticated()
            print('killing box')
        '''
        if 1 == 1:
            infobar = Gtk.InfoBar()
            self.top_box.pack_start(infobar, True, True, 0)
            infobar.set_message_type(Gtk.MessageType.INFO)
            auth_btn = infobar.add_button(_("Login"), 1)
            auth_btn.connect('clicked', self.auth)
            label = Gtk.Label(_("Requires authorization for accessing Dropbox..."))
            infobar.get_content_area().add(label)

        self.browser = RB.LibraryBrowser.new(shell.props.db, gentry)
        self.browser.set_model(self.props.base_query_model, False)
        self.browser.connect("notify::output-model", self.update_view)
        self.browser.set_size_request(-1, 200)

        self.search_widget = RB.SearchEntry.new(False)
        self.search_widget.connect("search", self.on_search)

        # sets the position for the search box...
        # gkt.Alignment(xalign, yalign, xscale, yscale)
        # argumetns are floating point numbers from 0.0 to 1.0
        search_box = Gtk.Alignment.new(0.99, 0, 0.1, 1)
        search_box.add(self.search_widget)

        self.top_box.pack_start(search_box, False, False, 5)
        #self.top_box.pack_start(self.browser, True, True, 0)

        self.update_view()

        self.vbox.add1(self.top_box)
        self.vbox.add2(self.songs_view)
        self.pack_start(self.vbox, True, True, 0)
        print('ending source setup.....')
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
            RB.RhythmDBPropType.GENRE, 'google-play-music',  # shit!
        )
        db.do_full_query_parsed(query_model, query)
        self.browser.set_model(query_model, False)
        self.update_view()

    def update_view(self, *args):
        self.songs_view.set_model(self.browser.props.output_model)
        self.props.query_model = self.browser.props.output_model

    def init_authenticated(self):
        print('authenticating..............')
        if hasattr(self, 'auth_box'):
            print('removing top box')
            self.top_box.remove(self.auth_box)
        self.load_songs()


    def auth(self, widget):
        print('connecting')
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
        global dbx
        shell = self.props.shell
        db = shell.props.db

        print('creating entry for path', path)

        #tag = stagger.read_tag(path)
        #print(tag.title)

        entry = RB.RhythmDBEntry.new(
            db, gentry, path,
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

    def load_songs():
        raise NotImplementedError
