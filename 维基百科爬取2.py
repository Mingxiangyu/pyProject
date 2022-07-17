# -*- coding:utf-8 -*-

import requests
import json
import logging
import sys
import os.path
import re

agreement = 'https://'
language = 'en'
organization = '.wikipedia.org/w/api.php'

API_URL = agreement + language + organization

program = os.path.basename(sys.argv[0])
logger = logging.getLogger(program)
logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')


def pageid(title=None, np=0):
    global API_URL
    URL = API_URL
    query_params = {
        'action': 'query',
        'prop': 'info',
        'format': 'json',
        'titles': title
    }
    if np != 0:
        query_params['titles'] = 'Category:' + title
    try:
        r = requests.get(URL, params=query_params)
        r.raise_for_status()
        html, r.encoding = r.text, 'gb2312'
    except:
        html = ""
    if html == "":
        return -1
    else:
        try:
            text = json.loads(html, encoding='gb2312')
        except json.JSONDecodeError:
            return -1
        try:
            for i in text["query"]['pages']:
                return int(i)
        except:
            return -1


def summary(title=None):
    global API_URL
    URL = API_URL
    query_params = {
        'action': 'query',
        'prop': 'extracts',
        'explaintext': '',
        'exintro': '',
        'format': 'json',
        'titles': title
    }
    try:
        r = requests.get(URL, params=query_params)
        r.raise_for_status()
        html, r.encoding = r.text, 'gb2312'
    except:
        logger.error('error summary about ' + title)
        return ""
    text = json.loads(html, encoding='gb2312')
    id = list(text["query"]["pages"].keys())[0]
    try:
        return text["query"]["pages"][id]["extract"]
    except:
        return ""


def body(title=None):
    global API_URL
    URL = API_URL
    query_params = {
        'action': 'query',
        'prop': 'extracts',
        'exlimit': 'max',
        'format': 'json',
        'titles': title
    }
    try:
        r = requests.get(URL, params=query_params)
        r.raise_for_status()
        html, r.encoding = r.text, 'gb2312'
    except:
        logger.error('error body about ' + title)
        return ""
    text = json.loads(html, encoding='gb2312')
    id = list(text["query"]["pages"].keys())[0]
    try:
        html_text = text["query"]["pages"][id]["extract"]

        def stripTagSimple(htmlStr):
            '''
            最简单的过滤html <>标签的方法    注意必须是<任意字符>  而不能单纯是<>
            :param htmlStr:
            '''
            #         dr =re.compile(r'<[^>]+>',re.S)
            dr = re.compile(r'</?\w+[^>]*>', re.S)
            htmlStr = re.sub(dr, '', htmlStr)
            return htmlStr

        html_text = stripTagSimple(html_text)
        html_text = str(html_text).replace("\n", "")
        return html_text
    except:
        return ""


def links(title=None):
    global API_URL
    URL = API_URL
    query_params = {
        'action': 'query',
        'prop': 'links',
        'pllimit': 'max',
        'plnamespace': '0',
        'format': 'json',
        'titles': title
    }
    try:
        r = requests.get(URL, params=query_params)
        r.raise_for_status()
        html, r.encoding = r.text, 'gb2312'
    except:
        logger.error('error links about ' + title)
        return list()
    text = json.loads(html, encoding='gb2312')
    id = list(text["query"]["pages"].keys())[0]
    link = list()
    summ = summary(title)
    try:
        for obj in text["query"]['pages'][id]["links"]:
            if obj['title'] in summ or obj['title'].lower() in summ:
                link.append(obj['title'])
    except:
        return link
    return link


def linkss(title=None):
    global API_URL
    URL = API_URL
    query_params = {
        'action': 'query',
        'prop': 'links',
        'pllimit': 'max',
        'plnamespace': '0',
        'format': 'json',
        'titles': title
    }
    try:
        r = requests.get(URL, params=query_params)
        r.raise_for_status()
        html, r.encoding = r.text, 'gb2312'
    except:
        logger.error('error linkss about ' + title)
        return list()
    text = json.loads(html, encoding='gb2312')
    id = list(text["query"]["pages"].keys())[0]
    link = list()
    try:
        for obj in text["query"]['pages'][id]["links"]:
            link.append(obj['title'])
    except:
        return link
    return link


def backlinks(title=None):
    global API_URL
    URL = API_URL
    query_params = {
        'action': 'query',
        'list': 'backlinks',
        'bllimit': 'max',
        'blnamespace': '0',
        'format': 'json',
        'bltitle': title
    }
    try:
        r = requests.get(URL, params=query_params)
        r.raise_for_status()
        html, r.encoding = r.text, 'gb2312'
    except:
        logger.error('error backlinks about ' + title)
        return list()
    text = json.loads(html, encoding='gb2312')
    link = list()
    try:
        link = [obj['title'] for obj in text["query"]["backlinks"]]
    except:
        return link
    return link


def categories(title=None):
    global API_URL
    URL = API_URL
    query_params = {
        'action': 'query',
        'prop': 'categories',
        'cllimit': 'max',
        'clshow': '!hidden',
        'format': 'json',
        'clcategories': '',
        'titles': title
    }
    try:
        r = requests.get(URL, params=query_params)
        r.raise_for_status()
        html, r.encoding = r.text, 'gb2312'
    except:
        logger.error('error categories about ' + title)
        return list()
    text = json.loads(html, encoding='gb2312')
    id = list(text["query"]["pages"].keys())[0]
    category = set()
    if id != -1:
        try:
            category = [obj['title'][9:] for obj in text["query"]['pages'][id]["categories"]]
        except:
            return category
    return category


def redirects(title=None):
    global API_URL
    URL = API_URL
    query_params = {
        'action': 'query',
        'prop': 'redirects',
        'rdlimit': 'max',
        'format': 'json',
        'titles': title
    }
    try:
        r = requests.get(URL, params=query_params)
        r.raise_for_status()
        html, r.encoding = r.text, 'gb2312'
    except:
        logger.error('error redirects about ' + title)
        return list()
    text = json.loads(html, encoding='gb2312')
    id = list(text["query"]["pages"].keys())[0]
    redirect = list()
    if id != -1:
        try:
            redirect = [obj['title'] for obj in text["query"]['pages'][id]["redirects"]]
        except:
            return redirect
    return redirect


def subcats(title=None):
    global API_URL
    URL = API_URL
    query_params = {
        'action': 'query',
        'list': 'categorymembers',
        'cmtype': 'subcat',
        'cmlimit': 'max',
        'format': 'json',
        'cmtitle': 'Category:' + title
    }
    try:
        r = requests.get(URL, params=query_params)
        r.raise_for_status()
        html, r.encoding = r.text, 'gb2312'
    except:
        logger.error('error subcats about ' + title)
        return list()
    text = json.loads(html, encoding='gb2312')
    subcat = list()
    try:
        subcat = [obj['title'][9:] for obj in text["query"]['categorymembers']]
    except:
        return subcat
    return subcat


def supercats(title=None):
    global API_URL
    URL = API_URL
    query_params = {
        'action': 'query',
        'prop': 'categories',
        'cllimit': 'max',
        'format': 'json',
        'clshow': '!hidden',
        'titles': 'Category:' + title
    }
    try:
        r = requests.get(URL, params=query_params)
        r.raise_for_status()
        html, r.encoding = r.text, 'gb2312'
    except:
        logger.error('error supercats about ' + title)
        return list()
    text = json.loads(html, encoding='gb2312')
    id = list(text["query"]["pages"].keys())[0]
    supercat = list()
    if id != -1:
        try:
            supercat = [obj['title'][9:] for obj in text["query"]['pages'][id]["categories"]]
        except:
            return supercat
    return supercat


def contributors(title=None):
    global API_URL
    URL = API_URL
    query_params = {
        'action': 'query',
        'prop': 'contributors',
        'pclimit': 'max',
        'format': 'json',
        'titles': title
    }
    try:
        r = requests.get(URL, params=query_params)
        r.raise_for_status()
        html, r.encoding = r.text, 'gb2312'
    except:
        logger.error('error linkss about ' + title)
        return list()
    text = json.loads(html, encoding='gb2312')
    id = list(text["query"]["pages"].keys())[0]
    contributors = list()
    try:
        for obj in text["query"]['pages'][id]["contributors"]:
            contributors.append(obj['userid'])
    except:
        return contributors
    return contributors


if __name__ == '__main__':
    title = "Computer networks"
    id = pageid(title, np=4)
    summ = summary(title)
    Out = links(title)
    print(id)
    print(summ)
    print(Out)
