#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


"""
  function: query doc tag statistics
created by: wx617977
created at: 2019/3/27 00:30
updated at:
copyright:
"""

from collections import OrderedDict
import codecs


def get_topk_query(keyword_log_file, topk_num):
    """
    get topk query by download count
    :param keyword_log_file:
    :param topk_num:
    :return: topk query's reversing ordered dictionary
    """
    query_dict = OrderedDict()
    with codecs.open(keyword_log_file, 'r') as rf:
        for line in rf.readlines():
            items = line.split('|')
            query = items[0]
            download_count = items[-1]
            query_dict[query] = int(download_count)

    return OrderedDict(list(sorted(query_dict.items(), key=lambda x: -x[1]))[:topk_num])


def get_topk_query_app_lick_log(app_click_log_file, wanted_keys, name_dict: OrderedDict, topk):
    """
    get topk's doc from every query's app lick log
    :param wanted_keys: the queries to get DOC
    :param name_dict: the dictionary of APPID and DOC
    :param topk: limit to get the size of topk's doc
    :return: a ordered dictionary of ordered dictionary
    """
    click_log_dict = {}
    with codecs.open(app_click_log_file, 'r') as rf:
        for line in rf.readlines():
            items = line.split('|')
            current_key = items[0]
            app_id = items[1]
            app_download_count = items[-1]
            if click_log_dict.__contains__(current_key):
                click_log_dict[current_key][app_id] = (name_dict[app_id], app_download_count)
            else:
                click_log_dict[current_key] = OrderedDict()
                if name_dict.__contains__(app_id):
                    click_log_dict[current_key][app_id] = (name_dict[app_id], app_download_count)

    for key, doc_dict in click_log_dict.items():
        click_log_dict[key] = OrderedDict(list(sorted(doc_dict.items(), key=lambda x: -x[1][1])[:topk]))

    return click_log_dict


def load_resources(filename):
    """
    load resource file like this:
    APPID|string
    :param filename:
    :return: a dictionary that key is APPID, value is string
    """
    resource_dict = {}
    with codecs.open(filename, 'r') as rf:
        for line in rf.readlines():
            app_id = line.split('|')[0]
            value_str = line.split('|')[-1]
            resource_dict[app_id] = value_str

    return resource_dict


def count_word_frequency(word_list, topk):
    """
    count the words' frequency in list
    :param word_list: a string list
    :param topk: limitation number of result size
    :return: a dictionary ofr words frequency
    """
    wordfreq = OrderedDict()
    for w in word_list:
        wordfreq[w] = word_list.count(w)

    return OrderedDict(list(sorted(wordfreq.items(), key=lambda x: -x[1]))[:topk])


def get_tag_word_frequency(tag_dict, app_click_log_dict, topk):
    """
    get tags' words frequency count
    :param tag_dict:
    :param app_click_log_dict:
    :return: tags' words frequency dictionary
    """
    word_dict = OrderedDict()
    for query, click_log_dict in app_click_log_dict.items():
        tag_list = []
        for app_id in click_log_dict.keys():
            tag_list = tag_list + tag_dict[app_id].split(',')
        word_dict[query] = count_word_frequency(tag_list, topk)
    return word_dict


def save_topk_doc(data, output_file):
    """
    query|["doc1", "doc2", ...]
    :param data:
    :param output_file:
    :return:
    """
    pass


def save_topk_tag(data, output_file):
    """
    query|[tag_word1, tag_word2, ...]
    :param data:
    :param output_file:
    :return:
    """

    pass


def save_topk_doc_query(data, output_file):
    """
    doc|[query1, query2, ...]
    :param data:
    :param output_file:
    :return:
    """
    pass


if __name__ == '__main__':
    # limit doc size
    doc_topk = 100
    # get top 10000 query
    keyword_click_log_file = ''
    app_click_log_file = ''

    doc_file = ''
    first_tag_file = ''
    second_tag_file = ''
    third_tag_file = ''

    doc_dict = load_resources(doc_file)
    first_tag_dict = load_resources(first_tag_file)
    second_tag_dict = load_resources(second_tag_file)
    third_tag_dict = load_resources(third_tag_file)

    keyword_click_log_dict = get_topk_query(keyword_click_log_file)
    app_click_log_dict = get_topk_query_app_lick_log(app_click_log_file, keyword_click_log_dict.keys(), doc_dict,
                                                     doc_topk)

