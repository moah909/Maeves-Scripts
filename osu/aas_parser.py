# import libraries
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv
import html

pages=[]
names=[]
positions = []
emails = []
directory_page = input('URL: ')

def getPositionFromSubpage(link):
    suburl = re.sub("/[^/]*$",link['href'],directory_page)
    subsoup = BeautifulSoup(urlopen(suburl),"html.parser")
    return subsoup.find(class_="field-name-field-asc-people-title").text

# query the website and return the html to the variable 'page'
page = urlopen(directory_page)

# parse the html using beautiful soup and store in variable 'soup'
soup = BeautifulSoup(page, 'html.parser')

try:
    dept = soup.find(id="logo")['alt']
except:
    dept = input("Department: ")

# Get all entries in the table
faculty = soup.find(class_="views-table").find_all("tr")

i = 1;

for person in faculty:
    name = person.find("a",href=re.compile("/people")).text
    name = re.sub(" +"," ",name).strip()
    names.append(name)
    try:
        emails.append(person.find(href=re.compile("mailto")).text.strip())
    except:
        print("\rEmail not found for {}".format(names[-1]))
        emails.append("")
    try:
        position = person.find(class_="views-field-title").contents[3]
        if "..." in position:
            position = getPositionFromSubpage(person.find("a",href=re.compile("/people")))
        positions.append(position)
    except:
        print("\rPosition not found for {}".format(names[-1]))
        positions.append("")

    print("\r{}/{}".format(i,len(faculty)), end = "")
    i += 1

print()

with open('aas_output.csv', 'a+', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for x in range(0,len(names)):
        try:
            writer.writerow([names[x],emails[x],positions[x],dept])
        except:
            print("There was an issue writing data for {}".format(names[x]))
