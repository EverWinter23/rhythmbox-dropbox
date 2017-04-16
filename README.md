# ABOUT

@author frost-forever
This package offers a plugin for the rhythmbox music player to stream music from dropbox using the Dropbox SDK.

# INSTALLATION

1.  Install [dropbox SDK](https://github.com/dropbox/dropbox-sdk-python)
```
    $ pip3 install dropbox
```
    Note:
     * pip3 must be installed algonside python3.5.2 or python3.
     * It will
3. Installing from source.
```
   $ git clone https://github.com/EverWinter23/rhythmbox-dropbox
   $ mkdir ~/.local/share/rhythmbox/plugins
   $ mv rhythmbox-dropbox ~/.local/share/rhythmbox/plugins/
```
 
2. Enable the plugin from rhythmbox plugins menu under the name Dropbox Music.

# RESOLVING ERRORS
1. Run the plugin using the following command
```
   $ rhythmbox -D Dropbox
```
2. See the console for the error and open an issue.

# AUTHORS

*  Rishabh Mehta <eternal.blizzard23@gmail.com>

If you have any questions regarding the plugin, don't hesitate
to create an issue or send me an email.

# LICENSE

[![AGPL](https://img.shields.io/github/license/coala/coala.svg)](https://www.gnu.org/licenses/agpl-3.0.html)

This code falls under the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of
the License, or (at your option) any later version.
