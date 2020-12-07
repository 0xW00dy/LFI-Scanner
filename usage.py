from items import payloads

def usage():
    print("Usage: ./lfiscan.py [option] [argument]")
    print("Options:")
    print("--help                 : Show this ")
    print("--url <url>            : URL of the website")
    print("--scan                 : Crawl the website to search for vulnerable URLs")
    print("--test                 : Tests an URL for LFI")
    print("--inject [type] [opts] : Executes LFI Injection on vulnerable URL")
    
    
def injection_usage():
    print("Invalid type for inject option.")
    print("Syntax:")
    print("lfiscan.py --url=url --inject [type] [resource]")
    print("You can use on of these option:")
    for key in payloads:
        print(f"{key} : {payloads[key]}")
    