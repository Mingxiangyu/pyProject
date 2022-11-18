import datetime
import logging
import re
import time
import urllib
from html import unescape
from urllib.parse import urlparse, urljoin

import cchardet
import dateutil.parser
import requests
import unicodedata
from dateutil import parser as date_parser
# from fake_useragent import UserAgent
from flask import Flask
from gerapy_auto_extractor import is_list
from lxml import etree
from lxml.html import HtmlElement
from lxml.html import fromstring
from readability import Document

DELETE_SET = ["\r", "\n", "\t"]

USELESS_TAG = ['style', 'script', 'link', 'video', 'iframe', 'source', 'picture', 'header', 'blockquote',
               'footer']

# if one tag in the follow list does not contain any child node nor content, it could be removed
TAGS_CAN_BE_REMOVE_IF_EMPTY = ['section', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'span']

USELESS_ATTR = {
    'share',
    'contribution',
    'copyright',
    'copy-right',
    'disclaimer',
    'recommend',
    'related',
    'footer',
    'comment',
    'social',
    'submeta',
    'report-infor'
}


def normalize_text(html):
    """
    使用 NFKC 对网页源代码进行归一化，把特殊符号转换为普通符号
    :param html:
    :return:
    """

    return unicodedata.normalize('NFKC', html)


def str_to_timestamp(date):
    dt = datetime.datetime.now()
    year = dt.year
    month = dt.month
    day = dt.day
    hour = dt.hour
    minute = dt.minute
    second = dt.second
    now = int(time.time())
    isParse = False
    m = None
    if not isParse:
        m = re.search(u'(\d+)\s*秒前', date, re.M | re.I)
        if m:
            isParse = True
            now = now - int(m.group(1))
    if not isParse:
        m = re.search(u'(\d+)\s*分钟前', date, re.M | re.I)
        if m:
            isParse = True
            now = now - int(m.group(1)) * 60
    if not isParse:
        m = re.search(u'(\d+)\s*小时前', date, re.M | re.I)
        if m:
            isParse = True
            now = now - int(m.group(1)) * 60 * 60
    if not isParse:
        m = re.search(u'(\d+)\s*天前', date, re.M | re.I)
        if m:
            isParse = True
            now = now - int(m.group(1)) * 60 * 60 * 24
    if not isParse:
        m = re.search(u'(\d+)\s*个月前', date, re.M | re.I)
        if m:
            isParse = True
            now = now - int(m.group(1)) * 60 * 60 * 24 * 30
    if not isParse:
        m = re.search(u'今天\s*(\d+):(\d+)', date, re.M | re.I)
        if m:
            isParse = True
            hour = 0
            minute = 0
            second = 0
            if m.group(1):
                hour = m.group(1)
            if m.group(2):
                minute = m.group(2)
            s = str(year) + "-" + str(month) + "-" + str(day) + " " + str(hour) + ":" + str(minute) + ":" + str(second)
            d = date_parser.parse(s, fuzzy=True)
            now = int(time.mktime(d.timetuple()))
    if not isParse:
        m = re.search(u'(\d{2,4})?年?(\d{1,2})月(\d{1,2})日\s*(\d{1,2})?[:时]?(\d{1,2})?[:分]?(\d{1,2})?', date, re.M | re.I)
        if m:
            isParse = True
            hour = 0
            minute = 0
            second = 0
            if m.group(1):
                tmp_year = m.group(1)
                if len(str(tmp_year)) == 2:
                    tmp_year = int("20" + tmp_year)
                tmp_year = int(tmp_year)
                if 1970 < tmp_year <= int(year):
                    year = tmp_year
            if m.group(2):
                month = m.group(2)
            if m.group(3):
                day = m.group(3)
            if m.group(4):
                hour = m.group(4)
            if m.group(5):
                minute = m.group(5)
            if m.group(6):
                second = m.group(6)
            s = str(year) + "-" + str(month) + "-" + str(day) + " " + str(hour) + ":" + str(minute) + ":" + str(second)
            # print(s)
            try:
                d = dateutil.parser.parse(s, fuzzy=True)
                now = int(time.mktime(d.timetuple()))
            except:
                pass
            # now = int(time.mktime(d.timetuple()))
    if not isParse:
        m = re.search(
            r'(\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2})|(\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2})|(\d{1,2}-\d{1,2} \d{1,2}:\d{1,2})|(\d{4}/\d{1,2}/\d{1,2} \d{1,2}:\d{1,2}:\d{1,2})|(\d{4}/\d{1,2}/\d{1,2} \d{1,2}:\d{1,2})|(\d{1,2}/\d{1,2} \d{1,2}:\d{1,2})',
            date, re.M | re.I)
        if m:
            isParse = True
            date = m.group()
            d = date_parser.parse(date, fuzzy=True)
            t = int(time.mktime(d.timetuple()))
            if t < now:
                now = t

    if not isParse:
        try:
            m = date.split('·')[0] + " " + "00-00-00"
            d = dateutil.parser.parse(m, fuzzy=True)
            now = int(time.mktime(d.timetuple()))

        except:
            pass
    if not isParse:
        m = re.search(r'(\d{4})-(\d{2})-(\d{2})', date, re.M | re.I)
        if m:
            isParse = True
            year = m.group(1)
            month = m.group(2)
            day = m.group(3)
            s = str(year) + "-" + str(month) + "-" + str(day)
            d = dateutil.parser.parse(s, fuzzy=True)
            now = int(time.mktime(d.timetuple()))

    return now


def html2element(html):
    html = re.sub('</?br.*?>', '', html)
    element = fromstring(html)
    return element


def title_extract(self, element: HtmlElement, title_xpath: str = '') -> str:
    title_xpath = title_xpath
    title = (self.extract_by_xpath(element, title_xpath)
             or self.extract_by_htag_and_title(element)
             or self.extract_by_title(element)
             or self.extract_by_htag(element)
             )
    return title.strip()


def time_extractor(self, element: HtmlElement, publish_time_xpath: str = '') -> str:
    publish_time_xpath = publish_time_xpath
    publish_time = (self.extract_from_user_xpath(publish_time_xpath, element)  # 用户指定的 Xpath 是第一优先级
                    or self.extract_from_meta(element)  # 第二优先级从 Meta 中提取
                    or self.extract_from_text(element))  # 最坏的情况从正文中提取
    return publish_time


def author_extractor(self, element: HtmlElement, author_xpath=''):
    author_xpath = author_xpath
    if author_xpath:
        author = ''.join(element.xpath(author_xpath))
        return author
    text = ''.join(element.xpath('.//text()'))
    for pattern in self.author_pattern:
        author_obj = re.search(pattern, text)
        if author_obj:
            return author_obj.group(1)
    return ''


def is_empty_element(node: HtmlElement):
    return not node.getchildren() and not node.text


def drop_tag(node: HtmlElement):
    """
    only delete the tag, but merge its text to parent.
    :param node:
    :return:
    """
    parent = node.getparent()
    if parent is not None:
        node.drop_tag()


def normalize_node(element: HtmlElement):
    etree.strip_elements(element, *USELESS_TAG)
    for node in iter_node(element):
        # inspired by readability.
        if node.tag.lower() in TAGS_CAN_BE_REMOVE_IF_EMPTY and is_empty_element(node):
            remove_node(node)

        # merge text in span or strong to parent p tag
        if node.tag.lower() == 'p':
            etree.strip_tags(node, 'span')
            etree.strip_tags(node, 'strong')

        # if a div tag does not contain any sub node, it could be converted to p node.
        if node.tag.lower() == 'div' and not node.getchildren():
            node.tag = 'p'

        if node.tag.lower() == 'span' and not node.getchildren():
            node.tag = 'p'

        # remove empty p tag
        if node.tag.lower() == 'p' and not node.xpath('.//img'):
            if not (node.text and node.text.strip()):
                drop_tag(node)

        class_name = node.get('class')
        if class_name:
            if class_name in USELESS_ATTR:
                remove_node(node)
                break


def pre_parse(element):
    normalize_node(element)

    return element


def remove_node(node: HtmlElement):
    """
    this is a in-place operation, not necessary to return
    :param node:
    :return:
    """
    parent = node.getparent()
    if parent is not None:
        parent.remove(node)


def remove_noise_node(element, noise_xpath_list):
    noise_xpath_list = noise_xpath_list

    if not noise_xpath_list:
        return
    for noise_xpath in noise_xpath_list:
        nodes = element.xpath(noise_xpath)
        for node in nodes:
            remove_node(node)
    return element


def iter_node(element: HtmlElement):
    yield element
    for sub_element in element:
        if isinstance(sub_element, HtmlElement):
            yield from iter_node(sub_element)


def pad_host_for_images(host, url):
    """
    网站上的图片可能有如下几种格式：

    完整的绝对路径：https://xxx.com/1.jpg
    完全不含 host 的相对路径： /1.jpg
    含 host 但是不含 scheme:  xxx.com/1.jpg 或者  ://xxx.com/1.jpg

    :param host:
    :param url:
    :return:
    """
    if url.startswith('http'):
        return url
    parsed_uri = urlparse(host)
    scheme = parsed_uri.scheme
    if url.startswith(':'):
        return f'{scheme}{url}'
    if url.startswith('//'):
        return f'{scheme}:{url}'
    return urljoin(host, url)


def content_extract(self, selector, host='', body_xpath='', with_body_html=False):
    body_xpath = body_xpath
    if body_xpath:
        body = selector.xpath(body_xpath)[0]
    else:
        body = selector.xpath('//body')[0]
    for node in iter_node(body):
        node_hash = hash(node)
        density_info = self.calc_text_density(node)
        text_density = density_info['density']
        ti_text = density_info['ti_text']
        text_tag_count = self.count_text_tag(node, tag='p')
        sbdi = self.calc_sbdi(ti_text, density_info['ti'], density_info['lti'])
        images_list = node.xpath('.//img/@src')
        host = host
        if host:
            images_list = [pad_host_for_images(host, url) for url in images_list]
        node_info = {'ti': density_info['ti'],
                     'lti': density_info['lti'],
                     'tgi': density_info['tgi'],
                     'ltgi': density_info['ltgi'],
                     'node': node,
                     'density': text_density,
                     'text': ti_text,
                     'images': images_list,
                     'text_tag_count': text_tag_count,
                     'sbdi': sbdi}
        if with_body_html:
            body_source_code = unescape(etree.tostring(node, encoding='utf-8').decode())
            node_info['body_html'] = body_source_code
        self.node_info[node_hash] = node_info
    self.calc_new_score()
    result = sorted(self.node_info.items(), key=lambda x: x[1]['score'], reverse=True)
    return result


def get_real_time(pubtime_re, pubtime_gne):
    """
    根据全文正则匹配的时间与gne抽取的时间作对比，取出更合理的时间
    :param pubtime_re:
    :param pubtime_gne:
    :return:
    """
    # print(f"pubtime_re:{pubtime_re}pubtime_gne:{pubtime_gne}")

    rtimearr = time.localtime(pubtime_re)
    r_hour = rtimearr.tm_hour
    r_min = rtimearr.tm_min

    gtimearr = time.localtime(pubtime_gne)
    g_hour = gtimearr.tm_hour
    g_min = gtimearr.tm_min

    if g_hour != 0 or g_min != 0:
        return pubtime_gne
    elif r_hour != 0 or r_min != 0:
        return pubtime_re
    else:
        return int(time.time())


def extract(html,
            title_xpath='',
            author_xpath='',
            publish_time_xpath='',
            host='',
            body_xpath='',
            noise_node_list=None,
            with_body_html=False):
    # 对 HTML 进行预处理可能会破坏 HTML 原有的结构，导致根据原始 HTML 编写的 XPath 不可用
    # 因此，如果指定了 title_xpath/author_xpath/publish_time_xpath，那么需要先提取再进行
    # 预处理
    normal_html = normalize_text(html)
    doc = re.sub(r'<!--.*?-->', '', normal_html)
    doc = re.sub(r'<meta.*?>', '', doc)
    doc = re.sub(r'<script>.*?</script>', '', doc)
    dr = re.compile(r'<[^>]+>', re.S)
    doc = dr.sub('', doc)

    pubtime_re = str_to_timestamp(doc)
    # print(pub_time)
    # 增加稿件来源提取，采用正则方式
    source = ''
    # results = re.search(r">*\s*[　]*来源\s*[：\-:](</em>)*\s*(\S*?)((<)|(\s)|(/)|(，)|(）|\"))", doc, re.M|re.I)
    # if '来源：' in doc:
    # print("*"*100)
    results = re.search(r">*\s*[　]*来源\s*[：\-:](</em>)*\s*(\S*?)((<)|(\s)|(/)|(，)|(）|\"))", doc, re.M | re.I)

    if results:
        source = results.group(2)
        source = source.strip()

    normal_html = normalize_text(html)
    element = html2element(normal_html)
    title = title_extract(element, title_xpath=title_xpath)
    publish_time = time_extractor(element, publish_time_xpath=publish_time_xpath)
    author = author_extractor(element, author_xpath=author_xpath)
    element = pre_parse(element)
    remove_noise_node(element, noise_node_list)
    content = content_extract(element,
                              host=host,
                              with_body_html=with_body_html,
                              body_xpath=body_xpath)
    pubtime_gne = str_to_timestamp(publish_time)
    publish_time = get_real_time(pubtime_re, pubtime_gne)
    result = {'title': title,
              'author': author,
              # 'pub_time':publish_time,
              'publish_time': publish_time,
              'content': content[0][1]['text'],
              'source': source,
              'images': content[0][1]['images']
              }
    if with_body_html:
        result['body_html'] = content[0][1]['body_html']
    return result


def parse_html(html, host):
    content_result = {}

    doc = Document(html)
    content_result["title"] = doc.title()

    summary = doc.summary(html_partial=True).replace("\n", "").replace("\r", "")
    for a in DELETE_SET:
        summary = summary.replace(a, "")

    summary_node = etree.HTML(summary)
    etree.strip_tags(summary_node, "div", "img", "a", "html", "body", "svg", "link")
    etree.strip_attributes(summary_node, "href", "src")
    content_result["summary"] = str(etree.tostring(summary_node, encoding="UTF-8"), encoding="utf-8")

    tag_content = doc.summary(html_partial=True)

    clear_content = etree.HTML(tag_content).xpath('string(.)')

    print(clear_content)
    content_result["text"] = clear_content
    list_page = is_list(html, threshold=0.97)
    if not list_page:
        try:
            detail = extract(html, host=host)
            content_result["publish_time"] = detail["publish_time"]
            content_result["source"] = detail["source"]
            content_result["author"] = detail["author"]
            images = detail["images"]
            if not images:
                detail_node = etree.HTML(tag_content)
                images = detail_node.xpath("//img/@src")
            new_images = []
            for i in images:
                if i.startswith("http"):

                    if re.match("(.*jpeg.*|.*png.*|.*jpg.*)", i, re.I | re.M):
                        new_images.append(urllib.parse.urljoin(host, i))
            content_result["images"] = new_images
        except Exception as e:
            logging.exception(e)


    # list_result = _list_parse(html, host)
    # total_result["list"] = list_result

    return content_result


class Clearoutside(object):

    def __init__(self):
        self.url = "https://zh.wikipedia.org/wiki/{}"
        # ua = UserAgent(verify_ssl=False)
        for i in range(1, 100):
            # 产生随机的User - Agent请求头进行访问
            self.headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
                "accept": "*/*"
            }

    # 请求网站获取url
    def get_html(self, url) -> str:
        response = requests.get(url, headers=self.headers, timeout=30)
        content = response.content
        # 获取响应字符串编码
        encoding = cchardet.detect(content)['encoding']
        print("=============================================================")
        print(content.decode(encoding, errors="ignore"))
        print("=============================================================")

        if content is None:
            raise Exception("access failed")

        return content.decode(encoding, errors="ignore")

    def main(self, keyword):
        url = self.url.format(keyword)
        print("start download html:{}".format(url))
        html = self.get_html(url)
        # TODO 进行数据抽取
        baike_data = parse_html(html, "https://zh.wikipedia.org/wiki/")
        # json_baike = json.dumps(baike_data)
        # print(json_baike)
        # return json_baike
        return baike_data


app = Flask(__name__)  # 创建flask实例


@app.route("/spider/<string:keyword>")
def spider(keyword):
    spider = Clearoutside()
    json_baike = spider.main(keyword)
    return json_baike


@app.route("/")
def hello():
    return " hello word"


if __name__ == '__main__':
    # 启动flask，提供http接口
    # 如果是docker部署，需要注意ip指定为0.0.0.0，flask默认ip为127.0.0.1，docker启动时，无法在宿主机访问！！
    app.run(host="0.0.0.0", port=int("8000"))
