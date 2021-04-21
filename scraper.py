import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords

domains = [".ics.uci.edu", ".cs.uci.edu", ".informatics.uci.edu", ".stat.uci.edu", "today.uci.edu/department/information_computer_sciences/"]
tokensDict = {}
uniquePageCount = 0

def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp):
    # Implementation requred.
    pageurls = []
    
    #good response the 200s
    if resp.status > 299:
        return []
    
    rawContent = resp.raw_response.content
    beautifulSoup = BeautifulSoup(rawContent, 'html.parser')
    
    for link in beautifulSoup.find_all('a'):
        if link.get('href') != None:
            pageurls.append(link.get('href'))
    return pageurls
    

def is_valid(url):
#     print("Test: ", end="")
#     print(url)
    
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        
        #https://docs.python.org/3/library/urllib.parse.html
        hasValidDomain = False
        for d in domains:
            if d in parsed.netloc:
                 hasValidDomain = True
        if hasValidDomain == False:
            return False
        
        if re.match(r"^.*calendar.*$", parsed.path.lower()):
            return False
        
        if re.match(r"^.*(respond|comment).*$", parsed.fragment.lower()):
            return False
        
        if re.match(r"^.*(\/files).*$", parsed.path.lower()):
            return False
        
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print("URL: ", url)
        print ("TypeError for ", parsed)
        raise
    
def tokenize(text):
    stop_words = stopwords.words('english')
    tokens = nltk.word_tokenize(text)
         
    for word in tokens: 
        if word not in stop_words and len(word) > 2: 
            if word in tokensDict:
                tokensDict[word] += 1
            else:
                tokensDict[word] = 1
                 
                 
def popular_tokens():
    #https://www.askpython.com/python/dictionary/sort-a-dictionary-by-value-in-python
    sortedTokens = dict(sorted(tokensDict.items(), key=lambda item: item[1])) 
    return sortedTokens

# import re
# from urllib.parse import urlparse
# from bs4 import BeautifulSoup
# import nltk
# from nltk.corpus import stopwords
# from enum import unique
# 
# 
# domains = [".ics.uci.edu", ".cs.uci.edu", ".informatics.uci.edu", ".stat.uci.edu", "today.uci.edu/department/information_computer_sciences/"]
# tokensDict = {}
# uniquePageCount = 0
# 
# def scraper(url, resp):
#     links = extract_next_links(url, resp)
#     return [link for link in links if is_valid(link)]
# 
# def extract_next_links(url, resp):
#     # Implementation requred.
#     pageurls = []
#     
#     if resp.status > 299:
#         return []
#     
#     rawContent = resp.raw_response.content
#     beautifulSoup = BeautifulSoup(rawContent, 'html.parser')
#     
# #     tokenize(beautifulSoup.get_text().lower())
# #     file = open("tokens.txt", "w")
# #     file.write("Tokens: ")
# #     sortedTokens = popular_tokens()
# #     for key in sortedTokens:
# #         file.write(f"{key} - {sortedTokens[key]}\n")
# #     file.close()
#     
#     
#     for link in beautifulSoup.find_all('a'):
#         if link.get('href') != None:
#             pageurls.append(link.get('href'))
#     return pageurls
#     
# 
# def is_valid(url):
#     try:
#         parsed = urlparse(url)
#         if parsed.scheme not in set(["http", "https"]):
#             return False
#         
#         #https://docs.python.org/3/library/urllib.parse.html
#         hasValidDomain = False
#         for d in domains:
#             if d in parsed.netloc:
#                  hasValidDomain = True
#             else:
#                 return False
# 
#         
#         if re.match(r"^.*calendar.*$", parsed.path.lower()):
#             return False
#         
#         if re.match(r"^.*(respond|comment).*$", parsed.fragment.lower()):
#             return False
#         
#         if re.match(r"^.*(\/files).*$", parsed.path.lower()):
#             return False
#         
#         return not re.match(
#             r".*\.(css|js|bmp|gif|jpe?g|ico"
#             + r"|png|tiff?|mid|mp2|mp3|mp4"
#             + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
#             + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
#             + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
#             + r"|epub|dll|cnf|tgz|sha1"
#             + r"|thmx|mso|arff|rtf|jar|csv"
#             + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())
#         
#     except TypeError:
#         print("URL: ", url)
#         print ("TypeError for ", parsed)
#         raise
#     
# def tokenize(text):
#     stop_words = stopwords.words('english')
#     tokens = nltk.word_tokenize(text)
#         
#     for word in tokens: 
#         if word not in stop_words and len(word) > 2: 
#             if word in tokensDict:
#                 tokensDict[word] += 1
#             else:
#                 tokensDict[word] = 1
#                 
#                 
# def popular_tokens():
#     #https://www.askpython.com/python/dictionary/sort-a-dictionary-by-value-in-python
#     sortedTokens = dict(sorted(tokensDict.items(), key=lambda item: item[1])) 
#     return sortedTokens


