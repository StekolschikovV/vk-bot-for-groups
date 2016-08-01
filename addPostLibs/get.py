import requests
from lxml import html
from grab import Grab
import logging
import urllib
from bs4 import BeautifulSoup
from lxml import html
import re

ALL_TEXT = ''
ALL_HTML = ''
TITLE_TEXT = ''
BODY_TEXT = ''

def all_page(url):
    response = requests.get(url, timeout=1)
    parsed_body = html.fromstring(response.text)
    text_from_url = parsed_body.xpath('//*/text()')
    global ALL_HTML
    ALL_HTML = response.text
    return " ".join(str(x) for x in text_from_url)


def post_title(url):
    print('Заупуск функци post_title:', url, '\n')
    if 'nnm' in url:
        s = ALL_TEXT[:ALL_TEXT.find(' torrent :: NNM-Club')]
        return s.lstrip()
    else:
        return ''

def post_tegs(url):
    print('Заупуск функци post_tegs:', url, '\n')
    try:
        result_list = []
        #получили список наших тегов
        f = open('tegs.txt', 'r+')
        f = f.read()
        list_f = f.split()
        # list_f.lower()
        print('Получен список тегов\n')
        #получили текст страницы
        text_from_url = BODY_TEXT.lower() + TITLE_TEXT.lower()
        #поиск тегов
        for i in list_f:
            if i in text_from_url:
                print('Совпадение: ', i)
                result_list.append('#'+i)
        result_list = " ".join(str(x) for x in result_list)
        return result_list
    except:
        print('ERROR: cant open!\n')

def post_img(url):
    print('Заупуск функци post_img:', url, '\n')
    try:
        txt = BeautifulSoup(ALL_HTML)
        img = txt.find('var', {'class': 'postImg'})
        img = img.attrs["title"]
        print(img, type(img))
        p = requests.get(img)
        out = open("img.jpg", "wb")
        out.write(p.content)
        out.close()
        return 'img.jpg'
    except:
        print('ERROR post_img:', '\n')
        return ''

def post_text(url):
    try:
        s =ALL_TEXT.find('Описание:') + 9
        e =ALL_TEXT.find('<br /><a')
        t = ALL_TEXT[s:e]
        # дополнительный посик
        if 'Продолжительность' in t:
            text = ALL_TEXT.find('Продолжительность')
            t = ALL_TEXT[s:text]
        if 'Чему вы научитесь' in t:
            text = ALL_TEXT.find('Чему вы научитесь')
            t = ALL_TEXT[s:text]
        if 'Скриншоты' in t:
            text = ALL_TEXT.find('Скриншоты')
            t = ALL_TEXT[s:text]
        if 'Раздача' in t:
            text = ALL_TEXT.find('Раздача')
            t = ALL_TEXT[s:text]

        if len(t) > 400:
            t = t[:400] + '...'
        r = re.sub(r'(\<(/?[^>]+)>)', '', t )
        return r[1:]
    except:
        return ''