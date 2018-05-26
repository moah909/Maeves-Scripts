import re
import bs4

PhD_regex  = re.compile(",? Ph\.?D\.?")
mailto_pat = re.compile("mailto")

def cleanName(name):
    name = re.sub(PhD_regex,"",name)
    name = re.sub(" +"," ",name)
    return name.strip()

def cleanPosition(position):
    position = position.split(" of ")[0] # Only get the chunk before of eg Professor of Anthropology
    position = re.sub(" +"," ",position)
    return position.strip()

def cleanDepartment(dept):
    dept = re.sub("Department of ","",dept)
    dept = re.sub(" +"," ",dept)
    return dept.strip()

def getEmailFromSubpage(link):
    suburl = re.sub("/people/[^/]*$",link['href'],directory_page)
    subsoup = BeautifulSoup(urlopen(suburl),"html.parser")
    return subsoup.find(href=mailto_pat.text)
