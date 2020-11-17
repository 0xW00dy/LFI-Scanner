#!/bin/python3

import os, sys
import re
import requests
from bs4 import BeautifulSoup
import threading

class Crawler:
    def __init__(self, url):
        if not url.startswith("http://") and not url.startswith("https://"):
            print("It seems that http:// is not present in the url you typed.")
        else:
            self.url = url
            self.visited = [self.url]
            self.crawl(url)
            for link in list(set(self.visited)):
                print(link)

    def crawl(self, url):
        self.visited.append(url)
        site = requests.get(url)
        soup = BeautifulSoup(site.text, 'lxml')
        links = []

        for link in soup.findAll('a'):
            link = link['href']
            reg = re.compile("^\*.\*.\*\/")
            if self.url in link and not self.url == link:
                links.append(link) 
            elif link.startswith('.'):
                links.append(self.url + link[1:])   
            elif link.startswith('?'):
                links.append(self.url + link)
            elif not reg.search(url):
                links.append(self.url + link)

        for link in links:
            if not link in self.visited and not link == self.url:
                self.visited.append(link)
                self.crawl(link)


def usage():
    print("Usage: ./lfiscan.py [option] [argument]")
    print("Options:")
    print("--url <url>     : URL of the website")
    print("--scan          : Crawl the website to search for vulnerable URLs")
    print("--test          : Tests a vulnerable URL for LFI")
    print("--inject [type] : Executes LFI Injection on vulnerable URL")
    print("Be careful, this app only tracks for LFI vulnerable in URLs.")

def isVulnerable(url):
    regex = re.compile('\?[a-zA-Z0-9]{1,}=')
    if regex.search(url):
        return True
    return False

def scan(url):
    pass

def test(url):
    pass

def inject(url, injectionType):
    pass

if __name__ == '__main__':
    crawler = Crawler('http://challenge01.root-me.org/web-serveur/ch16/')