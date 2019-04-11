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


def decode_rot_5(string):
    _maxid = ''
    _range = '0123456789'
    for n in string:
        try:
            int(n)
            _pos = _range.find(n)
            _maxid += (_range[5:] + _range[:5])[_pos]
        except ValueError:
            pass
    return _maxid


def autoprogressfeed(api: InstagramAPI, comments, blacklist, maxid=''):
    set.color(set.RED)
    print("\n-------------------------\n"
          "Sleeping 40sec between every interaction! (ban-protection)\n"
          "-------------------------\n")
    log_blacklist = []
    with open('Configs/Logs/Feed-Bot-Log.txt', 'r') as log:
        for i in log.readlines():
            log_blacklist.append(i.strip('\n'))
    api.SendRequest(
        'feed/timeline/?max_id=' + str(maxid) + '&?rank_token=' + str(api.rank_token) + '&ranked_content=true&')
    data = api.LastJson
    set.color(set.BLUE)
    print("------------------\n"
          "Data fetched"
          "\n------------------\n")
    for i in data['items']:
        try:
            set.color(set.BLUE)
            if 'injected' in i:
                if i['injected']['label'] == 'Sponsored':
                    print("\n------------------\n"
                          "Skipping advertisment"
                          "\n------------------\n")
                    continue
            print("------------------\n"
                  "Post by: [{}]".format(i['user']['username']))
            try:
                if i['video_versions']:
                    print("Video Information:")
                    print("View count: [{}]".format(i['view_count']))
            except KeyError:
                print("Picture Information:")
            if i['caption']['text'] is not None:
                print("Caption: [{}]".format(i['caption']['text']))
            print("Taken at: [{0}]\n"
                  "Photo of you: [{1}]\n"
                  "Like count: [{2}]\n"
                  "Comment count: [{3}]\n".format(unixtodate(i['taken_at']),
                                                  i['photo_of_you'],
                                                  i['like_count'],
                                                  i['comment_count']))
            if i['user']['username'] not in blacklist and str(i['caption']['media_id']) not in log_blacklist:
                with open('Configs/Logs/Feed-Bot-Log.txt', 'a') as log:
                    log.write(str(i['caption']['media_id']) + '\n')
                    api.like(i['caption']['media_id'])
                    comment = str(random.choice(comments))
                    api.comment(i['caption']['media_id'], comment)
                    set.color(set.GREEN)
                    print("Comment on post: [{}]".format(comment))
                    print("Post liked")
                    print("------------------\n")
                    time.sleep(t)
        except KeyError:
            set.color(set.RED)
            print("------------------\n"
                  "Can't handle data. Invalid! Skipping post...\n"
                  "------------------\n")
            time.sleep(1)
        except FileNotFoundError:
            set.color(set.RED)
            print("File 'Feed-Bot-Log.txt' not found in 'Configs//Logs/'!")
        except Exception as e:
            set.color(set.RED)
            print("An error occured! [ERROR]:", e)
            print("Skipping User!")
            time.sleep(1)
    if data['more_available']:
        set.color(set.GREEN)
        print("\n------------------\n"
              "More posts available! Loading..."
              "\n------------------\n")
        nextmaxid = decode_rot_5(data['next_max_id'])
        time.sleep(5)
        autoprogressfeed(api, comments, blacklist, nextmaxid)
    elif not data['more_available']:
        set.color(set.RED)
        print("------------------\n"
              "Empty feed! Try one of my algorithms to follow people!\n"
              "------------------")

