#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  @dev:        https://github.com/flerov/
#  @name:       Instagram All in One Bot
#  @version:    .4
#

from Scripts import mediadownloader, geobot, feedbot, followbytag, autounfollow, followersugests, colors as set
#import InstaAI.main #  not in this version
from InstagramAPI import InstagramAPI
import threading
import datetime
import time
import sys
import os


class Notifications(threading.Thread):
    def __init__(self):
        super().__init__()
    # in progress

    def run(self):
        api.getFollowingRecentActivity()


def options():
    print("\n\033[0;0m(1) Feed-Bot (auto likes and comment feed posts)")
    print("(2) Get-Rid-of-Fakes (auto detects people which do not follow you back)")
    print("(3) Geo-Bot (auto follows people in your area to increase your local influence)")
    print("(4) Tag-Bot (auto follows people by tag)")
    print("(5) Download Profile-Picture (by username)")
    print("(6) Download Post (by username)")
    print("(7) InstAlgorithm-Bot (follow users suggested by Instagram's algorithms")
    #print("(8) InstaAI (auto download high quality posts, upload posts with comments etc.)")

    set.color(set.GREEN)
    print("\nChoose one option by its number!")
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

if len(sys.argv) == 1:
    while True:
        try:
            set.color(set.BLUE)
            username = str(input("Instagram Username: "))
            password = str(input("Instagram Password: "))
            api = InstagramAPI(username, password)
            api.login()
            response = api.LastJson
            if 'invalid' in str(response).lower():
                set.color(set.RED)
                print("\nInvalid Credentials!\n")
            else:
                set.color(set.GREEN)
                print("Valid Credentials!")
                break
        except Exception:
            print(
                "\n\n\033[0;34mRefresh!  -- if you want to exit the script press Ctrl+C\033[0;0m\n")
            set.color(set.RESET)
else:
    username, password = sys.argv[1], sys.argv[2]
    api = InstagramAPI(username, password)
    api.login()


# --------------------
# SESSION
PATH = os.getcwd()
TIME = str(datetime.date.today())

try:
    session_name = username
    os.chdir(PATH + '/Sessions/')
    os.mkdir(session_name)
    os.mkdir(session_name + '/Downloads/')
    os.mkdir(session_name + '/Config/')
    os.mkdir(session_name + '/Config/Log')
    CONFIG_DIR = os.getcwd() + '/' + session_name + '/Config'
    # create .txt files in /Config/
    comment = open(CONFIG_DIR + '/comments.txt', 'x')
    comment.write('\n')
    comment.close()
    blacklist = open(CONFIG_DIR + '/blacklist.txt', 'x')
    blacklist.write('\n')
    blacklist.close()
    whitelist = open(CONFIG_DIR + '/whitelist.txt', 'x')
    whitelist.write('\n')
    whitelist.close()
    LOG_DIR = CONFIG_DIR + '/Log'
    geolog = open(LOG_DIR + '/Auto-Geo-Bot-Log.txt', 'x')
    geolog.write('\n')
    geolog.close()
    taglog = open(LOG_DIR + '/Auto-Tag-Bot-Log.txt', 'x')
    taglog.write('\n')
    taglog.close()
    feedlog = open(LOG_DIR + '/Feed-Bot-Log.txt', 'x')
    feedlog.write('\n')
    feedlog.close()

    string = "\n\033[0;34m[Session]\033[0;0m: \033[0;32m{} created\n".format(username)
    sys.stdout.write(str(string))
    time.sleep(1.5)
except FileExistsError:
    string = "\n\033[0;34m[Session]\033[0;0m \033[0;32m{}\033[0;0m loaded\n".format(username)
    sys.stdout.write(str(string))
    time.sleep(1.5)

comments = []
blacklist = []
whitelist = []

SESSION_DIR = PATH + '/Sessions/' + session_name + '/'
os.chdir(PATH)
with open(SESSION_DIR + 'Config/comments.txt', 'r') as c, open(SESSION_DIR + 'Config/blacklist.txt', 'r') as b, open(SESSION_DIR + 'Config/whitelist.txt', 'r') as w:
    _c, _b, _w = c.readlines(), b.readlines(), w.readlines()
    for i in _c:
        comments.append(i.strip('\n'))
    for i in _b:
        blacklist.append(i.strip('\n'))
    for i in _w:
        whitelist.append(i.strip('\n'))
# --------------------

while True:
    try:
        set.color(set.RESET)
        choice = options()
        if choice == 0:
            #bot()
            continue
        elif choice == 1:
            feedbot.autoprogressfeed(api, SESSION_DIR, comments, blacklist)
        elif choice == 2:
            autounfollow.getridoffakes(api, whitelist)
        elif choice == 3:
            geobot.geoBot(api, SESSION_DIR, blacklist, comments)
            print("\nRunning auto-unfollow!")
            autounfollow.getridoffakes(api, whitelist)
        elif choice == 4:
            tag, n, follow, comment, minlikes = followbytag.init()
            followbytag.bot(api, SESSION_DIR, follow, comments, blacklist, tag, n, comment, minlikes)
        elif choice == 5:
            mediadownloader.pbdownloader(api, SESSION_DIR)
        elif choice == 6:
            mediadownloader.postdownloader(api, SESSION_DIR)
        elif choice == 7:
            followersugests.followers_algorithm(api)
        #elif choice == 8:
        #    InstaAI.main.run(api)
    except KeyboardInterrupt:
        set.color(set.RESET)
        print("\nExit script: [Enter]; Exit module: [input]")
        if not input("?> "):
            sys.exit(0)
