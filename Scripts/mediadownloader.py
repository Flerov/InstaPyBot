#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from InstagramAPI import InstagramAPI
from Scripts import colors as set
import datetime
import urllib
import time
import sys


def unixtodate(unixid):
    return datetime.datetime.fromtimestamp(int(unixid)).strftime('%Y-%m-%d %H:%M:%S')


def pbdownloader(api: InstagramAPI, PATH):
    set.color(set.BLUE)
    username = str(input("Username: "))
    if api.searchUsername(username):
        data = api.LastJson['user']
        url = str(data['hd_profile_pic_url_info']['url'])
        urllib.request.urlretrieve(url, PATH + 'Downloads/' + username + '.jpg')
        set.color(set.GREEN)
        print("\n-------------------\n"
              "Profile Picture added to /Downloads/\n"
              "-------------------")
        time.sleep(1.5)
        return True
    else:
        return False


def postdownloader(api: InstagramAPI, PATH):
    set.color(set.BLUE)
    username = str(input("Username: "))
    api.searchUsername(username)
    if 'fail' in api.LastJson['status']:
        return False
    pk = api.LastJson['user']['pk']
    maxid = ''
    while True:
        api.getUserFeed(pk, maxid)
        feed = api.LastJson
        if 'fail' in feed['status']:
            return False
        for i in range(0, len(feed['items'])-1):
            set.color(set.BLUE)
            sys.stdout.write("\033[0;32mMedia number: [{0}] \033[0;34m| Taken at: [{1}] | Like count: [{2}]\n".format(i,
                                                                                                         unixtodate(
                                                                                                             feed['items'][i]['taken_at']),
                                                                                                         feed['items'][i]['like_count']))
            if feed['items'][i]['caption'] is not None:
                print("Caption: [{}]".format(feed['items'][i]['caption']['text']))
            else:
                print("No caption available")
            mediatype = feed['items'][i]['media_type']
            if mediatype == 1:
                #print("Media type: [Single Picture]\n-------------------------")
                sys.stdout.write("\033[0;32mMedia type: [Single Picture]\n\033[0;34m-------------------------\n")
            elif mediatype == 2:
                #print("Media type: [Video]\n-------------------------")
                sys.stdout.write("\033[0;32mMedia type: [Video]\n\033[0;34m-------------------------\n")
            elif mediatype == 8:
                numpics = len(feed['items'][i]['carousel_media'])
                #print("Media type: [{} Pictures]\n-------------------------".format(numpics))
                sys.stdout.write("\033[0;32mMedia type: ")
                print("[{} Pictures]\n-------------------------".format(numpics))
        if feed['more_available']:
            set.color(set.BLUE)
            print("More posts available. Do you want to load more? (Enter=No / Input=Yes)")
            set.color(set.GREEN)
            if input("[Load more]: "):
                maxid = feed['next_max_id']
                continue
        set.color(set.BLUE)
        print("Choose post to download by its media number")
        set.color(set.GREEN)
        try:
            medianumber = int(input("[Media number]: "))
        except ValueError:
            return
        mediatype = feed['items'][medianumber]['media_type']
        k = 0
        if mediatype == 1:
            url = str(feed['items'][medianumber]['image_versions2']['candidates'][0]['url'])
            urllib.request.urlretrieve(url, PATH + 'Downloads/' + str(medianumber) + '.jpg')
            print("\n-------------------\n"
                  "Single Picture added to /Downloads/\n"
                  "-------------------")
        elif mediatype == 2:
            url = str(feed['items'][medianumber]['video_versions'][0]['url'])
            urllib.request.urlretrieve(url, PATH + 'Downloads/' + 'video_' + str(medianumber) + '.mp4')
            print("\n-------------------\n"
                  "Video added to /Downloads/\n"
                  "-------------------")
        elif mediatype == 8:
            print("\n-------------------")
            for i in feed['items'][medianumber]['carousel_media']:
                k += 1
                if 'video_versions' in i:
                    url = str(i['video_versions'][0]['url'])
                else:
                    url = str(i['image_versions2']['candidates'][0]['url'])
                urllib.request.urlretrieve(url, PATH + 'Downloads/' + feed['items'][medianumber]['user'][
                    'username'] + '_carousel_media_' + str(k) + '.jpg')
                print("Carousel media", str(k), "added to /Downloads/")
            print("-------------------\n")
        time.sleep(2.5)
        return True
