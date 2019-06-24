#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from InstagramAPI import InstagramAPI
from Scripts import colors as set
import time
import sys


t = 5  # timer


def getridoffakes(api: InstagramAPI, whitelist):
    try:
        set.color(set.RED)
        print("\n-------------------------\n"
              "Sleeping 5sec between every interaction! (ban-protection)\n"
              "-------------------------\n")
        api.getUserFollowings(api.username_id)
        follower = api.LastJson['users']
        _list = []
        set.color(set.GREEN)
        for i in follower:
            api.userFriendship(i['pk'])
            _ = api.LastJson
            print('-------------------------\n')
            if _['followed_by']:
                print("[User]: {0} follows you\n"
                      "-------------------------\n".format(i['username']))
            elif not _['followed_by']:
                sys.stdout.write("\033[0;31m[User]: %s doesn't follow you " % i['username'])
                if i['username'] not in whitelist:
                    api.unfollow(i['pk'])
                    sys.stdout.write("unfollowed!\n\033[0;32m")
                    print("-------------------------\n")
                    _list.append(None)
                    time.sleep(t)
                else:
                    set.color(set.BLUE)
                    sys.stdout.write("\033[0;34m[User]: %s found in whitelist! Skipping unfollow\n\033[0;32m" % i['username'])
                    print('-------------------------\n')
    finally:
        sys.stdout.write("\n\033[0;43mUnfollowed: %s fake friends\033[0;0m" % len(_list))
