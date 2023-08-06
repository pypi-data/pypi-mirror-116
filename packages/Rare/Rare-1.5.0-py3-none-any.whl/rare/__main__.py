#!/usr/bin/python

import os
import platform
from argparse import ArgumentParser

from rare import __version__
from rare.utils import singleton, utils


def main():
    parser = ArgumentParser()
    parser.add_argument("-V", "--version", action="store_true", help="Shows version and exits")
    parser.add_argument("-S", "--silent", action="store_true",
                        help="Launch Rare in background. Open it from System Tray Icon")
    parser.add_argument("--offline", action="store_true", help="Launch Rare in offline mode")
    if platform.system() != "Windows":
        parser.add_argument("--disable-protondb", action="store_true", dest="disable_protondb",
                            help="Do not download and check data from ProtonDB. Disable it, if you don't need grades")
        parser.add_argument("--enable-protondb", action="store_true", dest="enable_protondb",
                            help="Enable ProtonDB data, after disabled")

    parser.add_argument("--desktop-shortcut", action="store_true", dest="desktop_shortcut",
                        help="Use this, if there is no link on desktop to start Rare")
    parser.add_argument("--startmenu-shortcut", action="store_true", dest="startmenu_shortcut",
                        help="Use this, if there is no link in start menu to launch Rare")
    subparsers = parser.add_subparsers(title="Commands", dest="subparser")

    launch_parser = subparsers.add_parser("launch")
    launch_parser.add_argument('app_name', help='Name of the app', metavar='<App Name>')

    args = parser.parse_args()

    if args.desktop_shortcut:
        utils.create_rare_desktop_link("desktop")
        print("Link created")
    if args.startmenu_shortcut:
        utils.create_rare_desktop_link("start_menu")
        print("link created")

    if args.version:
        print(__version__)
        exit(0)
    try:
        # this object only allows one instance pre machine
        me = singleton.SingleInstance()
    except singleton.SingleInstanceException:
        print("Rare is already running")

        with open(os.path.expanduser("~/.cache/rare/lockfile"), "w") as file:
            if args.subparser == "launch":
                file.write("launch " + args.app_name)
            else:
                file.write("start")
            file.close()

        exit(0)

    if args.subparser == "launch":
        args.silent = True

    from rare.app import start
    start(args)


if __name__ == '__main__':
    main()
