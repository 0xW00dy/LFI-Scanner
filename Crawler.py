from bs4 import BeautifulSoup
import requests
import threading

class Crawler:
    def __init__(self, url):
        if not url.startswith("http://") and not url.startswith("https://"):
            print("It seems that http:// is not present in the url you typed.")
        else:
            self.url = url
            self.visited = [self.url]
            self.toVisit = []
            self.crawl(url)

    def crawl(self, url):
        self.visited.append(url)
        print(f"[~] Visited url: {url}")
        site = requests.get(url)
        soup = BeautifulSoup(site.text, 'lxml')
        links = []

        toVisit = []
        for link in soup.findAll('a'):
            links.append(link.get('href'))
        for link in soup.findAll('link'):
            links.append(link.get('href'))
            
        for i in links:
            print(i)   
            
        for link in links:
            if self.url.split('/')[2] in str(link):
                if str(link).startswith('.'):
                    toVisit.append(self.url + link[1:])
                    toVisit.append(link)   
                elif str(link).startswith('?'):
                    toVisit.append(self.url + link)
                    toVisit.append(link)
                elif str(link).startswith('/'):
                    url = self.url.split('/')[0] + '//' + self.url.split('/')[2] 
                    toVisit.append(url + link)
                elif str(link).startswith('http'):
                    url = link
                    toVisit.append(url)
            
        for link in toVisit:
            if not link in self.visited and not link == self.url and "http" in link:
                self.crawl(link)
                
        def get_crawled():
            return self.visited
