from urllib import request
from urllib import error
from bs4 import BeautifulSoup
from bs4 import re
import json


import ssl
# disable ssl verify in global
# ssl._create_default_https_context = ssl._create_unverified_context


# ex1
def get_title_ex1(url):
    try:
        html = request.urlopen(url)
    except error.HTTPError:
        return None
    try:
        bsObj = BeautifulSoup(html.read(), 'lxml')
        title = bsObj.html.h1
    except AttributeError:
        return None
    return title


def main_ex1():
    title = get_title_ex1('http://www.pythonscraping.com/pages/page1.html')
    if title is None:
        print('Title cound not be found')
    else:
        print(title)
        print(title.get_text())
        print(title.string)


# ex2
def get_name_list_ex2(url):
    try:
        html = request.urlopen(url)
    except error.HTTPError as e:
        return None
    try:
        bsObj = BeautifulSoup(html.read(), 'xml')
        nameList = bsObj.find_all("span", {"class": "green"})
    except AttributeError as e:
        return None
    return nameList


def main_ex2():
    nameList = get_name_list_ex2('http://www.pythonscraping.com/pages/warandpeace.html')
    if nameList is None:
        print('Error')
    else:
        for n in nameList:
            print(n.get_text())


# ex3
def children_and_descendants_ex3():
    html = request.urlopen('http://www.pythonscraping.com/pages/page3.html')
    bsObj = BeautifulSoup(html, 'lxml-xml')       # same as 'xml'
    #for child in bsObj.find("table", {"id": "giftList"}).descendants:   # or children
    #    print(child)
    #
    #for sibling in bsObj.find("table", {"id": "giftList"}).tr.next_siblings:
    #    print(sibling)
    #
    #print(bsObj.find("img", {"src": "../img/gifts/img1.jpg"}).parent.previous_sibling.get_text())
    #
    #images = bsObj.findAll("img", {"src": re.compile("\.\.\/img\/gifts/img.*\.jpg")})
    #for image in images:
    #    print(image["src"])
    #
    #tags = bsObj.findAll(lambda tag:len(tag.attrs)==2)
    #for tag in tags:
    #    print(tag.attrs)
    for link in bsObj.findAll('a'):
        if 'href' in link.attrs:
            print(link.attrs['href'])


# ex4
def wikipedia_find_links(url):
    req = request.Request(url)
    # gcontext = ssl._create_unverified_context()
    gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)   # Only for gangstars
    html = request.urlopen(req, context=gcontext)   # pass context to disable ssl verify
    bsObj = BeautifulSoup(html, 'lxml-xml')
    for link in bsObj.find("div", {"id": "bodyContent"}).findAll("a", href=re.compile("^(/wiki/)((?!:).)*$")):
        if 'href' in link.attrs:
            yield link.attrs['href']


def wikipedia_get_links(articleUrl, pages):
    newPages = set()
    for link in wikipedia_find_links("http://en.wikipedia.org"+articleUrl):
        newPages.add(link)
    newPages = newPages - pages
    pages = pages | newPages
    for newPage in newPages:
        wikipedia_get_links(newPage, pages)


def Kevin_Bacon_Links():
    pages = set()
    wikipedia_get_links('/wiki/Kevin_Bacon', pages)


def get_ip_json(ipAddress):
    res = request.urlopen("http://freegeoip.net/json/" + ipAddress).read()
    res = res.decode('utf-8')
    return json.loads(res)

if __name__ == '__main__':
    # Kevin_Bacon_Links()
    j = get_ip_json("50.78.253.58")
    print(j.get("country_code"))
