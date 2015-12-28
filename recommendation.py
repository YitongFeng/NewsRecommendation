__author__ = 'fyt'

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
import re
import jieba


train_news_ids = []
train_title_tf = []
train_body_tf = []
train_user_reads = {}

test_news_ids = []
test_title_tf = []  
test_body_tf = []
test_user_reads = {}

word_df_dic = {}


def data_process(filename):
    global stopkeys
    stopkeys = [line.strip() for line in open('stopword.txt').readlines()]     #stop key table
    t = (2014, 3, 20, 0, 0, 0, 3, 79, 0)    #2014.3.20 struct time
    stamp_time = time.mktime(t)      #convert to time stamp of Unix

    try:
        with open(filename, 'r') as f:
            for line in f:
                sp = line.split('\t')

                #filter out the chinese with regex
                #print('filter out the chinese with regex')
                regex = u"[\u4e00-\u9fa5]+"
                titles = re.findall(regex, sp[3])
                bodies = re.findall(regex, sp[4])

                #divide the dataset
                #print('divide the dataset')

                # training data set
                if int(sp[2]) < stamp_time:
                    if sp[1] not in train_news_ids:
                        train_news_ids.append(sp[1])
                        (title_tf_str, body_tf_str) = seg_and_count(titles, bodies)
                        train_title_tf.append(title_tf_str)
                        train_body_tf.append(body_tf_str)

                    if sp[0] not in train_user_reads:
                        train_user_reads[sp[0]] = str(sp[1])
                    else:
                        train_user_reads[sp[0]] += " " + str(sp[1])


                # test data set
                else:
                    if sp[1] not in test_news_ids:
                        test_news_ids.append(sp[1])
                        (title_tf_str, body_tf_str) = seg_and_count(titles, bodies)
                        test_title_tf.append(title_tf_str)
                        test_body_tf.append(body_tf_str)
                    if sp[0] not in train_user_reads:
                        train_user_reads[sp[0]] = str(sp[1])
                    else:
                        train_user_reads[sp[0]] += " " + str(sp[1])



        with open('words.txt', 'w') as f:
            # filter out the words according to df
            word_number = 0;
            for k, v in word_df_dic.items():
                if v < 500 and v > 5:
                    f.write(k + " " + str(v) + "\n")
                    word_number += 1;
                    print(word_number)

        with open('train_user_reads.txt', 'w') as f:
            for k, v in train_user_reads.items():
                f.write(k + "\t\t" + v + "\n")
        with open('test_user_reads.txt', 'w') as f:
            for k, v in test_user_reads.items():
                f.write(k + "\t\t" + v + "\n")
        with open('train_news_ids.txt', 'w') as f:
            f.writelines('\n'.join(train_news_ids))
        with open('test_news_ids.txt', 'w') as f:
            f.writelines('\n'.join(test_news_ids))

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

def seg_and_count(titles, bodies):
    #word segmentation
    #count the df of each word
    #count the tf of titles and bodies

    words = set()       # store the total word appered in news

    #word segmentation
    #print('word segmentation & remove stop keys')
    title_cuts = []
    for title in titles:
        title_cuts.extend(list(jieba.cut(title)))
    body_cuts = []
    for body in bodies:
        body_cuts.extend(list(jieba.cut(body)))

    #remove stop keys
    title_cuts_without_stopkeys = [word for word in title_cuts if len(word) >= 2 and word not in stopkeys]
    body_cuts_without_stopkeys = [word for word in body_cuts if len(word) >= 2 and word not in stopkeys]
    # use set to remove repeated words
    set_title_cuts = set(title_cuts_without_stopkeys)
    set_body_cuts = set(body_cuts_without_stopkeys)
    words = words | set_title_cuts | set_body_cuts
    # compute df of each word
    for w in words:
        if w in word_df_dic:
            word_df_dic[w] += 1
        else:
            word_df_dic[w] = 1

    #compute tf of each news' title and body
    #print('compute tf of each news\' title and body')
    dic_title_tf = {}
    for key1 in title_cuts_without_stopkeys:    # compute title-tf can't use set_title_cuts
        if key1 in dic_title_tf:
            dic_title_tf[key1] += 1
        else:
            dic_title_tf[key1] = 1

    dic_body_tf = {}
    for key2 in body_cuts_without_stopkeys:
        if key2 in dic_body_tf:
            dic_body_tf[key2] = dic_body_tf[key2] + 1
        else:
             dic_body_tf[key2] = 1

    title_tf_str = ""
    for k, v in dic_title_tf.items():
        title_tf_str += k + " " + str(v) + " "
    body_tf_str = ""
    for k, v in dic_body_tf.items():
        body_tf_str += k + " " + str(v) + " "

    return (title_tf_str, body_tf_str)

print(sys.getdefaultencoding())