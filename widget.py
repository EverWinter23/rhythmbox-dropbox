'''
8th march 2017 wednesday
file=widget.py      lan=python3.5.2
'''

# imports
from gi.repository import Gtk

'''
about
    creates an authorization dialog in which ouath2 code
    is entered...
'''
class OAuthDialog(Gtk.Dialog):
    '''
    attributes
        oauth2
         password field for storing oauth2 code
    '''
    oauth2 = None

    def __init__(self):
        Gtk.Dialog.__init__(self,
                   _('Authentication'), None, 0, (
                    Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                    Gtk.STOCK_OK, Gtk.ResponseType.OK,
        ))

        thebox = Gtk.VBox()
        message = "Authentication required for accessing Dropbox"
        label = Gtk.Label(_(message))
        thebox.add(label)


        oauth2_box = Gtk.HBox()
        oauth2_label = Gtk.Label(_("Oauth2"))
        self.oauth2 = Gtk.Entry()
        self.oauth2.set_visibility(False)

        oauth2_box.add(oauth2_label)
        oauth2_box.add(self.oauth2)

        thebox.add(oauth2_box)

        box = self.get_content_area()
        box.add(thebox)
        # width, height
        # box.set_size_request(300, 100)
        self.show_all()
