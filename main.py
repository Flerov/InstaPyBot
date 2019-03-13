#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  @dev:        https://github.com/flerov/
#  @name:       Instagram All in One Bot
#  @version:    .4
#

from InstagramAPI import InstagramAPI
from Scripts import mediadownloader, geobot, feedbot, followbytag, autounfollow, colors as set
import time
import sys
import os


comments = []
blacklist = []
whitelist = []

def options():
    print("\n(1) Feed-Bot (auto likes and comment feed posts)")
    print("(2) Get-Rid-of-Fakes (auto detects people which do not follow you back)")
    print("(3) Geo-Bot (auto follows people in your area to increase your local influence)")
    print("(4) Tag-Bot (auto follows people by tag)")
    print("(5) Download Profile-Picture (by username)")
    print("(6) Download Post (by username)")
    print("(0) Automatisch")

    set.color(set.GREEN)
    print("Choose one option by its number!")
    try:
        set.color(set.BLUE)
        choice = int(input("Choice >  "))
        return choice
    except ValueError:
        set.color(set.RED)
        print("Invalid argument!")
        time.sleep(1.5)
        options()


print("""
#############################################
#  @dev:        https://github.com/flerov/  #
#  @name:       Instagram All in One Bot    #
#  @version:    .4                          #
#############################################
\n\n
""")

print("Checking files...")

for i in ['comments.txt', 'blacklist.txt', 'whitelist.txt', 'Logs/Auto-Geo-Bot-Log.txt',
          'Logs/Auto-Tag-Bot-Log.txt', 'Logs/Feed-Bot-Log.txt']:
    if not os.path.isfile('Configs/'+i):
        print("File", i, "is missing in /Configs/")
        sys.exit(0)

print("All files found\n")

with open('Configs/comments.txt', 'r') as c, open('Configs/blacklist.txt', 'r') as b, open('Configs/whitelist.txt', 'r') as w:
    _c, _b, _w = c.readlines(), b.readlines(), w.readlines()
    for i in _c:
        comments.append(i.strip('\n'))
    for i in _b:
        blacklist.append(i.strip('\n'))
    for i in _w:
        whitelist.append(i.strip('\n'))

try:
    while True:
        set.color(set.BLUE)
        username = str(input("Instagram Username: "))
        password = str(input("Instagram Password: "))
        api = InstagramAPI(username, password)
        api.login()
        response = api.LastJson
        if 'invalid_credentials' in response:
            set.color(set.RED)
            print("\nInvalid Credentials!\n")
        else:
            set.color(set.GREEN)
            print("Valid Credentials!")
            break
except KeyboardInterrupt:
    set.color(set.BLUE)
    print("Refresh!  -- if you want to exit the script at this point you have to close your shell")

while True:
    try:
        set.color(set.RESET)
        choice = options()
        if choice == 0:
            #bot()
            continue
        elif choice == 1:
            feedbot.autoprogressfeed(api, comments, blacklist)
        elif choice == 2:
            autounfollow.getridoffakes(api, whitelist)
        elif choice == 3:
            geobot.geoBot(api, blacklist, comments)
        elif choice == 4:
            tag, n, comment, minlikes = followbytag.init()
            followbytag.bot(api, comments, blacklist, tag, n, comment, minlikes)
        elif choice == 5:
            mediadownloader.pbdownloader(api)
        elif choice == 6:
            mediadownloader.postdownloader(api)
    except KeyboardInterrupt:
        set.color(set.RESET)
        print("\nExit script: [Enter]; Exit module: [input]")
        if not input("?> "):
            sys.exit(0)
