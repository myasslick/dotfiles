#!/usr/bin/env python

import argparse
import getpass
import os
import sys

try:
    from urllib.request import urlretrieve
except ImportError:
    from urllib import urlretrieve

COMMON_FILES = [
    ".gitconfig",
    ".hgrc",
    ".pythonrc",
    ".vimrc"
]

MAC_FILES = [
    (".bash_profile.mac", ".bash_profile"),
]

LINUX_FILES = [
    (".bash_profile", ".bash_aliases"),
]

URL = "https://raw.githubusercontent.com/yeukhon/dotfiles/master/"

def file_maps(files):
    maps = {}
    home_dir = os.path.expanduser("~")
    for f in files:
        if isinstance(f, tuple):
            _url = URL + f[0]
            maps[_url] = os.path.join(home_dir, f[1])
        else:
            _url = URL + f
            maps[_url] = os.path.join(home_dir, f)
    return maps

def download_files(files):
    for link, fpath in files.items():
        print("Downloading {}".format(link.split("/")[-1]))
        local_path, headers = urlretrieve(link, filename=fpath)

def retrieve(is_mac=False, is_linux=False):
    if is_mac:
        files = file_maps(MAC_FILES + COMMON_FILES)
    elif is_linux:
        files = file_maps(LINUX_FILES + COMMON_FILES)

    download_files(files)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Install dotfiles")
    parser.add_argument("--mac", action="store_true",
                       help="Install dotfiles on Mac.")
    parser.add_argument("--linux", action="store_true",
                       help="Install dotfiles on Linux.")

    if len(sys.argv) == 1:
        parser.print_help()
    else:
        args = parser.parse_args()
        if args.mac:
            retrieve(is_mac=True)
        elif args.linux:
            retrieve(is_linux=True)
        else:
            sys.exit("Meh I don't get it. RTFM")
