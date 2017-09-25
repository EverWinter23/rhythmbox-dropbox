'''
5th march 2017 sunday
file=plugin.py       lang=python3.5.2
'''
# imports
import rb
from gi.repository import GObject, Peas, RB, Gio, Gtk
import dropbox
from source import DropboxSource
from lib import DropboxLibrary


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

# register the source or it will produce segmentation fault later...
GObject.type_register(DropboxLibrary)
