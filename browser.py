import os
import sys
import argparse
import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style

parser = argparse.ArgumentParser(description='')
parser.add_argument('dir', type=str, nargs='?', help='folder name')
args = parser.parse_args()


if args.dir:
    if not os.access(args.dir, os.W_OK):
        os.mkdir(args.dir)


def fix_url(raw_url):
    if "https://" not in raw_url and "http://" not in raw_url:
        return f"https://{raw_url}"
    else:
        return raw_url


def get_filename(site_url):
    return site_url.replace("https://", "").replace("http://", "")\
        .replace("www.", "").replace("/", ".").split(".")[0]


def parse_page(raw_page):
    soup = BeautifulSoup(raw_page, 'html.parser')
    tags = soup.find_all(["p", "a", "ul", "al", "li",
                          "h1", "h2", "h3", "h4", "h5", "h6"])
    raw_page_print, raw_page_file = [], []
    for tag in tags:
        raw_line = tag.text.strip() # .replace("\n", "")
        raw_line = raw_line.replace("Python Developer???s Guide", "Python Developer’s Guide")
        raw_line = raw_line.replace("avoid noisy Unicode characters like z???a???l???g??o??? and byte order", "avoid noisy Unicode characters like z̯̯͡a̧͎̺l̡͓̫g̹̲o̡̼̘ and byte order")
        if raw_line != "": # and raw_line[-1] != " ":
            if tag.name == "a":
                raw_page_file.append(raw_line)
                raw_page_print.append(Fore.BLUE + raw_line + Style.RESET_ALL)
            else:
                raw_page_file.append(raw_line)
                raw_page_print.append(raw_line)
    return raw_page_print, raw_page_file


history = []

while True:
    url = input()
    with open("urls.txt", "a") as f:
            f.write(url + "\n")
    if url == "exit":
        break
    if url == "back":
        if history:
            if len(history) > 1:
                history.pop()
            url = history.pop()
        else:
            continue

    if "." not in url:
        print("Invalid URL")
    else:
        url = fix_url(url)
        history.append(url)
        page_print, page_file = parse_page(requests.get(url).text.encode('cp1251', 'replace'))
        for line in page_print:
            print(line)
        fn = os.path.join(args.dir, get_filename(url))
        with open(fn, "w", encoding="utf-8") as f:
            for line in page_file:
                f.write(line + "\n")
