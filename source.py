'''
5th match 2017 sunday
file=source.py     lang=python3.5.2
'''

from gi.repository import RB
from gi.repository import GLib, Gtk
from con.dropcon import DropCon
from entry import DropboxEntryType
from widget import OAuthDialog

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
    infobar
     for requesting dropbox authorization
'''
class DropboxSource(RB.Source):
    dropcon = DropCon()
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
        # I prefer track_number, title and duration
        #self.songs_view.append_column(RB.EntryViewColumn.PLAY_COUNT, True,)
        self.songs_view.append_column(RB.EntryViewColumn.TITLE, True,)
        self.songs_view.append_column(RB.EntryViewColumn.TRACK_NUMBER, True)
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

        if self.dropcon.client == None:
            self.infobar = Gtk.InfoBar()
            self.top_box.pack_start(self.infobar, True, True, 0)
            self.infobar.set_message_type(Gtk.MessageType.INFO)
            # add a login button
            auth_btn = self.infobar.add_button(_("Login"), 1)
            auth_btn.connect('clicked', self.auth)
            # the label for authorization
            label = Gtk.Label(_("Requires authorization for accessing Dropbox..."))
            self.infobar.get_content_area().add(label)
        else:
            self.top_box.remove(self.infobar)

        self.dropbox_entry = DropboxEntryType(self.dropcon)
        self.browser = RB.LibraryBrowser.new(shell.props.db, self.dropbox_entry)
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
        #self.top_box.pack_start(self.browser, True, True, 0)m
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
            RB.RhythmDBPropType.GENRE, 'dropbox-music',  # shit didn't add GENRE!
        )
        db.do_full_query_parsed(query_model, query)
        self.browser.set_model(query_model, False)
        self.update_view()

    def update_view(self, *args):
        self.songs_view.set_model(self.browser.props.output_model)
        self.props.query_model = self.browser.props.output_model

    def init_authenticated(self):
        print("authenticating...")

        if self.dropcon.client != None:
            print("removing the information bar...")
            self.top_box.remove(self.infobar)
        self.load_songs()

    def auth(self, widget):
    #def auth(self):
        '''this part only works for me'''
        '''
        access_token = APP_TOKEN
        print("connecting to dropbox...")

        # make a dropbox connection
        self.dropcon = DropCon(access_token)

        if self.dropcon != None:
            print('connected.............')
            self.init_authenticated()
        '''

        '''
        if self.dropcon != None:
            print('connected.............')
            self.init_authenticated()
        '''

        self.dropcon.authenticate()
        dialog = OAuthDialog()
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            auth_code = dialog.oauth2.get_text()
            print("connecting to dropbox...")
            self.dropcon.connect(auth_code)

        if self.dropcon.client != None:
            dialog.destroy()
            print('connected.............')
            self.init_authenticated()


    def do_impl_get_entry_view(self):
        return self.songs_view

    def create_entry_from_track_data(self, sound):
        shell = self.props.shell
        db = shell.props.db

        print('creating entry for path', sound['path'])
        print("path printed")

        # avoid segmentation fault
        # entry type must remain same
        self.dropbox_entry.client = self.dropcon.client
        entry = RB.RhythmDBEntry.new(db, self.dropbox_entry, sound['path'])

        print(sound['name'])

        db.entry_set(entry, RB.RhythmDBPropType.TITLE, sound['name'])
        db.entry_set(entry, RB.RhythmDBPropType.TRACK_NUMBER, int(sound['trackNumber']))
        # for all entries -- commong genre
        db.entry_set(entry, RB.RhythmDBPropType.GENRE, 'dropbox-music')
        # for searching -- got it working on 16th march 2017
        db.entry_set(entry, RB.RhythmDBPropType.COMMENT, sound['name'].lower())
        print('done............')
        return entry

    def load_songs(self):
        raise NotImplementedError
