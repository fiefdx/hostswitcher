# hostswitcher

a GUI tool for linux to switch hosts configurations for different develop environments quickly

![Alt text](/doc/hostswitcher.png?raw=true "hostswitcher")

# Install & Run

```bash
# install wx
sudo apt-get install python-wxgtk3.0 python-wxtools wx3.0-i18n libwxgtk3.0-dev

# install
git clone git@github.com:fiefdx/hostswitcher.git
cd hostswitcher
sudo python ./setup.py install

# run
sudo hostswitcher
# it will create a directory /etc/hostswitcher and copy your default hosts file /etc/hosts into it as /etc/hostswitcher/default

# click "Add" button, then enter <file name>, it will create a new hosts file in /etc/hostswitcher/<file name> base on default file, and you can edit this file properly
# select a hosts file from the drop down menu, then click "Edit", then you can edit this selected hosts file
# select a hosts file from the drop down menu, then click "Delete", then you can delete this selected hosts file
# select a hosts file from the drop down menu, then click "Set", then you can set this selected hosts file as current hosts file
# the status bar always display currently used hosts file name, so you can easily tell which hosts file is currently used

# it use gedit as default editor, if you don't like it, you can change the hostswitcher file 'Editor = "gedit"' to any other editor easily
```
