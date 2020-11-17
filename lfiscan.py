#!/usr/bin/env python3

import os, sys
import re
import requests
import threading


def usage():
    print("Usage: ./lfiscan.py [option] [argument]")
    print("Options:")
    print("--url <url>     : URL of the website")
    print("--scan          : Crawl the website to search for vulnerable URLs")
    print("--test          : Tests a vulnerable URL for LFI")
    print("--inject [type] : Executes LFI Injection on vulnerable URL")
    print("Be careful, this app only tracks for LFI vulnerabilities in URLs.")

def mayBeVulnerable(url):
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