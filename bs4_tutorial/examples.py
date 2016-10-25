from urllib import request
from urllib import error
from bs4 import BeautifulSoup


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
def get_gif_list_ex3(url):
    try:
        html = request.urlopen(url)
    except error.HTTPError as e:
        return None
    try:
        bsObj = BeautifulSoup(html.read(), 'xml')
        l = bsObj.find_all('span', )
    except AttributeError as e:
        return None
    return l


def main_ex3():
    l = get_gif_list_ex3('')


if __name__ == '__main__':
    main_ex1()
    # main_ex2()
