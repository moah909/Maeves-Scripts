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

def getEmailFromSubpage(link):
    suburl = re.sub("/departments/.*$",link['href'],directory_page)
    subsoup = BeautifulSoup(urlopen(suburl),"html.parser")
    return subsoup.find(class_="email").text

# query the website and return the html to the variable 'page'
page = urlopen(directory_page)

# parse the html using beautiful soup and store in variable 'soup'
soup = BeautifulSoup(page, 'html.parser')

dept = input("Department: ")

# Get all entries in the table
faculty = soup.find_all(class_="faculty-preview")

i = 1;

for person in faculty:
    name = person.find(class_="faculty-name").text.strip()
    name = re.sub(" +"," ",name).strip()
    names.append(name)
    try:
        emails.append(getEmailFromSubpage(person.find("a")))
    except:
        print("\rEmail not found for {}".format(names[-1]))
        emails.append("")
    try:
        position = person.find(class_="faculty-title").text.strip()
        position = position.split(" of ")[0]
        position = position.split(" in ")[0]
        positions.append(position)
    except:
        print("\rPosition not found for {}".format(names[-1]))
        positions.append("")

    print("\r{}/{}".format(i,len(faculty)), end = "")
    i += 1

print()

with open('paul_output.csv', 'a+', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for x in range(0,len(names)):
        try:
            writer.writerow([names[x],emails[x],positions[x],dept])
        except:
            print("There was an issue writing data for {}".format(names[x]))
