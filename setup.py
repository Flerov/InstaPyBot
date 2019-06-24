#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time


'''
Setup Script creates folders:
    /Sessions/
    /InstaAI/Images
    /InstaAI/quotes.txt
    /InstaAI/log.txt
    /InstaAI/igcreators.txt
'''

if __name__ == '__main__':
    PATH = os.getcwd()
    os.mkdir(PATH + '/Sessions/')
    #os.mkdir(PATH + '/InstaAI/Images/')
    #with open(PATH + '/InstaAI/quotes.txt', 'x') as file:
    #    file.write('Change me with some descriptions')
    #with open(PATH + '/InstaAI/log.txt', 'x') as file:
    #    file.write('\n')
    #with open(PATH + '/InstaAI/igcreators.txt', 'x') as file:
    #    file.write('Change me with a list of instagram photographers\nFrom this list I will automatically fetch some high quality posts')
    print("Setup finished. All files created")
    time.sleep(3)
