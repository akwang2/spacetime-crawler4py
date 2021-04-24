import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords

domains = [".ics.uci.edu", ".cs.uci.edu", ".informatics.uci.edu", ".stat.uci.edu", "today.uci.edu/department/information_computer_sciences/"]
tokensDict = {}
longestPage = ""
uniquePageCount = 0
longestPageCount = 0
icsSubdomains = {}
uniquePages = []


def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]


def extract_next_links(url, resp):
    global longestPageCount
    global longestPage

    pageurls = []
    
    if resp.status > 299:
        return []
    
    rawContent = resp.raw_response.content
    beautifulSoup = BeautifulSoup(rawContent, 'html.parser')
    count = tokenize(beautifulSoup.get_text().lower())
    if (count > longestPageCount):
        longestPageCount = count
        longestPage = url
    f = open("PageLength.txt", "w")
    f.write(f"{longestPage} has {longestPageCount} words")
    f.close()
    
    getTopTokens()
    
    for link in beautifulSoup.find_all('a'):
        if link.get('href') != None:
            pageurls.append(link.get('href'))
    return pageurls
    

def is_valid(url):
    global uniquePageCount
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        
        #https://docs.python.org/3/library/urllib.parse.html
        hasValidDomain = False
        for d in domains:
            if d in parsed.netloc:
                hasValidDomain = True
                #check if the url is a subdomain of ics.uci.edu and add to dictionary
                domain = parsed.netloc.lower()
                if "ics.uci.edu" in domain:
                    if domain in icsSubdomains:
                        icsSubdomains[domain] += 1
                    else:
                        icsSubdomains[domain] = 1
        if hasValidDomain == False:
            return False
        
        saveSubdomains()
                
        if re.match(r"^.*calendar.*$", parsed.path.lower()):
            return False
        
        if re.match(r"^.*(respond|comment).*$", parsed.fragment.lower()):
            return False
        
        if re.match(r"^.*(\/files).*$", parsed.path.lower()):
            return False
                    
        
        valid = not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz|ppsx)$", parsed.path.lower())
        
        if valid:
            page = parsed.netloc + parsed.path
            if page.lower() not in uniquePages:
                uniquePages.append(page.lower())
                uniquePageCount += 1
            file = open("PageCount.txt", "w")
            file.write(f"Number of unique pages: {uniquePageCount}")
            file.close()
        return valid

    except TypeError:
        print("URL: ", url)
        print ("TypeError for ", parsed)
        raise
    
    
def tokenize(text):
    tokens = nltk.word_tokenize(text)
    count = 0
         
    for word in tokens: 
        if re.match('^[a-zA-Z0-9]+$', word) and word not in stopwords.words('english') and len(word) > 2: 
            if word in tokensDict:
                tokensDict[word] += 1
            else:
                tokensDict[word] = 1
        if re.match('^[a-zA-Z0-9]+$', word) and len(word) > 2:
            count += 1
    return count
                 

def getTopTokens():
    tokens = sorted(tokensDict.items(), key=lambda x: x[1], reverse=True)
    file = open("tokens.txt", "w")
    file.write("Tokens:\n")
    for i in tokens[0:50]:
        file.write(f"{i[0]} - {i[1]}\n")
    file.close()
    

def saveSubdomains():
    f = open("subdomains.txt", "w")
    f.write(f"Subdomains: {len(icsSubdomains)}\n")
    alphabetical = sorted(icsSubdomains.keys())
    for i in alphabetical:
        f.write(f"{i}, {icsSubdomains[i]}\n")
    f.close()


