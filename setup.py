#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os


'''
Setup Script -> Creates folders: 
/Downloads/ 
/Configs/whitelist.txt 
/Configs/blacklist.txt 
/Downloads/Logs/Auto-Geo-Bot-Log.txt 
/Downloads/Logs/Auto-Tag-Bot-Log.txt 
/Downloads/Logs/Feed-Bot-Log.txt 
'''

if __name__ == '__main__':
    PATH = os.getcwd()
    os.mkdir(PATH + '/Downloads/')
    os.mkdir(PATH + '/Configs/Logs')
    CONFIG = PATH + '/Configs'
    # create .txt files in /Configs/
    blacklist = open(CONFIG + '/blacklist.txt', 'x')
    blacklist.write('\n')
    blacklist.close()
    whitelist = open(CONFIG + '/whitelist.txt', 'x')
    whitelist.write('\n')
    whitelist.close()
    LOG = CONFIG + '/Logs'
    # create .txt files in /Configs/Logs/
    geolog = open(LOG + '/Auto-Geo-Bot-Log.txt', 'x')
    geolog.write('\n')
    geolog.close()
    taglog = open(LOG + '/Auto-Tag-Bot-Log.txt', 'x')
    taglog.write('\n')
    taglog.close()
    feedlog = open(LOG + '/Feed-Bot-Log.txt', 'x')
    feedlog.write('\n')
    feedlog.close()
    
    print("Setup finished. All files created!")

