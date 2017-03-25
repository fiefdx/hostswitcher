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

# it use gedit as default editor, if you don't like it, you can change the hostswitcher file 'Editor = "gedit"' to any other editor easily
```
