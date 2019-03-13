#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from InstagramAPI import InstagramAPI
from Scripts import colors as set
import datetime
import random
import time


def unixtodate(unixid):
    return datetime.datetime.fromtimestamp(int(unixid)).strftime('%Y-%m-%d %H:%M:%S')

def getLocationFeed(api: InstagramAPI, locid, maxid=''):
    api.getLocationFeed(locid, maxid)
    return api.LastJson


def geoBot(api: InstagramAPI, blacklist, comments):
    log_blacklist, log2_blacklist = [], []
    with open('Configs/Logs/Auto-Tag-Bot-Log.txt', 'r') as log, open('Configs/Logs/Feed-Bot-Log.txt', 'r') as log2:
        for i in log.readlines():
            log_blacklist.append(i.strip('\n'))
        for i in log2.readlines():
            log2_blacklist.append(i.strip('\n'))
    set.color(set.RED)
    print("\n-------------------------\n"
          "Sleeping 40sec between every interaction! (ban-protection)\n"
          "-------------------------\n")
    set.color(set.BLUE)
    print("City coordinates: ")
    lat, lng = float(input("[Latitude]: ")), float(input("[Longitude]: "))
    query = "location_search?latitude={lat}&longitude={lng}&rank_token={token}".format(
        lat=str(lat),
        lng=str(lng),
        token=api.rank_token
    )
    api.SendRequest(query)
    locresponse = api.LastJson['venues']

    set.color(set.BLUE)
    print("Locations found: ")
    locs = []
    for i in locresponse:
        locs.append(i['name'])

    while True:
        set.color(set.BLUE)
        for i in range(0, len(locs)):
            print("[{0}. {1}]".format(i, locs[i]))
        print("Choose a location by its number:")
        set.color(set.GREEN)
        loc = int(input("[Location]: "))
        externalid = locresponse[loc]['external_id']
        locfeedresponse = getLocationFeed(api, externalid)  # location_feed
        if locfeedresponse['num_results'] == 0:
            locs.remove(locs[loc])
            locresponse.remove(locresponse[loc])
            set.color(set.RED)
            print("Invalid address. Servers didn't respond!")
            time.sleep(1.5)
            continue
        else:
            break

    set.color(set.BLUE)
    print("How many people to follow?:")
    set.color(set.GREEN)
    follow = int(input("[Follow]: "))
    set.color(set.BLUE)
    print("Comment on pictures? (No=[ENTER] / Yes=[y/Y]):")
    set.color(set.GREEN)
    try:
        comment = bool(input("[Comment]: "))
    except ValueError:
        comment = False
    set.color(set.BLUE)
    print("Minimum number of likes a photo needs to follow the person (Enter=no min):")
    set.color(set.GREEN)
    try:
        minlikes = int(input("[Min]: "))
    except ValueError:
        minlikes = 0

    items = {}
    k = 0
    items[k] = locfeedresponse['items']
    k += 1
    set.color(set.RESET)
    print("------------------\nLoading [{}] posts. This could take a while...\n"
          "------------------".format(follow))
    try:
        while follow > len(items):
            for i in range(0, locfeedresponse['num_results']):
                username = locfeedresponse['items'][i]['user']['username']
                if locfeedresponse['items'][i]['like_count'] >= minlikes \
                        and username not in blacklist \
                        and username not in log_blacklist:
                    items[k] = locfeedresponse['items'][i]
                    k += 1
                    if k % 10 == 0:
                        set.color(set.GREEN)
                        print("[{}/{}] posts found".format(len(items), follow))
            maxid = locfeedresponse['next_max_id']
            locfeedresponse = getLocationFeed(api, externalid, maxid)
    except KeyboardInterrupt:
        set.color(set.RED)
        print("Break!")
        set.color(set.GREEN)
        print("[{}/{}] posts found".format(len(items), follow))
    except KeyError:
        set.color(set.RED)
        print("Bad Location. Only found [{}] posts.".format(len(items)))
        time.sleep(2)

    for i in range(0, follow):
        try:
            set.color(set.BLUE)
            user = items[i]['user']
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
                time.sleep(40)
        except KeyError:
            set.color(set.RED)
            print("------------------\nCan't handle data. Invalid! Skipping post...\n------------------")
            time.sleep(1)
        except FileNotFoundError:
            set.color(set.RED)
            print("File 'Auto-Tag-Bot-Log.txt' and 'Feed-Bot-Log.txt' not found in 'Configs//Logs/'!")
            return
        except Exception as e:
            set.color(set.RED)
            print("An error occured! [ERROR]:", e)
            print("Skipping User!")
            time.sleep(1)
