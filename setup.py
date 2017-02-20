# -*- coding: utf-8 -*-
'''
hostswitcher for linux
'''

from setuptools import setup

setup(
    name = "hostswitcher",
    version = "0.0.1",
    author = "fiefdx",
    author_email = "fiefdx@163.com",
    packages = ['hostswitcher'],
    entry_points={
        'gui_scripts': ['hostswitcher = hostswitcher.hostswitcher:main']
    },
    data_files = [('/usr/share/icons/hicolor/128x128/apps', ['switch-icon.png'])],
    install_package_data = True
)
