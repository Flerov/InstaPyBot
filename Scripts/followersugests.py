#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from InstagramAPI import InstagramAPI
from Scripts import colors as set
from time import sleep


time = 30


def followers_algorithm(api: InstagramAPI):  # suggested users to follow by instagrams algorithm
    api.getRecentActivity()
    data = api.LastJson
    users = {}

    # preparing dict -> username: pk
    for i in data['aymf']['items']:
        users[i['user']['username']] = []
        users[i['user']['username']].append(i['user']['pk'])      # 0
        users[i['user']['username']].append(i['algorithm'])       # 1
        users[i['user']['username']].append(i['social_context'])  # 2

    set.color(set.GREEN)
    for i in users:
        api.follow(users[i][0])
        print("----------------\n"
              "Username: {}".format(i))
        print("Algorithm: [{}]".format(users[i][1]))  # -> [0, 1, 2]
        print("Social Context: [{}]\n"
              "----------------\n".format(users[i][2]))  # -> [0, 1, 2]
        sleep(time)
