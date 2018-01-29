import os
from multiprocessing import Process
from multiprocessing import Pool

from bs4 import BeautifulSoup


def parse_file(file_path, fo):
    if ".DS_Store" in file_path:
        return False

    if not file_path.endswith(".html"):
        return False

    print(file_path)
    
    with open(file_path, 'r', encoding='utf-8') as fi:
        text = fi.read()

    soup = BeautifulSoup(text, 'html.parser')

    for script in soup(["script", "style"]):
        script.extract()

    path_parts = file_path.split('/')

    result = {
        "yyyymm": path_parts[-3],
        "dd": path_parts[-2],
        "filename": path_parts[-1],
        "title":"",
        "main":"",
        "author":"",
        "date":"",
    }

    # title
    item = soup.find("h1", {"itemprop":"headline"})
    if item is not None:
        result["title"] += item.text.replace("\n", "").replace("  ", "").replace("|", "")

    # main
    item = soup.find("div", {"itemprop":"articleBody"})
    if item is not None:
        result["main"] += item.text.replace("\n", "").replace("  ", "").replace("|", "")

    # author
    item = soup.find("strong", {"rel":"author"})
    if item is not None:
        result["author"] += item.text.replace("\n", "").replace("  ", "").replace("|", "")

    # date
    item = soup.find("time", {"itemprop":"datePublished"})
    if item is not None:
        result["date"] += item.text.replace("\n", "").replace("  ", "").replace("|", "")

    # print(result)

    wline = "%(filename)s|%(yyyymm)s|%(dd)s|%(title)s|%(main)s|%(author)s|%(date)s\n" % result

    # print(wline)

    fo.write(wline)

    return True


def parse(_dir):
    list_dir = os.listdir(_dir)

    with open("result.csv", 'w', encoding='utf-8') as fo:
        fo.write("TITLE|MAIN|AUTHOR|DATE\n")
        for dir_name in list_dir:
            # print(dir_name)
            
            month_dir_path = _dir + dir_name + '/'

            if '.' in dir_name:
                continue

            print(month_dir_path)

            day_list = os.listdir(month_dir_path)

            for day in day_list:
                if "archives_" in day:
                    continue
                day_dir_path = month_dir_path + day + '/'
                print(day_dir_path)

                if ".DS_Store" in day_dir_path:
                    continue

                article_list = os.listdir(day_dir_path)

                for article in article_list:
                    article_path = day_dir_path + article
                    parse_result = parse_file(article_path, fo)

    return True

def parse_monthly(month_dir):
    yyyymm = month_dir.split('/')[-2]

    with open(month_dir + "result_%s.csv" % yyyymm, 'w', encoding='utf-8') as fo:
        fo.write("FILENAME|YYYYMM|DD|TITLE|MAIN|AUTHOR|DATE\n")
        
        day_list = os.listdir(month_dir)

        for day in day_list:
            if "archives_" in day:
                continue

            if "." in day:
                continue

            day_dir_path = month_dir + day + '/'
            print(day_dir_path)

            article_list = os.listdir(day_dir_path)

            for article in article_list:
                article_path = day_dir_path + article
                parse_result = parse_file(article_path, fo)


if __name__ == '__main__':
    root_dir_path = "./archive_data/"

    month_archives = os.listdir(root_dir_path)

    proc_num = 12
    pl = Pool(processes=proc_num)

    arg_list = list()

    for month_dirname in month_archives:
        print(month_dirname)
        if "." in month_dirname:
            continue

        month_dir_path = root_dir_path + month_dirname + '/'
        arg_list.append((month_dir_path,))

    pl.starmap(parse_monthly, arg_list)

