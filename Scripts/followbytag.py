#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from InstagramAPI import InstagramAPI
from Scripts import colors as set
import datetime
import random
import time


t = 40  # timer


def unixtodate(unixid):
    return datetime.datetime.fromtimestamp(int(unixid)).strftime('%Y-%m-%d %H:%M:%S')


def init():
    set.color(set.RED)
    print(
        "\n-------------------------\n"
        "Sleeping 40sec between every interaction! (ban-protection)\n"
        "-------------------------\n")
    set.color(set.BLUE)
    print("Tag")
    set.color(set.GREEN)
    tag = str(input("[Tag]: "))
    set.color(set.BLUE)
    print("How many people to follow ?")
    set.color(set.GREEN)
    n = int(input("[Follow]: "))
    set.color(set.BLUE)
    print("Comment on pictures ?([Enter]=No / [y/Y]=Yes)")
    try:
        set.color(set.GREEN)
        comment = bool(input("[Comment]: "))
    except ValueError:
        comment = False
    set.color(set.BLUE)
    print("Minimum number of likes a photo needs to follow the person: (Enter=no min)")
    try:
        set.color(set.GREEN)
        minlikes = int(input("[Min]: "))
    except ValueError:
        minlikes = 0
    return tag, n, comment, minlikes


def bot(api: InstagramAPI, comments, blacklist, tag, n, comment, minlikes):
    log_blacklist, log2_blacklist = [], []
    with open('Configs/Logs/Auto-Tag-Bot-Log.txt', 'r') as log, open('Configs/Logs/Feed-Bot-Log.txt', 'r') as log2:
        for i in log.readlines():
            log_blacklist.append(i.strip('\n'))
        for i in log2.readlines():
            log2_blacklist.append(i.strip('\n'))
    maxid = ''
    items = {}
    set.color(set.RESET)
    print("------------------\nLoading [{}] posts. This could take a while...\n"
          "------------------".format(n))
    k = 0
    try:
        while n > len(items):
            api.getHashtagFeed(tag, maxid)
            feedresponse = api.LastJson
            maxid = feedresponse['next_max_id']
            for i in range(0, len(feedresponse['items'])):
                if feedresponse['items'][i]['like_count'] >= minlikes \
                        and feedresponse['items'][i]['user']['username'] not in blacklist \
                        and feedresponse['items'][i]['user']['username'] not in log_blacklist:
                    items[k] = feedresponse['items'][i]
                    k += 1
                    if k % 10 == 0:
                        set.color(set.GREEN)
                        print("[{}/{}] posts found".format(len(items), n))
    except KeyboardInterrupt:
        set.color(set.RED)
        print("Break!")
        set.color(set.GREEN)
        print("[{}/{}] posts found".format(len(items), n))
    set.color(set.BLUE)
    for i in range(0, n):
        try:
            user = items[i]['user']
            if 'injected' in items[i]:
                if items[i]['injected']['label'] == 'Sponsored':
                    set.color(set.RED)
                    print("------------------\nSkipping advertisment")
                    continue
            set.color(set.GREEN)
            print("------------------\nPost by: [{}]".format(user['username']))
            if 'video_versions' in items[i]:
                set.color(set.BLUE)
                print("Video Information:")
                print("View count: [{}]".format(items[i]['view_count']))
            else:
                set.color(set.BLUE)
                print("Picture Information:")
            if items[i]['caption']['text'] is not None:
                print("Caption: [{}]".format(items[i]['caption']['text']))
            print("Taken at: [{0}]\n"
                  "Photo of you: [{1}]\n"
                  "Like count: [{2}]\n"
                  "Comment count: [{3}]".format(unixtodate(items[i]['taken_at']),
                                                  items[i]['photo_of_you'],
                                                  items[i]['like_count'],
                                                  items[i]['comment_count']))
            with open('Configs/Logs/Auto-Tag-Bot-Log.txt', 'a') as log, open('Configs/Logs/Feed-Bot-Log.txt', 'a') as log2:
                log.write(str(user['username'] + '\n'))
                log2.write(str(items[i]['caption']['media_id']) + '\n')
                api.like(items[i]['caption']['media_id'])
                api.follow(items[i]['user']['pk'])
                set.color(set.GREEN)
                if comment:
                    cmt = str(random.choice(comments))
                    api.comment(items[i]['caption']['media_id'], cmt)
                    print("!Comment on post: [{}]".format(cmt))
                print("!Post liked")
                print("!User followed")
                time.sleep(t)
        except KeyError as e:
            set.color(set.RED)
            print("------------------\nCan't handle data. Invalid! Skipping post...\n------------------")
            time.sleep(1)
        except FileNotFoundError:
            set.color(set.RED)
            print("File 'Auto-Tag-Bot-Log.txt' and 'Feed-Bot-Log.txt' not found in '/Logs/'!")
            return
        except Exception as e:
            set.color(set.RED)
            print("An error occured! [ERROR]:", e)
            print("Skipping User!")
            time.sleep(1)

            # follow fehlt + bug in schleife bei invalid data
