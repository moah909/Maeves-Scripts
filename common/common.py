import re
from bs4 import BeautifulSoup
import requests

PhD_regex  = re.compile("(,? Ph\.?D\.?)|(,? M\.?D\.?)")
mailto_pat = re.compile("mailto")

def cleanName(name, flip=False, delim = None, index=0):
    if delim is not None:
        name = name.split(delim)[index]
    name = name.split("- ")[0]
    name = re.sub(PhD_regex,"",name)
    name = re.sub(" +"," ",name)
    if flip:
        name = (" ".join(name.split(", ")[1::-1]))
    return name.strip()

def cleanPosition(position, delim=None, index=0):
    if delim is not None:
        position = position.split(delim)[index]
    position = position.split(" of ")[0] # Only get the chunk before of eg Professor of Anthropology
    position = re.sub("\\n"," ",position)
    position = re.sub(" +"," ",position)
    return position.strip()

def cleanDepartment(dept):
    dept = re.sub("Department of ","",dept)
    dept = re.sub(" +"," ",dept)
    return dept.strip()

def getEmailFromSubpage(link,regex,base_url):
    suburl = re.sub(regex,link['href'],base_url)
    subsoup = BeautifulSoup(urlopen(suburl),"html.parser")
    return subsoup.find(href=mailto_pat.text)

def getPositionFromSubpage(link,regex,base_url,args,kwargs):
    suburl = re.sub(regex,link['href'],base_url)
    subsoup = BeautifulSoup(urlopen(suburl),"html.parser")
    return subsoup.find(*args,**kwargs)

def writeToCSV(filename,array):
    with open(filename, 'a+', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in array:
            writer.writerow(row)

def getSoup(url):
    return BeautifulSoup(requests.get(url).content,"html.parser")

def getStrings(chunk):
    return [string for string in chunk.stripped_strings]
