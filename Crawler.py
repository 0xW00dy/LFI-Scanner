from bs4 import BeautifulSoup
import requests
import re
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