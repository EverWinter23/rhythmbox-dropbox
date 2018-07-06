# ABOUT

Dropbox plugin for the rhythmbox music player to stream music from dropbox  account. No
need to download the files to your PC, streams the music directly. So, if you have a huge
music collection, this plugin is perfect for you.

This plugin does not store your access token for security reasons and privacy concerns,
so you will have to authorize the plugin every time.

# INSTALLATION

+ Install [dropbox SDK](https://github.com/dropbox/dropbox-sdk-python). pip3 must be 
  installed alongside python3.5.2 or python3.
    ```
    $ pip3 install dropbox
    ```

+ Installing from source.
    ```
    $ mkdir -p ~/.local/share/rhythmbox/plugins
    $ git clone https://github.com/EverWinter23/rhythmbox
    ```
+ Move the dir **rhythmbox-dropbox** to **~/.local/share/rhythmbox/plugins**.

+ After this, just enable the plugin for rhythmbox. It will be listed as **Dropbox
  Music**.
 
# SCREENSHOT
![Rhymbox Dropbox](/screenshots/rhythm.png?raw=true "Not Much...")

# RESOLVING ERRORS
+ Run the plugin using the following command
    ```
   $ rhythmbox -D Dropbox
    ```
+ See the console for the error and open an issue.

# AUTHOR

*  Rishabh Mehta <eternal.blizzard23@gmail.com>

If you have any questions regarding the plugin, don't hesitate
to create an issue or send me an email.


# LICENSE [![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

Permissions of this strongest copyleft license are conditioned on making available complete
source code of licensed works and modifications, which include larger works using a
licensed work, under the same license. Copyright and license notices must be preserved.
Contributors provide an express grant of patent rights. When a modified version is used to
provide a service over a network, the complete source code of the modified version must be
made available.