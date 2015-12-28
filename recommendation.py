__author__ = 'fyt'

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
import re
import jieba


train_user_ids = []
train_news_ids = []
train_read_time = []
train_news_title = []
train_news_body = []
train_publish_time = []
train_title_tf = []
train_body_tf = []
train_title_tf = []
train_body_tf = []

test_user_ids = []
test_news_ids = []
test_read_time = []
test_news_title = []
test_news_body = []
test_publish_time = []
test_title_tf = []  
test_body_tf = []
test_title_tf = []
test_body_tf = []

def data_process(filename):
    stopkeys = [line.strip() for line in open('stopword.txt').readlines()]     #stop key table
    t = (2014, 3, 20, 0, 0, 0, 3, 79, 0)    #2014.3.20 struct time
    stamp_time = time.mktime(t)      #convert to time stamp of Unix
    words = set()       # store the total word appered in news

    try:
        with open(filename, 'r') as f:
            for line in f:
                sp = line.split('\t')

                #filter out the chinese with regex
                print('filter out the chinese with regex')
                regex = u"[\u4e00-\u9fa5]+"
                titles = re.findall(regex, sp[3])
                bodies = re.findall(regex, sp[4])

                #word segmentation
                print('word segmentation & remove stop keys')
                title_cuts = []
                for title in titles:
                    title_cuts.extend(list(jieba.cut_for_search(title, HMM=True)))
                body_cuts = []
                for body in bodies:
                    body_cuts.extend(list(jieba.cut_for_search(body, HMM=True)))

                #remove stop keys
                title_cuts_without_stopkeys = [word for word in title_cuts if word not in stopkeys]
                body_cuts_without_stopkeys = [word for word in body_cuts if word not in stopkeys]

                words = words | set(title_cuts_without_stopkeys) | set(body_cuts_without_stopkeys)

                #compute tf of each news' title and body
                print('compute tf of each news\' title and body')
                dic_title_tf = {}
                for key1 in title_cuts_without_stopkeys:
                    if key1 in dic_title_tf:
                        dic_title_tf[key1] = dic_title_tf[key1] + 1
                    else:
                        dic_title_tf[key1] = 1

                dic_body_tf = {}
                for key2 in body_cuts_without_stopkeys:
                    if key2 in dic_body_tf:
                        dic_body_tf[key2] = dic_body_tf[key2] + 1
                    else:
                        dic_body_tf[key2] = 1

                #divide the dataset
                print('divide the dataset')
                if int(sp[2]) < stamp_time:
                    train_user_ids.append(sp[0])
                    train_news_ids.append(sp[1])
                    train_read_time.append(sp[2])
                    train_news_title.append(sp[3])
                    train_news_body.append(str(sp[4]))
                    train_publish_time.append(sp[5])

                    tmpstr = ""
                    for k, v in dic_title_tf.items():
                        tmpstr += k + " " + str(v) + " "
                    train_title_tf.append(tmpstr)

                    tmpstr = ""
                    for k, v in dic_body_tf.items():
                        tmpstr += k + " " + str(v) + " "
                    train_body_tf.append(tmpstr)

                else:
                    test_user_ids.append(sp[0])
                    test_news_ids.append(sp[1])
                    test_read_time.append(sp[2])
                    test_news_title.append(sp[3])
                    test_news_body.append(str(sp[4]))
                    test_publish_time.append(sp[5])

                    tmpstr = ""
                    for k, v in dic_title_tf.items():
                        tmpstr += k + " " + str(v) + " "
                    test_title_tf.append(tmpstr)

                    tmpstr = ""
                    for k, v in dic_body_tf.items():
                        tmpstr += k + " " + str(v) + " "
                    test_body_tf.append(tmpstr)

        with open('words.txt', 'w') as f:
            f.writelines('\t'.join(list(words)))
        with open('train_user_ids.txt', 'w') as f:
            f.writelines('\n'.join(train_user_ids))
        with open('test_user_ids.txt', 'w') as f:
            f.writelines('\n'.join(test_user_ids))
        with open('train_news_ids.txt', 'w') as f:
            f.writelines('\n'.join(train_news_ids))
        with open('test_news_ids.txt', 'w') as f:
            f.writelines('\n'.join(test_news_ids))
        with open('train_news_title.txt', 'w') as f:
            f.writelines('\n'.join(train_news_title))
        with open('test_news_title.txt', 'w') as f:
            f.writelines('\n'.join(test_news_title))
        with open('train_news_body.txt', 'w') as f:
            f.writelines('\n'.join(train_news_body))
        with open('test_news_body.txt', 'w') as f:
            f.writelines('\n'.join(test_news_body))
        with open('train_title_tf.txt', 'w') as f:
            f.writelines('\n'.join(train_title_tf))
        with open('test_title_tf.txt', 'w') as f:
            f.writelines('\n'.join(test_title_tf))
        with open('train_body_tf.txt', 'w') as f:
            f.writelines('\n'.join(train_body_tf))
        with open('test_body_tf.txt', 'w') as f:
            f.writelines('\n'.join(test_body_tf))

    except IOError as ioerr:
        print('File Error' + str(ioerr))    #print the error
        return None



print(sys.getdefaultencoding())