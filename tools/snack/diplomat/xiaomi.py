#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
root_mod = '/home/sdu/MyProject/tools'
sys.path.append(root_mod)

import re

import datetime
from lxml import etree, html

from mysql import query, query_one, save

from tools.crawler.utils.crawler.process import (extract_content_by_xpath,
                                                 extract_link_by_re,
                                                 extract_pubtime_by_re,
                                                 extract_item_by_re,
                                                 extract_title_by_xpath,
                                                 get_response, is_last_node,
                                                 get_max_page_number)


def get_data():
    page = 0
    while(True):
        url = 'http://market.xiaomi.com/apm/comment/list/108048?channel=market_100_1_android&clientId=56df5d2d2eafff6a7366aa331b99ff14&co=CN&densityScaleFactor=2.0&imei=70b45cdc762b8a01062cd7e18d92d81b&la=zh&marketVersion=146&model=XT1060&os=1&page=%s&resolution=720*1184&sdk=22&session=2jmj7l5rSw0yVb_v' % page
        page += 1
        handle_data(get_response(url).text)


def handle_data(source_data):
    source_data = source_data.replace('false', 'False')
    source_data = source_data.replace('true', 'True')
    data = eval(source_data)
    messages = data.get('comments')
    for message in messages:
        username = message.get('nickname')
        user_star = message.get('score')
        game_version = message.get('versionName')
        content = message.get('commentValue')
        create_at = datetime.datetime.fromtimestamp(int(message.get('updateTime')) / 1e3)
        likes = message.get('likes')
        comment_number = message.get('replies')
        model = message.get('model')
        weight = message.get('weight')
        image_url = message.get('image_url')
        channel = 'xiaomi';

        if save(sql=u'''INSERT INTO `base_comment`(`username`, `user_star`, `game_version`, `content`, `create_at`, `likes`, `comment_number`, `model`, `weight`, `image_url`, `channel`) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s , %s) ''', list1=(username, user_star, game_version, content, create_at, likes, comment_number, model, weight, image_url, channel)):
            print "INSERT INTO < %s > SUCCESSFUL!" % username


def main():
    get_data()

if __name__ == '__main__':
    main()
