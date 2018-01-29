import os
import grequests

from multiprocessing import Process
from multiprocessing import Pool

import requests
from bs4 import BeautifulSoup

def get_url(_url, _filepath):
    if os.path.isfile(_filepath):
        return True

    try:
        resp = requests.get(_url)
    except:
        return False

    with open(_filepath, 'w', encoding='utf-8') as fo:
        fo.write(resp.text)

    print(_url)

    return True


def get_main(main_url="http://www.01net.com/archives/"):
    get_url(main_url, 'main.html')

    return True


def parse_main(file_path):
    result = []
    with open(file_path, 'r', encoding='utf-8') as fi:
        html = fi.read()

    soup = BeautifulSoup(html, 'html.parser')

    h3s = soup.find_all('h3', 'title-large bloc')

    for h in h3s:
        print(h.text)
        ns = h.next_siblings

        for tag in ns:
            if tag.name != 'ul':
                continue

            a_list = tag.find_all('a')

            for a in a_list:
                month_url = a.attrs['href']
                result.append(month_url)

    return result


def parse_month(dir_path, filename):
    _filepath = dir_path + filename

    with open(_filepath, 'r', encoding='utf-8') as fi:
        text = fi.read()

    soup = BeautifulSoup(text, 'html.parser')

    ul = soup.find('ul', 'list-unstyled')
    a_list = ul.find_all('a')

    for a in a_list:
        url = a.attrs['href']
        title = a.attrs['title']
        title_name = title.replace(' ', '_') + '.html'
        date = title_name.split('_')[1]

        old_filepath = dir_path + title_name

        new_dir = dir_path + date + '/'

        if not os.path.isdir(new_dir):
            os.mkdir(new_dir)

        new_filepath = new_dir + title_name

        if os.path.isfile(old_filepath):
            os.remove(old_filepath)

        print(new_filepath)

        if not get_url(url, new_filepath):
            print("[parse_month][error] %s" % new_dir + title_name)
            continue

        parse_day(new_dir, title_name)

    return True


def parse_day(dir_path, filename):
    filepath = dir_path + filename
    old_dir = "/".join(dir_path.split("/")[:-2]) + "/"

    with open(filepath, 'r', encoding='utf-8') as fi:
        text = fi.read()

    soup = BeautifulSoup(text, 'html.parser')

    ul = soup.find('ul', 'list-unstyled')

    a_list = ul.find_all('a')

    # for a in a_list:
    #     # title = a.attrs['title']
    #     url = a.attrs['href']
    #     html_name = url.split('/')[-1]

    #     get_url(url, dir_path + html_name)

    #     if os.path.isfile(old_dir + html_name):
    #         os.remove(old_dir + html_name)

    rs = list()
    for a in a_list:
        url = a.attrs['href']
        html_name = url.split('/')[-1]

        if os.path.isfile(dir_path + html_name):
            continue

        rs.append(grequests.get(url))

    resp_list = grequests.map(rs)

    for resp in resp_list:
        print(resp.url)
        html_name = resp.url.split('/')[-1]
        
        with open(dir_path + html_name, 'w', encoding='utf-8') as fi:
            fi.write(resp.text)

    return True


def parse(_month_url):
    parts = _month_url.split('/')
    dir_name =  '_'.join(parts[-4:-1])
    dir_path = './archive_data/' + dir_name + '/'

    if not os.path.isdir(dir_path):
        print(dir_path)
        os.mkdir(dir_path)

    file_name = dir_name + '.html'
    file_path = dir_path + file_name

    if not get_url(_month_url, file_path):
        print("[Error] %s" % _month_url)

    parse_month(dir_path, file_name)

    return True


if __name__ == '__main__':
    month_list = parse_main('main.html')

    # for month_url in month_list:
    #     parse(month_url)

    proc_num = 20
    pl = Pool(processes=proc_num)

    arg_list = list()

    skip_list = list() # ['%d' % n for n in range(2000, 2019)]
    print(skip_list)

    for month_url in month_list:
        year = month_url.split('/')[-3]
        if year in skip_list:
            continue
        print(month_url)
        arg_list.append((month_url,))

    pl.starmap(parse, arg_list)


