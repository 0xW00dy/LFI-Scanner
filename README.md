# LFI-Scanner

This is a simple Scanner for Local File Inclusion.

Usage: 

```
lfiscan.py [options] [arguments]

--url <url>            : URL of the website
--scan                 : Crawl the website to search for vulnerable URLs
--test                 : Tests an URL for LFI
--inject [type] [opts] : Executes LFI Injection on vulnerable URL
```

At the moment you can:

- Retrieve the content of a page from a website vulnerable to php://filter
- Crawl a website searching for vulnerable pages
- Test if a URL might be vulnerable


NB: I can't be responsible for what you might do with this tool.


Currently Work In Progress, Doesn't work at all atm
